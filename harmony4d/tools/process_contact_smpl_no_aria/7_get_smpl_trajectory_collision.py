import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import cv2
import matplotlib.pyplot as plt
from cycler import cycle
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import mmcv

from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'smpl_collision') 
    vis_output_path = os.path.join(args.output_path, 'vis_smpl_collision') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    ##-----------------------------------------------------
    scene.init_smpl_trajectory_collision()
    smpl_trajectory = scene.get_smpl_trajectory_collision() # human x time x smpl

    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = scene.total_time_fit_pose3d_metric

    ## we start with t=1
    time_stamps = list(range(start_time, end_time + 1)) 

    
    ##--------------------------------------------------------------
    ##-------save--------------------
    for t in tqdm(time_stamps):
        print('saving time_stamp:{}'.format(t))
        scene.update(time_stamp=t)
        smpl = {human_name: smpl_trajectory[human_name][t-1] for human_name in smpl_trajectory.keys()}
        save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        scene.save_smpl(smpl, save_path)

    ##----------visualize-----------------
    for t in tqdm(time_stamps):
        print('visualizing time_stamp:{}'.format(t))

        scene.update(time_stamp=t)
        smpl = {human_name: smpl_trajectory[human_name][t-1] for human_name in smpl_trajectory.keys()}
        scene.set_smpl(smpl) ## set the smpl to humans

        camera_names = scene.camera_names

        for (camera_name, camera_mode) in camera_names:

            ##-------------visualize the pose-------------------    
            ## skip cameras if not in vis list
            if not camera_name == "cam01":
                continue
            # if scene.cfg.SMPL.VIS_CAMERAS != [] and camera_name not in scene.cfg.SMPL.VIS_CAMERAS:
            #     continue

            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_smpl(smpl, save_path)

    print('done, start:{}, end:{} -- both inclusive!'.format(start_time, end_time))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()