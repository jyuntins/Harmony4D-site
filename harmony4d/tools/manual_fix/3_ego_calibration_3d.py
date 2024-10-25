import _init_paths
import cv2 
import glob
import numpy as np
import sys
from scipy import linalg
import yaml
import os
from scipy.spatial.transform import Rotation as R
from aria_camera import *
from utils.procrustes_alignment import procrustes_alignment, inner_procrustes_alignment

# https://www.pythonpool.com/opencv-solvepnp/

## returns T x points_3d
def linear_transform(points_3d, T):
    points_3d_homo = np.ones((4, points_3d.shape[0]))
    points_3d_homo[:3, :] = np.copy(points_3d.T)

    points_3d_prime_homo = np.dot(T, points_3d_homo)
    points_3d_prime = points_3d_prime_homo[:3, :]/ points_3d_prime_homo[3, :]
    points_3d_prime = points_3d_prime.T
    return points_3d_prime

# ###----------------------------------------------------------------------------
# # # https://yangcha.github.io/iview/iview.html

# target_camera_name = "aria02"
# sequence_name = 'volleyball_calibration'

target_camera_name = "aria01"
sequence_name = 'frisbee_calibration'

###--------------------------------------------------------------------------------
save_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/colmap/workplace/manual_calib/{}'.format(sequence_name, target_camera_name)
read_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/colmap/workplace/manual_calib/{}'.format(sequence_name, target_camera_name)
os.makedirs(save_dir, exist_ok=True)

###------------------------------------------------------------------------------------
all_points_2d = np.load(os.path.join(read_dir, 'points_2d.npy'), allow_pickle=True).item()
points_3d = np.load(os.path.join(read_dir, 'points_3d_colmap_frame.npy'), allow_pickle=True)
points_3d_aria_frame = np.load(os.path.join(read_dir, 'points_3d_aria_frame.npy'), allow_pickle=True)

time_stamps = all_points_2d.keys()
colmap_centers = []
aria_centers = []
all_extrinsics = {}

for time_stamp in time_stamps:
    image_path = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/ego/{}/images/rgb/{:05d}.jpg'.format(sequence_name, target_camera_name, time_stamp)
    calib_file_path = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/ego/{}/calib/{:05d}.txt'.format(sequence_name, target_camera_name, time_stamp)
    with open(calib_file_path) as f:
        lines = f.readlines()
        lines = lines[1:] ## drop the header, eg. Serial, intrinsics (radtanthinprsim), extrinsic (3x4)
        lines = [line.strip() for line in lines]

    intrinsics = np.asarray([float(x) for x in lines[1].split(' ')])
    assert(intrinsics.shape[0] == 15)
    aria_extrinsics = np.asarray([float(x) for x in lines[2].split(' ')]).reshape(4, 3).T
    aria_extrinsics = np.concatenate([aria_extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4

    image = cv2.imread(image_path)
    image_width = image.shape[1]
    image_height = image.shape[0]

    points_2d = all_points_2d[time_stamp]

    ###--------------------------------------------------------------------------------
    f = intrinsics[0]
    fx = f; fy = f
    cx = intrinsics[1]
    cy = intrinsics[2]
    k1 = intrinsics[3]
    k2 = intrinsics[4]
    k3 = intrinsics[5]
    k4 = intrinsics[6]
    k5 = intrinsics[7]
    k6 = intrinsics[8]
    p1 = intrinsics[9]
    p2 = intrinsics[10]
    s1 = intrinsics[11]
    s2 = intrinsics[12]
    s3 = intrinsics[13]
    s4 = intrinsics[14]

    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    D = np.array([k1, k2, p1, p2, k3, k4, k5, k6, s1, s2, s3, s4]) ## distCoeffs1 output vector of distortion coefficients [k1,k2,p1,p2,k3,k4,k5,k6,s1,s2,s3,s4,taux,tauy] of 4, 5, 8, 12 or 14 elements. 

    ##----------undistort points--------------
    undistorted_points_2d = undistort(points_2d, intrinsics)
    K_undistorted = K.copy()

    ###-------------------------------------------------------------------------------------------------
    success, rotation_vector, translation_vector = cv2.solvePnP(points_3d, undistorted_points_2d, K_undistorted, None, flags=0)
    rotation_matrix = R.from_rotvec(rotation_vector.reshape(-1)).as_matrix()
    ## this is the aria's extrinsics in colmap reference frame
    new_extrinsics = np.eye(4)
    new_extrinsics[:3, :3] = rotation_matrix[:, :]
    new_extrinsics[:3, 3] = (translation_vector.reshape(-1))[:]

    new_projected_points_2d = project(points_3d, intrinsics, new_extrinsics) ## in aria orientation
    x = new_projected_points_2d[:, 0].copy()
    y = new_projected_points_2d[:, 1].copy()

    rotated_x = image.shape[0] - y
    rotated_y = x
    new_projected_points_2d[:, 0] = rotated_x
    new_projected_points_2d[:, 1] = rotated_y

    for idx in range(len(new_projected_points_2d)):
        image = cv2.circle(image, (round(new_projected_points_2d[idx, 0]), round(new_projected_points_2d[idx, 1])), 3, (0, 0, 255), -1)
        image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(new_projected_points_2d[idx, 0]), round(new_projected_points_2d[idx, 1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    factor = 1.4
    cv2.namedWindow('reprojected points using calibration')
    image_resized = cv2.resize(image, (int(image_width/factor), int(image_height/factor)), interpolation=cv2.INTER_AREA)

    while True:
        cv2.imshow('reprojected points using calibration', image_resized)
        key = cv2.waitKey(5) & 0xFF

        if key == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ### colmap point to aria camera corrdinate
    print('{} extrinsics in colmap frame at t:{}'.format(target_camera_name, time_stamp))
    print(repr(new_extrinsics))
    print()

    ##----compute camera centers in colmap reference frame----
    rotmat = new_extrinsics[:3, :3]
    translation = new_extrinsics[:3, 3]
    colmap_camera_center = -1*np.dot(rotmat.T, translation)
    colmap_centers.append(colmap_camera_center.reshape(1, -1))

    ##----compute camer acenters in aria reference frame----
    rotmat = aria_extrinsics[:3, :3]
    translation = aria_extrinsics[:3, 3]
    aria_camera_center = -1*np.dot(rotmat.T, translation)
    aria_centers.append(aria_camera_center.reshape(1, -1))

    all_extrinsics[time_stamp] = aria_extrinsics

aria_centers = np.concatenate(aria_centers, axis=0)
colmap_centers = np.concatenate(colmap_centers, axis=0)

T, l2_error, output = inner_procrustes_alignment(aria_centers, colmap_centers) ## convert aria centers to colmap centers
print('error:{}, scale:{}'.format(l2_error, output['scale']))
np.save('{}/transform.npy'.format(save_dir), T)

###------------------------debug----------------------------
# colmap_centers_hat = linear_transform(aria_centers, T)

# import pdb; pdb.set_trace()

# def qvec2rotmat(qvec):
#   return np.array([
#       [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
#        2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
#        2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
#       [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
#        1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
#        2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
#       [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
#        2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
#        1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

# t = 505
# #   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
# line = "29 -0.05041609806298037 0.69483951552476853 0.69359666022053845 0.18324829508708634 -0.19996880902600389 2.2176226551521712 1.237169928964952 1 aria01/00505.jpg"
# line = line.strip().split()
# qvec = np.asarray([float(element) for element in line[1:5]]) ## QW, QX, QY, QZ
# translation = np.asarray([float(element) for element in line[5:8]]) ## TX, TY, TZ
# rotmat = qvec2rotmat(qvec=qvec)

# import pdb; pdb.set_trace()