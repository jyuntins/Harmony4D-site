import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
from colour import Color
import cv2
import matplotlib.pyplot as plt
from cycler import cycle
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import mmcv

from datasets.aria_camera import AriaCamera
from datasets.aria_human import AriaHuman
from datasets.ego_exo_scene import EgoExoScene

from configs import cfg
from configs import update_config
from utils.transforms import linear_transform
from utils.triangulation import Triangulator

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    print('sequence at {}'.format(sequence_path))

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    
    ## we start with t=1
    # time_stamps = list(range(1, scene.total_time + 1))  
    # time_stamps = list(range(1, 2 + 1))  
    # time_stamps = [1, 220, 420, 620] 
    # ego_time_stamps = [15, 118, 233, 437] 

    ego_time_stamps = [252, 505, 710, 1606] 

    exo_time_stamp = 1 

    # camera_names = ['cam04', 'cam06', 'cam07', 'cam08', 'cam09']
    # target_camera_name = 'aria01'

    # camera_names = ['cam02', 'cam05', 'cam07', 'cam13', 'cam15']
    # target_camera_name = 'aria02'

    camera_names = ['cam01', 'cam02']
    target_camera_name = 'aria01'

    camera_mode = 'rgb'
    exo_factor = 2.0 ## resize factor, the original image is too big
    ego_factor = 1.4 ## resize factor, the original image is too big

    triangulator = Triangulator(scene.cfg, 1, [], [], [], [], {}, {})

    ##----------------exo run-------------------------------
    scene.update(time_stamp=exo_time_stamp)

    points_2d = {}

    for camera_name in camera_names:
        factor = exo_factor
        camera = scene.cameras[(camera_name, camera_mode)]

        image_path = camera.get_image_path(time_stamp=exo_time_stamp)
        image_original = cv2.imread(image_path)
        image_original_width = image_original.shape[1]
        image_original_height = image_original.shape[0]

        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)
        image = image_original_resized.copy()

        ###------------------------------------------------------------------------------------
        def click_event(event, x, y, flags, params):
            # ----------------checking for left mouse clicks--------------
            if event == cv2.EVENT_LBUTTONDOWN:
                params['points_idx'] += 1
                cv2.circle(params['canvas'], (x, y), 3, (0, 0, 255), -1)
                params['canvas'] = cv2.putText(params['canvas'], 'id:{}'.format(params['points_idx']), (x, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 1, cv2.LINE_AA)
                params['points'].append((x, y))

            return
        
        ###------------------------------------------------------------------------------------
        window_title = '{}-{}'.format(camera_name, exo_time_stamp)
        cv2.namedWindow(window_title)
        params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}
        cv2.setMouseCallback(window_title, click_event, params)

        while True:
            cv2.imshow(window_title, params['canvas'])
            key = cv2.waitKey(5) & 0xFF

            ## refresh everything
            if key == ord("r"):
                params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}

            ## escape
            elif key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        camera_points_2d = np.zeros((len(params['points']), 2))
        for idx, point in enumerate(params['points']):
            camera_points_2d[idx, 0] = point[0]*factor 
            camera_points_2d[idx, 1] = point[1]*factor

        points_2d[camera_name] = camera_points_2d

    num_points = len(points_2d[camera_names[0]])

    ###--------------triangulate----------------
    points_3d = np.zeros((num_points, 3))
    for point_idx in range(num_points):
        proj_matricies = []
        points = []

        for camera_name in camera_names:
            camera = scene.cameras[(camera_name, camera_mode)]
            point_2d = points_2d[camera_name][point_idx]
            extrinsics = camera.extrinsics[:3, :] ## 3x4
            ray_3d = camera.cam_from_image(point_2d=point_2d)
            assert(len(ray_3d) == 3 and ray_3d[2] == 1)  
            point = ray_3d.copy()
            points.append(point)
            proj_matricies.append(extrinsics)

        point_3d, inlier_views, reprojection_error_vector = triangulator.triangulate_ransac(proj_matricies, points, n_iters=100, reprojection_error_epsilon=0.01, direct_optimization=True)
        points_3d[point_idx, :] = point_3d[:]

    ##-----------reproject to exo cameras---------------
    for camera_name in camera_names:
        factor = exo_factor
        camera = scene.cameras[(camera_name, camera_mode)]
        image_path = camera.get_image_path(time_stamp=exo_time_stamp)
        image = cv2.imread(image_path)
        image_original_width = image.shape[1]
        image_original_height = image.shape[0]
        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)

        projected_points_2d = camera.vec_project(points_3d)

        for idx in range(num_points):
            image = cv2.circle(image, (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1])), 10, (0, 0, 255), -1)
            image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1]) - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)


        window_title = '{}-{}'.format(camera_name, exo_time_stamp)

        cv2.namedWindow(window_title)
        cv2.resizeWindow(window_title, image_original_resized.shape[1], image_original_resized.shape[0])
        image_resized = cv2.resize(image, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)

        while True:
            cv2.imshow(window_title, image_resized)
            key = cv2.waitKey(5) & 0xFF

            if key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    ##-------------------now get the labelled points from aria-------------------------
    points_2d = {}
    for t in ego_time_stamps:
        scene.update(time_stamp=t)
        factor = ego_factor
        camera = scene.cameras[(target_camera_name, camera_mode)]

        image_path = camera.get_image_path(time_stamp=t)
        image_original = cv2.imread(image_path)
        image_original_width = image_original.shape[1]
        image_original_height = image_original.shape[0]

        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)
        image = image_original_resized.copy()

        ###------------------------------------------------------------------------------------
        window_title = '{}-{}--target_time_stamp'.format(camera_name, t)
        cv2.namedWindow(window_title)
        params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}
        cv2.setMouseCallback(window_title, click_event, params)

        while True:
            cv2.imshow(window_title, params['canvas'])
            key = cv2.waitKey(5) & 0xFF

            ## refresh everything
            if key == ord("r"):
                params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}

            ## escape
            elif key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        camera_points_2d = np.zeros((len(params['points']), 2))
        for idx, point in enumerate(params['points']):
            camera_points_2d[idx, 0] = point[0]*factor 
            camera_points_2d[idx, 1] = point[1]*factor

            x = camera_points_2d[idx, 0]
            y = camera_points_2d[idx, 1]
            rotated_x = y
            rotated_y = image_original_width - x

            camera_points_2d[idx, 0] = rotated_x
            camera_points_2d[idx, 1] = rotated_y

        points_2d[t] = camera_points_2d


    ####--------------------print 3d---------------------------------
    print('points_3d in aria01 frame')
    print(repr(points_3d)); print()

    print('points_3d in colmap frame')
    points_3d_colmap = linear_transform(points_3d, scene.primary_transform)
    print(repr(points_3d_colmap)); print()

    for t in points_2d.keys():
        print('labelled points_2d for target camera in aria orientation at time_stamp {}'.format(t))        
        print(repr(points_2d[t])); print()

    ###----------------------save info-------------------------
    save_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/colmap/workplace/manual_calib/{}'.format(sequence_name, target_camera_name)
    os.makedirs(save_dir, exist_ok=True)
    np.save(os.path.join(save_dir, 'points_3d_aria_frame.npy'), points_3d)
    np.save(os.path.join(save_dir, 'points_3d_colmap_frame.npy'), points_3d_colmap)
    np.save(os.path.join(save_dir, 'points_2d.npy'), points_2d)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()