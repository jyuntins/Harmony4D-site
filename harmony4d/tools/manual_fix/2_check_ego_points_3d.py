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

    vis_output_path = os.path.join(args.output_path, 'vis_manual_calibration_3d') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    
    ## we start with t=1
    # ego_time_stamps = [142, 175, 492, 561, 608, 695] ## rgb, volley, aria01
    # ego_time_stamps = [1, 120, 200, 470, 570, 595] ## left, volley, aria01
    # ego_time_stamps = [345, 420, 497, 703, 749, 1002] ## left, volley, aria01

    # ego_time_stamps = [1, 212, 345, 400, 510, 545] ## rgb, volley, aria02
    # ego_time_stamps = [120, 165, 306, 488] ## rgb, volley, aria03
    ego_time_stamps = [51, 408, 950] ## rgb, volley, aria04

    # target_camera_name = 'aria01'
    # target_camera_name = 'aria02'
    # target_camera_name = 'aria03'
    target_camera_name = 'aria04'

    camera_mode = 'rgb'
    # camera_mode = 'left'
    # camera_mode = 'right'

    ego_factor = 1.4 ## resize factor, the original image is too big

    triangulator = Triangulator(scene.cfg, 1, [], [], [], [], {}, {})

    ##-------------------labelled points from aria-------------------------
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
        def click_event(event, x, y, flags, params):
            # ----------------checking for left mouse clicks--------------
            if event == cv2.EVENT_LBUTTONDOWN:
                params['points_idx'] += 1
                cv2.circle(params['canvas'], (x, y), 3, (0, 0, 255), -1)
                params['canvas'] = cv2.putText(params['canvas'], 'id:{}'.format(params['points_idx']), (x, y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 1, cv2.LINE_AA)
                params['points'].append((x, y))

            return

        ###------------------------------------------------------------------------------------
        window_title = '{}-{}--target_time_stamp'.format(target_camera_name, t)
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

    num_points = len(points_2d[ego_time_stamps[0]])

    ###--------------triangulate----------------
    points_3d = np.zeros((num_points, 3))
    for point_idx in range(num_points):
        proj_matricies = []
        points = []

        for t in ego_time_stamps:
            scene.update(time_stamp=t)
            camera = scene.cameras[(target_camera_name, camera_mode)]
            point_2d = points_2d[t][point_idx]
            extrinsics = camera.extrinsics[:3, :] ## 3x4
            ray_3d = camera.cam_from_image(point_2d=point_2d)
            assert(len(ray_3d) == 3 and ray_3d[2] == 1)  
            point = ray_3d.copy()
            points.append(point)
            proj_matricies.append(extrinsics)

        point_3d, inlier_views, reprojection_error_vector = triangulator.triangulate_ransac(proj_matricies, points, n_iters=100, reprojection_error_epsilon=0.01, direct_optimization=True)
        points_3d[point_idx, :] = point_3d[:]
        print(reprojection_error_vector, inlier_views)

    ##-----------reproject to ego---------------
    for t in ego_time_stamps:
        scene.update(time_stamp=t)
        factor = ego_factor
        camera = scene.cameras[(target_camera_name, camera_mode)]
        image_path = camera.get_image_path(time_stamp=t)
        image = cv2.imread(image_path)
        image_original_width = image.shape[1]
        image_original_height = image.shape[0]
        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)

        projected_points_2d = camera.vec_project(points_3d) ## in aria orientation

        print('labelled points in aria orientation')
        print(points_2d[t]); print()

        print('reprojected points in aria orientation')
        print(projected_points_2d); print()

        print('point in 3d')
        print(points_3d); print()

        x = projected_points_2d[:, 0].copy()
        y = projected_points_2d[:, 1].copy()

        rotated_x = image_original_width - y
        rotated_y = x 

        projected_points_2d[:, 0] = rotated_x
        projected_points_2d[:, 1] = rotated_y        

        for idx in range(num_points):
            image = cv2.circle(image, (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1])), 3, (0, 0, 255), -1)
            image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1]) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        window_title = '{}-{}'.format(target_camera_name, t)

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

    print(points_3d)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()