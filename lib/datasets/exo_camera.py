import numpy as np
import os
import cv2
from utils.transforms import linear_transform

##------------------------------------------------------------------------------------
class ExoCamera:
    def __init__(self, cfg, root_dir, colmap_dir, exo_camera_name='cam01', coordinate_transform=None, reconstruction=None, exo_camera_mapping=None, max_time_stamps=4):
        self.cfg = cfg
        self.root_dir = root_dir
        self.exo_camera_name = exo_camera_name
        self.camera_name = exo_camera_name

        self.exo_camera_id = int(self.exo_camera_name.replace('cam', ''))
        self.colmap_dir = colmap_dir
        self.type_string = 'rgb'
        self.camera_type = 'exo'

        self.images_path = os.path.join(self.root_dir, self.exo_camera_name, 'images')
        self.intrinsics_calibration_file = os.path.join(self.colmap_dir, 'cameras.txt')
        self.extrinsics_calibration_file = os.path.join(self.colmap_dir, 'images.txt')

        self.coordinate_transform = coordinate_transform
        self.reconstruction = reconstruction

        ###----------set image width and height----------
        self.image_height, self.image_width = self.set_image_resolution()

        ##--------load intrinsics------------
        ### load intrisncis for other cameras if colmap did not converge for these gopros
        ## intrisicnsi of gopors are approximately similar for same resolution
        self.colmap_camera_id = exo_camera_mapping[self.exo_camera_name]
        self.intrinsics = self.reconstruction.cameras[self.colmap_camera_id]

        ##------------load all extrinsics-----
        self.all_extrinsics = {}
        self.all_extrinsics_image = {} ## image is pycolmap object

        for image_id, image in self.reconstruction.images.items():
            image_path = image.name
            image_camera_name = image_path.split('/')[0]
            time_stamp = int((image_path.split('/')[1]).replace('.jpg', ''))

            if image_camera_name == self.exo_camera_name:
                self.all_extrinsics[time_stamp] = image.projection_matrix() ## 3 x 4
                self.all_extrinsics_image[time_stamp] = image

            if len(self.all_extrinsics.keys()) > max_time_stamps:
                break
        
        return  

    ##--------------------------------------------------------
    def set_image_resolution(self):
        image_path = self.get_image_path(time_stamp=1)
        image = cv2.imread(image_path)
        image_height = image.shape[0]
        image_width = image.shape[1]

        return image_height, image_width

    ##--------------------------------------------------------
    def set_closest_calibration(self, time_stamp):
        min_dist_time_stamp = None
        min_dist = None

        ## nearest neighbour by time stamps
        for calib_time_stamp in self.all_extrinsics.keys():
            dist = abs(calib_time_stamp - time_stamp)

            if min_dist == None or dist < min_dist:
                min_dist = dist
                min_dist_time_stamp = calib_time_stamp

        if min_dist_time_stamp == None:
            print('{} extrinsics not found, you should be in manual calibration mode or better know what you are doing! returning dummy_extrinsics'.format(self.exo_camera_name))
            dummy_extrinsics = (np.eye(4))[:3, :]
            return None, dummy_extrinsics

        self.calib_time_stamp = min_dist_time_stamp

        return self.all_extrinsics_image[min_dist_time_stamp], self.all_extrinsics[min_dist_time_stamp]

    ##--------------------------------------------------------
    def update(self, time_stamp):
        self.extrinsics_image, self.extrinsics = self.set_closest_calibration(time_stamp=time_stamp)
        self.raw_extrinsics = np.concatenate([self.extrinsics, [[0, 0, 0, 1]]], axis=0)
        self.extrinsics = np.dot(self.raw_extrinsics, self.coordinate_transform)
        self.time_stamp = time_stamp
        self.location = self.get_location()

        return

    ##--------------------------------------------------------
    def get_image_path(self, time_stamp):
        image_path = os.path.join(self.images_path, '{:05d}.jpg'.format(time_stamp))

        return image_path

    def get_image(self, time_stamp):
        image_path = self.get_image_path(time_stamp=time_stamp) 
        image = cv2.imread(image_path)

        return image

    def get_location(self):
        self.inv_extrinsics = np.linalg.inv(self.extrinsics)
        center = np.dot(self.inv_extrinsics, np.array([0, 0, 0, 1]).reshape(4, 1))
        location = center[:3].reshape(-1)

        return location

    ##-------------vectorized version of projection----------------
    ## point_3d is N x 3, vectorized projection
    ## 3D to 2D using perspective projection and then radial tangential thin prism distortion
    def vec_project(self, point_3d):
        assert(point_3d.shape[0] >= 1 and point_3d.shape[1] == 3)

        point_3d_cam = self.vec_cam_from_world(point_3d)
        point_2d = self.vec_image_from_cam(point_3d_cam)

        return point_2d

    ##--------------------------------------------------------
    ## to camera coordinates 3D from world cooredinate 3D
    def vec_cam_from_world(self, point_3d):
        point_3d_cam = linear_transform(point_3d, self.extrinsics)

        return point_3d_cam

    # to image coordinates 2D from camera cooredinate 3D
    # https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
    def vec_image_from_cam(self, point_3d, eps=1e-9):
        fx, fy, cx, cy, k1, k2, k3, k4 = self.intrinsics.params

        x = point_3d[:, 0]
        y = point_3d[:, 1]
        z = point_3d[:, 2]

        a = x/z; b = y/z
        r = np.sqrt(a*a + b*b)
        theta = np.arctan(r)

        theta_d = theta * (1 + k1*theta**2 + k2*theta**4 + k3*theta**6 + k4*theta**8)
        x_prime = (theta_d/r)*a
        y_prime = (theta_d/r)*b

        u = fx*(x_prime + 0) + cx
        v = fy*y_prime + cy

        point_2d = np.concatenate([u.reshape(-1, 1), v.reshape(-1, 1)], axis=1)

        return point_2d