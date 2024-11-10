import numpy as np
import os
import cv2
from .aria_camera import AriaCamera
import pickle

##------------------------------------------------------------------------------------
class AriaHuman:
    def __init__(self, cfg, sequence_mode, root_dir, human_name, human_id=0, coordinate_transform=None):
        self.cfg = cfg
        self.sequence_mode = sequence_mode
        self.root_dir = root_dir
        self.human_name = human_name
        self.human_id = human_id
        
        if self.human_id == 0:
            self.color = [204, 0, 0] ## bgr, blue
            self.color_string = 'blue'

        elif self.human_id == 1:
            self.color = [0, 204, 0] ## bgr, green
            self.color_string = 'green'

        if self.sequence_mode == "exo":
            return 
        
        self.calibration_path = os.path.join(self.root_dir, self.human_name, 'calib')
        self.total_time = len(sorted(os.listdir(self.calibration_path))) if self.cfg.SEQUENCE_TOTAL_TIME == -1 else self.cfg.SEQUENCE_TOTAL_TIME
        assert(self.total_time <= len(sorted(os.listdir(self.calibration_path))))

        self.images_path = os.path.join(self.root_dir, self.human_name, 'images')

        ## we go from global colmap to aria coordinate
        ## then the self.extrinsics is valid, world to cam cooredinates of the aria 
        self.coordinate_transform = coordinate_transform

        ###--------------------------------------------------------
        self.rgb_cam = AriaCamera(cfg=cfg, human_id=self.human_id, camera_name=human_name, type_string='rgb', calibration_path=self.calibration_path, images_path=self.images_path) ## 0
        self.left_cam = AriaCamera(cfg=cfg, human_id=self.human_id, camera_name=human_name, type_string='left', calibration_path=self.calibration_path, images_path=self.images_path) ## 1
        self.right_cam = AriaCamera(cfg=cfg, human_id=self.human_id, camera_name=human_name, type_string='right', calibration_path=self.calibration_path, images_path=self.images_path) ## 2

        self.location = None ##in the global frame
        self.time_stamp = None

        ##----------------3d pose---------------------
        self.pose3d = None ## per time stamp

        return  
    
    ##--------------------------------------------------------
    def read_calibration(self, time_stamp):
        time_stamp_string = '{:05d}'.format(time_stamp)
        calibration_file = os.path.join(self.calibration_path, '{}.txt'.format(time_stamp_string))

        with open(calibration_file) as f:
            lines = f.readlines()
            lines = lines[1:] ## drop the header, eg. Serial, intrinsics (radtanthinprsim), extrinsic (3x4)
            lines = [line.strip() for line in lines]

        output = {}
        assert(len(lines) % 7 == 0) # 1 for person id, 2 lines each for rgb, left and right cams. Total 7 lines per person
        num_persons = len(lines)//7
        assert(num_persons == 1) ## we assume only single person per calib directory

        for idx in range(num_persons):
            data = lines[idx*7:(idx+1)*7]

            person_id = data[0]
            rgb_intrinsics = np.asarray([float(x) for x in data[1].split(' ')])
            rgb_extrinsics = np.asarray([float(x) for x in data[2].split(' ')]).reshape(4, 3).T

            left_intrinsics = np.asarray([float(x) for x in data[3].split(' ')])
            left_extrinsics = np.asarray([float(x) for x in data[4].split(' ')]).reshape(4, 3).T

            right_intrinsics = np.asarray([float(x) for x in data[5].split(' ')])
            right_extrinsics = np.asarray([float(x) for x in data[6].split(' ')]).reshape(4, 3).T

            ###--------------store everything as nested dicts---------------------
            rgb_cam = {'intrinsics': rgb_intrinsics, 'extrinsics': rgb_extrinsics}
            left_cam = {'intrinsics': left_intrinsics, 'extrinsics': left_extrinsics}
            right_cam = {'intrinsics': right_intrinsics, 'extrinsics': right_extrinsics}

            output[idx] = {'rgb': rgb_cam, 'left': left_cam, 'right':right_cam, 'person_id_string': person_id}

        return output[0] 

    ##--------------------------------------------------------
    def update(self, time_stamp):
        self.time_stamp = time_stamp

        if self.sequence_mode == "exo":
            return

        calibration = self.read_calibration(time_stamp)

        rgb_intrinsics = calibration['rgb']['intrinsics']
        rgb_extrinsics = calibration['rgb']['extrinsics'] ## this is world to camera
        rgb_extrinsics = np.concatenate([rgb_extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4
        rgb_extrinsics = np.dot(rgb_extrinsics, self.coordinate_transform) ## align the world
        self.rgb_cam.update(intrinsics=rgb_intrinsics, extrinsics=rgb_extrinsics)

        left_intrinsics = calibration['left']['intrinsics']
        left_extrinsics = calibration['left']['extrinsics']
        left_extrinsics = np.concatenate([left_extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4
        left_extrinsics = np.dot(left_extrinsics, self.coordinate_transform) ## align the world
        self.left_cam.update(intrinsics=left_intrinsics, extrinsics=left_extrinsics)

        right_intrinsics = calibration['right']['intrinsics']
        right_extrinsics = calibration['right']['extrinsics']
        right_extrinsics = np.concatenate([right_extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4
        right_extrinsics = np.dot(right_extrinsics, self.coordinate_transform) ## align the world
        self.right_cam.update(intrinsics=right_intrinsics, extrinsics=right_extrinsics)

        ## update location in world frame
        self.location = (self.left_cam.get_location() + self.right_cam.get_location())/2

        return

    def set_pose3d(self, pose3d):
        self.pose3d = pose3d
        return

    ##--------------------------------------------------------
    def set_smpl(self, smpl):
        self.smpl = smpl
        return
