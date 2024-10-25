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
    parser.add_argument('--start_time_stamp', default=0, action='store', help='start time stamp')
    parser.add_argument('--end_time_stamp', default=10, action='store', help='end time stamp')

    args = parser.parse_args()

    start_time_stamp = int(args.start_time_stamp)
    end_time_stamp = int(args.end_time_stamp)

    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'mesh_obj') 
    vis_output_path = os.path.join(args.output_path, 'vis_mesh') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    scene.load_smpl()
    scene.init_blender_vis()
    
    if end_time_stamp == -1:
        end_time_stamp = scene.total_time_smpl

    time_stamps = list(range(start_time_stamp, end_time_stamp + 1))

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t) ## loads the smpl parameters

        save_dir = os.path.join(output_path, '{:05d}'.format(t))
        scene.save_mesh_as_obj(save_dir)

        save_path = os.path.join(vis_output_path, '{:05d}.jpg'.format(t))
        scene.blender_vis(mesh_dir=save_dir, save_path=save_path)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()