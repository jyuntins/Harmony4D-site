import numpy as np
import os
import cv2
from utils.transforms import linear_transform

##------------------------------------------------------------------------------------
class AriaCamera:
    def __init__(self, cfg, human_id='', camera_name='', type_string='rgb', calibration_path='', images_path=''):
        self.cfg = cfg
        self.human_id = human_id
        self.type_string = type_string
        self.camera_type = 'ego'
        self.camera_name = camera_name
        self.calibration_path = calibration_path
        self.images_path = os.path.join(images_path, self.type_string)
        
        self.image_height, self.image_width = self.set_image_resolution()
        self.rotated_image_height = self.image_width
        self.rotated_image_width = self.image_height

        self.intrinsics = None
        self.extrinsics = None

        return  

    ##--------------------------------------------------------
    def get_image_path(self, time_stamp):
        image_path = os.path.join(self.images_path, '{:05d}.jpg'.format(time_stamp))
        return image_path

    # ##--------------------------------------------------------
    def set_image_resolution(self):
        time_stamp_string = sorted(os.listdir(self.calibration_path))[0].replace('.txt', '')
        image_path = self.get_image_path(time_stamp=int(time_stamp_string))
        image = cv2.imread(image_path)
        image_height = image.shape[0]
        image_width = image.shape[1]
        return image_height, image_width

    # ##--------------------------------------------------------
    def update(self, intrinsics, extrinsics):
        # the parameter vector has the following interpretation:
        # intrinsic = [f c_u c_v [k_0: k_5]  {p_0 p_1} {s_0 s_1 s_2 s_3}]
        self.intrinsics = intrinsics
        assert(self.intrinsics.shape[0] == 15)

        self.extrinsics = extrinsics

        assert(self.extrinsics.shape[0] == 4 and self.extrinsics.shape[1] == 4)
        self.inv_extrinsics = np.linalg.inv(self.extrinsics)

        ## finding a XYX such that [0, 0, 0, 1] = [R, T; 0 1] * [XYZ1];
        center = np.dot(self.inv_extrinsics, np.array([0, 0, 0, 1]).reshape(4, 1))
        self.location = center[:3].reshape(-1)

        return  

    # ##--------------------------------------------------------
    def get_image(self, time_stamp):
        image_path = self.get_image_path(time_stamp=time_stamp)
        image = cv2.imread(image_path)
        return image

    def get_location(self):
        return self.location

    # ###----------aria frame to human frame----------
    def get_inverse_rotated_pose2d(self, pose2d, bbox=None):
        assert(pose2d.shape[1] == 3 or pose2d.shape[1] == 2) ## x, y, score
        assert bbox is None

        x = pose2d[:, 0].copy()
        y = pose2d[:, 1].copy()

        rotated_x = self.rotated_image_height - y
        rotated_y = x 

        pose2d[:, 0] = rotated_x
        pose2d[:, 1] = rotated_y

        return pose2d

    #-------------vectorized version of projection----------------
    # point_3d is N x 3, vectorized projection
    # 3D to 2D using perspective projection and then radial tangential thin prism distortion
    def vec_project(self, point_3d):
        assert(point_3d.shape[0] >= 1 and point_3d.shape[1] == 3)
        point_3d_cam = self.vec_cam_from_world(point_3d)
        point_2d = self.vec_image_from_cam(point_3d_cam)
        return point_2d


    ## to camera coordinates 3D from world cooredinate 3D
    def vec_cam_from_world(self, point_3d):
        point_3d_cam = linear_transform(point_3d, self.extrinsics)
        return point_3d_cam

    ## reference: https://math.stackexchange.com/questions/4144827/determine-if-a-point-is-in-a-cameras-field-of-view-3d
    def vec_check_point_behind_camera(self, point_3d):    
        return point_3d[:, 2] < 0 


    ## to image coordinates 2D from camera cooredinate 3D
    ## reference: https://ghe.oculus-rep.com/minhpvo/NikosInternship/blob/04e672190a11c76d0b810ebc121f46a2aa5b67e4/aria_hand_obj/aria_utils/geometry.py#L29
    ## reference: https://www.internalfb.com/code/fbsource/[0c9e159d90aee8bfeff67a6e2066726a5ecc1796]/arvr/projects/surreal/experiments/PseudoGT/increAssoRecon/core/geometry.cpp?lines=567
    ## the intrinsics paramters are // intrinsic = [f_u {f_v} c_u c_v [k_0: k_5]  {p_0 p_1} {s_0 s_1 s_2 s_3}]
    ## the intrinsics paramters are // intrinsic = [f c_u c_v [k_0: k_5]  {p_0 p_1} {s_0 s_1 s_2 s_3}], 15 in total. f_u = f_v
    ## k_1, k_2, k_3, k_4, k_5, and k_6 are radial distortion coefficients. p_1 and p_2 are tangential distortion coefficients. Higher-order coefficients are not considered in OpenCV.
    def vec_image_from_cam(self, point_3d, eps=1e-9):
        is_point_behind_camera = self.vec_check_point_behind_camera(point_3d)

        ##------------------
        startK = 3
        numK = 6
        startP = startK + numK
        startS = startP + 2

        ##------------------
        inv_z = 1/point_3d[:, -1]
        ab = point_3d[:, :2].copy() * inv_z.reshape(-1, 1) ## makes it [u, v, w] to [u', v', 1]
            
        ab_squared = ab**2
        r_sq = ab_squared[:, 0] + ab_squared[:, 1]
        
        r = np.sqrt(r_sq)
        th = np.arctan(r)
        thetaSq = th**2

        th_radial = np.ones(len(point_3d))
        theta2is = thetaSq.copy()

        ## radial distortion
        for i in range(numK):
            th_radial += theta2is * self.intrinsics[startK + i]
            theta2is *= thetaSq

        th_divr = th / r
        th_divr[r < eps] = 1

        xr_yr = (th_radial.reshape(-1, 1).repeat(2, 1) * th_divr.reshape(-1, 1).repeat(2, 1)) * ab
        xr_yr_squared_norm = (xr_yr**2).sum(axis=1)

        uvDistorted = xr_yr.copy()
        temp = 2.0 * xr_yr * self.intrinsics[startP:startP+2]
        uvDistorted += temp * xr_yr + xr_yr_squared_norm.reshape(-1, 1).repeat(2, 1)  * self.intrinsics[startP:startP+2]

        radialPowers2And4 = np.concatenate([xr_yr_squared_norm.reshape(-1, 1), (xr_yr_squared_norm**2).reshape(-1, 1)], axis=1)

        uvDistorted[:, 0] += (self.intrinsics[startS:startS+2] * radialPowers2And4).sum(axis=1)
        uvDistorted[:, 1] += (self.intrinsics[startS+2:] * radialPowers2And4).sum(axis=1)

        point_2d = self.intrinsics[0] * uvDistorted + self.intrinsics[1:3]

        point_2d[is_point_behind_camera] = -1

        return point_2d
