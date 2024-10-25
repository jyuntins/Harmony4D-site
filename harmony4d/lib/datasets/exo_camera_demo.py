import os
import json
import numpy as np
from .exo_camera import ExoCamera

class ExoCameraDemo(ExoCamera):
    def __init__(self, root_dir=None, exo_camera_name="cam01"):
        self.root_dir = root_dir
        self.exo_camera_name = exo_camera_name
        self.camera_name = exo_camera_name
        self.type_string = "rgb"
        self.camera_type = "exo"
        self.images_path = os.path.join(root_dir, "exo", exo_camera_name, "images")

        ###----------set image width and height----------
        self.image_height, self.image_width = self.set_image_resolution()

    def update(self, time_stamp):
        with open(os.path.join(self.root_dir, f"exo/calib_json/{self.exo_camera_name}/{time_stamp:05d}.json"), "r") as f:
            params = json.load(f)
        
        # pinhole intrinsics
        self.intrinsics = np.zeros((3, 4))
        self.intrinsics[:, :3] = np.array(params[0]['payload'][0]['data']['camera_intrinsics']) # 3 x 3
        
        self.extrinsics = np.array(params[0]['payload'][0]['data']['camera_extrinsics'])
        self.extrinsics = np.concatenate([self.extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4
        
        self.projection = np.matmul(self.intrinsics, self.extrinsics) # 3d to 2d projection matrix for pinhole
        # self.extrinsics = np.dot(self.raw_extrinsics, self.coordinate_transform)

        self.time_stamp = time_stamp

        self.location = self.get_location()

    # pinhole camera
    def vec_project(self, point_3d):
        # point_3d is N x 3
        n = point_3d.shape[0]
        homo_points = np.ones((n, 4)) # N x 4
        homo_points[:, :3] = point_3d

        projected_pose = np.matmul(self.projection, homo_points.T).T # N x 3

        pose2d = np.zeros((n, 2))
        pose2d[:, 0] = projected_pose[:, 0] / projected_pose[:, 2]
        pose2d[:, 1] = projected_pose[:, 1] / projected_pose[:, 2]

        return pose2d
        
