import cv2 
import glob
import numpy as np
import sys
from scipy import linalg
import yaml
import os
from scipy.spatial.transform import Rotation as R

###--------------------custom aria projection---------------------------------------------
def project(batch_point_3d, intrinsics, extrinsics):
    assert(batch_point_3d.shape[0] > 1 and batch_point_3d.shape[1] == 3)
    batch_point_2d = []
    for point_3d in batch_point_3d:
        point_2d = project_(point_3d, intrinsics, extrinsics)
        batch_point_2d.append(point_2d.reshape(1, -1))
    batch_point_2d = np.concatenate(batch_point_2d, axis=0)
    return batch_point_2d

def project_(point_3d, intrinsics, extrinsics):
    assert(point_3d.shape[0] == 3)
    point_3d_cam = cam_from_world(point_3d, extrinsics)
    point_2d = image_from_cam(point_3d_cam, intrinsics)
    return point_2d

def cam_from_world(point_3d, extrinsics):
    assert(point_3d.shape[0] == 3)
    point_3d_homo = np.asarray([point_3d[0], point_3d[1], point_3d[2], 1])
    point_3d_cam = np.dot(extrinsics, point_3d_homo)
    point_3d_cam = point_3d_cam[:3]/point_3d_cam[3]
    return point_3d_cam

def image_from_cam(point_3d, intrinsics, eps=1e-9):
    startK = 3
    numK = 6
    startP = startK + numK
    startS = startP + 2
    
    inv_z = 1/point_3d[-1]
    ab = point_3d[:2].copy() * inv_z ## makes it [u, v, w] to [u', v', 1]
    
    ab_squared = ab**2
    r_sq = ab_squared[0] + ab_squared[1]

    r = np.sqrt(r_sq)
    th = np.arctan(r)
    thetaSq = th**2

    th_radial = 1.0 
    theta2is = thetaSq

    ## radial distortion
    for i in range(numK):
        th_radial += theta2is * intrinsics[startK + i]
        theta2is *= thetaSq

    th_divr = 1 if r < eps else th / r

    xr_yr = (th_radial * th_divr) * ab
    xr_yr_squared_norm = (xr_yr**2).sum()

    uvDistorted = xr_yr
    temp = 2.0 * xr_yr * intrinsics[startP:startP+2]
    uvDistorted += temp * xr_yr + xr_yr_squared_norm * intrinsics[startP:startP+2]

    radialPowers2And4 = np.array([xr_yr_squared_norm, xr_yr_squared_norm**2])

    uvDistorted[0] += (intrinsics[startS:startS+2] * radialPowers2And4).sum()
    uvDistorted[1] += (intrinsics[startS+2:] * radialPowers2And4).sum()

    point_2d = intrinsics[0] * uvDistorted + intrinsics[1:3]
    return point_2d


def undistort(batch_point_2d, intrinsics):
    assert(batch_point_2d.shape[0] > 1 and batch_point_2d.shape[1] == 2)
    batch_undistorted_point_2d = []
    for point_2d in batch_point_2d:
        point_2d = undistort_(point_2d, intrinsics)
        batch_undistorted_point_2d.append(point_2d.reshape(1, -1))
    batch_undistorted_point_2d = np.concatenate(batch_undistorted_point_2d, axis=0)
    return batch_undistorted_point_2d

def undistort_(point_2d, intrinsics):
    uvDistorted = (point_2d - intrinsics[1:3]) / intrinsics[0]
    xr_yr = compute_xr_yr_from_uvDistorted(uvDistorted, intrinsics)

    # early exit if point is in the center of the image
    xr_yrNorm = np.sqrt((xr_yr**2).sum())

    if xr_yrNorm == 0:
        temp_ = np.asarray([0, 0])
    else:
        theta = getThetaFromNorm_xr_yr(xr_yrNorm, intrinsics) ## is a double
        temp_ = (np.tan(theta) / xr_yrNorm) * xr_yr ## direct assignment to point_3d[:2] does not work!
    
    undistorted_point_2d = temp_ * intrinsics[0] + intrinsics[1:3]
    return undistorted_point_2d

def compute_xr_yr_from_uvDistorted(uvDistorted, intrinsics, kMaxIterations=50, kDoubleTolerance2=1e-7*1e-7):
    startK = 3
    numK = 6
    startP = startK + numK
    startS = startP + 2

    xr_yr = uvDistorted # initialize

    for j in range(kMaxIterations):
        uvDistorted_est = xr_yr
        xr_yr_squared_norm = (xr_yr**2).sum()

        temp = 2 * xr_yr * intrinsics[startP:startP+2]
        uvDistorted_est += temp * xr_yr + xr_yr_squared_norm * intrinsics[startP:startP+2]

        radialPowers2And4 = np.array([xr_yr_squared_norm, xr_yr_squared_norm**2])

        uvDistorted_est[0] += (intrinsics[startS:startS+2] * radialPowers2And4).sum()
        uvDistorted_est[1] += (intrinsics[startS+2:] * radialPowers2And4).sum()

        ## compute the derivative of uvDistorted wrt xr_yr
        duvDistorted_dxryr =  compute_duvDistorted_dxryr(xr_yr, xr_yr_squared_norm, intrinsics)

        ## compute correction:
        ## the matrix duvDistorted_dxryr will be close to identity ?(for resonable values of tangenetial/thin prism distotions)
        ## so using an analytical inverse here is safe
        correction = np.dot(np.linalg.inv(duvDistorted_dxryr), uvDistorted - uvDistorted_est) 

        xr_yr += correction

        if (correction**2).sum() < kDoubleTolerance2:
            break

    return xr_yr

## helper function, computes the Jacobian of uvDistorted wrt the vector [x_r; y_r]
def compute_duvDistorted_dxryr(xr_yr, xr_yr_squared_norm, intrinsics):
    startK = 3
    numK = 6
    startP = startK + numK
    startS = startP + 2

    duvDistorted_dxryr = np.zeros((2, 2)) ## initialize
    duvDistorted_dxryr[0, 0] = 1.0 + 6.0 * xr_yr[0] * intrinsics[startP] + 2.0 * xr_yr[1] * intrinsics[startP + 1]

    offdiag = 2.0 * (xr_yr[0] * intrinsics[startP + 1] + xr_yr[1] * intrinsics[startP])
    duvDistorted_dxryr[0, 1] = offdiag
    duvDistorted_dxryr[1, 0] = offdiag
    duvDistorted_dxryr[1, 1] = 1.0 + 6.0 * xr_yr[1] * intrinsics[startP + 1] + 2.0 * xr_yr[0] * intrinsics[startP]

    temp1 = 2.0 * (intrinsics[startS] + 2.0 * intrinsics[startS + 1] * xr_yr_squared_norm)
    duvDistorted_dxryr[0, 0] += xr_yr[0] * temp1
    duvDistorted_dxryr[0, 1] += xr_yr[1] * temp1

    temp2 = 2.0 * (intrinsics[startS + 2] + 2.0 * intrinsics[startS + 3] * xr_yr_squared_norm)
    duvDistorted_dxryr[1, 0] += xr_yr[0] * temp2
    duvDistorted_dxryr[1, 1] += xr_yr[1] * temp2

    return duvDistorted_dxryr


def getThetaFromNorm_xr_yr(th_radialDesired, intrinsics, kMaxIterations=50, eps=1e-9):
        th = th_radialDesired
        startK = 3
        numK = 6
        startP = startK + numK
        startS = startP + 2

        for j in range(kMaxIterations):
            thetaSq = th*th

            th_radial = 1
            dthD_dth = 1

            ## compute the theta polynomial and its derivative wrt theta
            theta2is = thetaSq

            for i in range(numK):   
                th_radial += theta2is * intrinsics[startK + i]
                dthD_dth += (2*i + 3) * intrinsics[startK + i] * theta2is
                theta2is *= thetaSq

            th_radial *= th

            ## compute correction
            if np.abs(dthD_dth) > eps:
                step = (th_radialDesired - th_radial)/dthD_dth
            else:
                step = 10*eps if (th_radialDesired - th_radial)*dthD_dth > 0.0 else -10*eps

            th += step

            ## revert to within 180 degrees FOV to avoid numerical overflow
            if np.abs(th) >= np.pi / 2.0:
                ## the exact value we choose here is not really important, we will iterate again over it
                th = 0.999*np.pi/2.0

        return th