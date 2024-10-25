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

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    parser.add_argument('--choosen_time', default="", help='choosen time')


    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'segposes2d') 
    vis_output_path = os.path.join(args.output_path, 'vis_segposes2d') 
    print('sequence at {}'.format(sequence_path))

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    scene.init_segpose2d()

    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if start_time != -1:
        if end_time == -1:
            end_time = scene.total_time 

        time_stamps = list(range(start_time, end_time + 1))
    else:
        assert(args.choosen_time != '')
        time_stamps = [int(val) for val in args.choosen_time.split(':')]

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        # ####---------------------------------------------------
        exo_cameras = [(camera_name, camera_mode) \
                        for camera_name in scene.exo_camera_names \
                        for camera_mode in ['rgb']]

        cameras = exo_cameras; print('only using exo cameras')

        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            poses2d = scene.get_segposes2d()

            ##-----------save poses--------------
            save_dir = os.path.join(output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.npy'.format(t))
            scene.save_poses2d(poses2d, save_path)
            
            # ##-------------visualize the pose-------------------       
             # ##-------------visualize the bboxes-------------------   
            ## skip cameras if not in vis list
            if scene.cfg.POSE2D.VIS_CAMERAS != [] and camera_name not in scene.cfg.POSE2D.VIS_CAMERAS:
                continue

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_poses2d(poses2d, save_path)

    print('done, start:{}, end:{} -- both inclusive!. sequence-len:{} secs'.format(start_time, end_time, scene.total_time/20.0))

    
    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()