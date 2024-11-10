import numpy as np
import os
import cv2
import pickle
import pycolmap
import smplx

from .aria_human import AriaHuman
from .exo_camera import ExoCamera

from utils.transforms import linear_transform, fast_circle
from utils.keypoint import show_result

np.random.seed(0) ## seed the numpy so that the results are reproducible
##------------------------------------------------------------------------------------
class EgoExoSceneVis:
    def __init__(self, cfg, root_dir):
        self.cfg = cfg
        self.root_dir = root_dir
        self.exo_dir = os.path.join(self.root_dir, 'exo')
        self.ego_dir = os.path.join(self.root_dir, 'ego')    
        self.colmap_dir = os.path.join(self.root_dir, 'colmap', 'workplace')

        ########################## We visualize 3D poses and SMPL ############################ 
        self.pose3d_dir = os.path.join(self.root_dir, 'processed_data', 'poses3d')
        self.smpl_dir = os.path.join(self.root_dir, 'processed_data', 'smpl')

        ########################## Colmap Transformations #####################################
        ## scale.npy is the transformation from colmap to metric coordinate system
        self.sequence_mode = None # We have sequence captured with and without aria  

        if os.path.exists(os.path.join(self.colmap_dir, 'scale.npy')):
            self.sequence_mode = 'exo'
            T = np.load(os.path.join(self.colmap_dir, 'scale.npy'))
            self.primary_transform = np.linalg.inv(T)

        else:
            self.sequence_mode = 'ego_exo'

            colmap_transforms_file = os.path.join(self.colmap_dir, 'colmap_from_aria_transforms.pkl') 
            inv_colmap_transforms_file = os.path.join(self.colmap_dir, 'aria_from_colmap_transforms.pkl') ## colmap to aria

            with open(colmap_transforms_file, 'rb') as handle:
                self.colmap_from_aria_transforms = pickle.load(handle) ## aria coordinate system to colmap

            with open(inv_colmap_transforms_file, 'rb') as handle:
                self.inv_colmap_from_aria_transforms = pickle.load(handle) ## colmap coordinate system to aria

            self.anchor_ego_camera = self.cfg.CALIBRATION.ANCHOR_EGO_CAMERA # We typically use aria01 as the anchor camera
            self.primary_transform = self.colmap_from_aria_transforms[self.anchor_ego_camera] # Transformation from Aria01 to Colmap

        print('sequence mode: {}'.format(self.sequence_mode))
        ########################## Initialize Aria Human ########################################
        self.aria_human_names = ['aria01', 'aria02']
        self.aria_humans = {}

        for person_idx, aria_human_name in enumerate(self.aria_human_names):
            
            if self.sequence_mode == 'ego_exo':
                coordinate_transform = np.dot(
                                    np.linalg.inv(self.colmap_from_aria_transforms[aria_human_name]), 
                                    self.primary_transform
                                ) # VxP, where P is the transform from aria01 to colmap coordinate, and V is the transform from colmap coordinate system to designated aria camera 
            else:
                coordinate_transform = np.eye(4)
                self.ego_dir = None

            self.aria_humans[aria_human_name] = AriaHuman(
                                                cfg=cfg,
                                                sequence_mode = self.sequence_mode, 
                                                root_dir=self.ego_dir,
                                                human_name=aria_human_name,
                                                human_id=person_idx,
                                                coordinate_transform=coordinate_transform)

        ########################## Initialize Exo Camera ########################################
        self.exo_camera_mapping = self.get_colmap_camera_mapping()
        self.exo_camera_names = [exo_camera_name for exo_camera_name in sorted(os.listdir(self.exo_dir)) if exo_camera_name not in self.cfg.INVALID_EXOS and exo_camera_name.startswith('cam')]

        self.colmap_reconstruction = pycolmap.Reconstruction(self.colmap_dir) ## this is the bottleneck
        self.exo_cameras = {exo_camera_name: ExoCamera(cfg=cfg, root_dir=self.exo_dir, colmap_dir=self.colmap_dir, \
                        exo_camera_name=exo_camera_name, coordinate_transform=self.primary_transform, reconstruction=self.colmap_reconstruction, \
                        exo_camera_mapping=self.exo_camera_mapping) \
                        for exo_camera_name in sorted(self.exo_camera_names)}  

        ########################## Camera Names and Modes ########################################
        self.ego_camera_names_with_mode = [(aria_human_name, camera_mode) \
                        for aria_human_name in self.aria_human_names \
                        for camera_mode in ['rgb', 'left', 'right']]

        if self.sequence_mode == "exo":
            self.ego_camera_names_with_mode = []

        self.exo_camera_names_with_mode = [(camera_name, camera_mode) \
                        for camera_name in self.exo_camera_names \
                        for camera_mode in ['rgb']]

        ########################## Flags for Loading Data ########################################
        self.load_pose3d_flag = False
        self.load_smpl_flag = False


    def update(self, time_stamp):
        self.time_stamp = time_stamp

        ## update aria humans
        for aria_human_name in self.aria_humans.keys():
            self.aria_humans[aria_human_name].update(time_stamp=self.time_stamp)    

        ## update exo cameras
        for exo_camera_name in self.exo_cameras.keys():
            self.exo_cameras[exo_camera_name].update(time_stamp=self.time_stamp)        

        ## load 3d poses
        if self.load_pose3d_flag == True:
            pose3d_path = os.path.join(self.pose3d_dir, '{:05d}.npy'.format(time_stamp))

            pose3d = np.load(pose3d_path, allow_pickle=True)

            self.set_poses3d(pose3d.item()) ## ndarray to dict, set the refined pose!

        ## load smpl params
        if self.load_smpl_flag == True:
            smpl_path = os.path.join(self.smpl_dir, '{:05d}.npy'.format(time_stamp))
            smpl = np.load(smpl_path, allow_pickle=True)
            self.set_smpl(smpl.item()) ## ndarray to dict      

        return

    def set_view(self, camera_name='aria01', camera_mode='rgb'):
        camera, view_type = self.get_camera(camera_name, camera_mode)
        self.view_camera = camera
        self.view_camera_type = camera_mode
        self.view_type = view_type ## ego or exo
        self.viewer_name = camera_name

        return 

    def get_camera(self, camera_name='aria01', camera_mode='rgb'):
        camera = None
        view_type = None

        if camera_name in self.aria_human_names:
            view_type = 'ego'
            if camera_mode == 'rgb':
                camera = self.aria_humans[camera_name].rgb_cam

            elif camera_mode == 'left':
                camera = self.aria_humans[camera_name].left_cam

            elif camera_mode == 'right':
                camera = self.aria_humans[camera_name].right_cam

        elif camera_name in self.exo_camera_names:
            view_type = 'exo'
            camera = self.exo_cameras[camera_name]

        else:
            print('invalid camera name!: {},{}'.format(camera_name, camera_mode))
            exit()

        return camera, view_type

    def init_pose2d_rgb(self):
        self.rgb_pose_num_keypoints =  133

        ## Keypoint radius for visualization
        self.rgb_pose_radius = { \
                        ('exo', 'rgb'): self.cfg.POSE2D.VIS.RADIUS.EXO_RGB,
                        ('ego', 'rgb'): self.cfg.POSE2D.VIS.RADIUS.EGO_RGB,
                        ('ego', 'left'): self.cfg.POSE2D.VIS.RADIUS.EGO_LEFT,
                        ('ego', 'right'): self.cfg.POSE2D.VIS.RADIUS.EGO_RIGHT,
                    } 

        ## Link thickness for visualization
        self.rgb_pose_thickness = { \
                        ('exo', 'rgb'): self.cfg.POSE2D.VIS.THICKNESS.EXO_RGB,
                        ('ego', 'rgb'): self.cfg.POSE2D.VIS.THICKNESS.EGO_RGB,
                        ('ego', 'left'): self.cfg.POSE2D.VIS.THICKNESS.EGO_LEFT,
                        ('ego', 'right'): self.cfg.POSE2D.VIS.THICKNESS.EGO_RIGHT,
                    } 

        return

    def load_pose3d(self):
        self.load_pose3d_flag = True
        self.total_time_pose3d = len([file for file in os.listdir(self.pose3d_dir) if file.endswith('npy')])

        return         

    def set_poses3d(self, poses3d):
        for human_name in poses3d.keys():
            self.aria_humans[human_name].set_pose3d(pose3d=poses3d[human_name])

        return

    def load_smpl(self):
        self.load_smpl_flag = True
        self.total_time_smpl = len([file for file in os.listdir(self.smpl_dir) if file.endswith('npy')])
        self.smpl_faces = self.get_smpl_faces()

        return

    def get_smpl_faces(self):
        smpl_model = smplx.create(self.cfg.SMPL_MODEL_DIR, "smpl")
        smpl_model_faces = smpl_model.faces

        return smpl_model_faces

    def set_smpl(self, smpl):
        for human_name in smpl.keys():
            self.aria_humans[human_name].set_smpl(smpl=smpl[human_name])

        return

    def get_colmap_camera_mapping(self):
        self.intrinsics_calibration_file = os.path.join(self.colmap_dir, 'cameras.txt')
        self.extrinsics_calibration_file = os.path.join(self.colmap_dir, 'images.txt')

        with open(self.intrinsics_calibration_file) as f:
            intrinsics = f.readlines()
            intrinsics = intrinsics[3:] ## drop the first 3 lines

        colmap_camera_ids = []
        is_exo_camera = []
        for line in intrinsics:
            line = line.split()
            colmap_camera_id = int(line[0])
            colmap_camera_model = line[1]
            image_width = int(line[2])
            image_height = int(line[3])

            colmap_camera_ids.append(colmap_camera_id)

            if image_height == 1408 and image_width == 1408:
                is_exo_camera.append(False)
            else:
                is_exo_camera.append(True)

        num_colmap_arias = len(is_exo_camera) - sum(is_exo_camera)
        num_arias = len(os.listdir(self.ego_dir))
        exo_camera_names = sorted(os.listdir(self.exo_dir))

        ## get the name of the folder containing the camera name for the exo cameras
        exo_camera_mapping = {}
        for (colmap_camera_id, is_valid) in zip(colmap_camera_ids, is_exo_camera):
            if is_valid == True:
                exo_camera_name = self.get_camera_name_from_colmap_camera_id(colmap_camera_id)
                assert(exo_camera_name is not None)
                exo_camera_mapping[exo_camera_name] = colmap_camera_id            

        return exo_camera_mapping
    

    def get_camera_name_from_colmap_camera_id(self, colmap_camera_id):
        with open(self.extrinsics_calibration_file) as f:
            extrinsics = f.readlines()
            extrinsics = extrinsics[4:] ## drop the first 4 lines
            extrinsics = extrinsics[::2] ## only alternate lines

        for line in extrinsics:
            line = line.strip().split()
            camera_id = int(line[-2])
            image_path = line[-1]
            camera_name = image_path.split('/')[0]

            if camera_id == colmap_camera_id:
                return camera_name

        return None

    def get_projected_poses3d(self):
        pose_results = {}

        for human_name in self.aria_humans:
            if human_name != self.viewer_name:
                pose3d = self.aria_humans[human_name].pose3d ## 17 x 4
                projected_pose3d = self.view_camera.vec_project(pose3d[:, :3]) ## 17 x 2
                projected_pose3d = np.concatenate([projected_pose3d, pose3d[:, 3].reshape(-1, 1)], axis=1) ## 17 x 3 (homogeneous)

                ## rotated poses from aria frame to human frame
                if self.view_camera.camera_type == 'ego':
                    projected_pose3d = self.view_camera.get_inverse_rotated_pose2d(pose2d=projected_pose3d)

                pose_results[human_name] = projected_pose3d

        return pose_results

    def draw_projected_poses3d(self, pose_results, save_path):
        image_name = self.view_camera.get_image_path(time_stamp=self.time_stamp)

        camera_type=self.view_camera.camera_type ## ego or exo
        camera_mode=self.view_camera.type_string  ## rgb, left or right

        if camera_mode == 'rgb':
            keypoint_thres = self.cfg.POSE2D.RGB_THRES
        else:
            keypoint_thres = self.cfg.POSE2D.GRAY_THRES

        pose_results_ = []
        for human_name in pose_results.keys():
            pose = pose_results[human_name] ## 17 x 3
            pose_ = np.zeros((self.rgb_pose_num_keypoints, 3))

            pose_[:len(pose), :3] = pose[:, :]

            pose_result = {'keypoints':pose_}
            pose_results_.append(pose_result)
        
        pose_results = pose_results_            

        show_result(image_name,
                    pose_results,
                    kpt_score_thr=keypoint_thres,
                    radius=self.rgb_pose_radius[(camera_type, camera_mode)],
                    thickness=self.rgb_pose_thickness[(camera_type, camera_mode)],
                    show=False,
                    out_file=save_path,
        )

        return


    def draw_smpl(self, smpl, save_path):
        original_image = self.view_camera.get_image(time_stamp=self.time_stamp)
        image = original_image.copy()
        overlay = 255*np.ones(image.shape)
        alpha = 0.7

        for human_name in smpl.keys():
            ## skip if human_name is the same as aria
            if human_name == self.viewer_name:
                continue

            smpl_human = smpl[human_name]
            color = self.aria_humans[human_name].color

            points_3d = smpl_human['vertices']
            points_2d = self.view_camera.vec_project(points_3d)

            ## rotated poses from aria frame to human frame
            if self.view_camera.camera_type == 'ego':
                points_2d = self.view_camera.get_inverse_rotated_pose2d(pose2d=points_2d)

            is_valid = (points_2d[:, 0] >= 0) * (points_2d[:, 0] < image.shape[1]) * \
                        (points_2d[:, 1] >= 0) * (points_2d[:, 1] < image.shape[0])

            points_2d = points_2d[is_valid] ## only plot inside image points

            ## for exo
            if image.shape[0] > 1408:
                radius = 3
            else:
                radius = 1

            image, overlay = fast_circle(image, overlay, points_2d, radius, color)

        image = cv2.addWeighted(image, alpha, original_image, 1 - alpha, 0)
        image = np.concatenate([image, overlay], axis=1)

        ##----------------
        cv2.imwrite(save_path, image)

        return

    def draw_pose2d(self, pose2d, save_path):
        original_image = self.view_camera.get_image(time_stamp=self.time_stamp)
        image = original_image.copy()
        overlay = 255*np.ones(image.shape)
        alpha = 0.7

        for human_name in pose2d.keys():

            if human_name == self.viewer_name:
                continue

            color = self.aria_humans[human_name].color

            points_2d = pose2d[human_name]

            is_valid = (points_2d[:, 0] >= 0) * (points_2d[:, 0] < image.shape[1]) * \
                        (points_2d[:, 1] >= 0) * (points_2d[:, 1] < image.shape[0])

            points_2d = points_2d[is_valid] ## only plot inside image points

            ## for exo
            if image.shape[0] > 1408:
                radius = 10
            else:
                radius = 5

            image, overlay = fast_circle(image, overlay, points_2d, radius, color)

        image = cv2.addWeighted(image, alpha, original_image, 1 - alpha, 0)
        image = np.concatenate([image, overlay], axis=1)

        ##----------------
        cv2.imwrite(save_path, image)

        return

    def draw_smpl_bboxes(self, bboxes, save_path): 
        image_name = self.view_camera.get_image_path(time_stamp=self.time_stamp)
        image = cv2.imread(image_name)
        color = (0, 0, 255)
        for aria in bboxes.keys():
            bbox_2d = bboxes[aria]

            if image.shape[0] > 1408:
                thickness = 12
            elif image.shape[0] == 1408:
                thickness = 5
            else:
                thickness = 2

            image = cv2.rectangle(image, (round(bbox_2d[0]), round(bbox_2d[1])), (round(bbox_2d[2]), round(bbox_2d[3])), color, thickness)
        
        ##----------------        
        cv2.imwrite(save_path, image)

        return 
