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
    output_path = os.path.join(args.output_path, 'mesh_obj') 
    vis_output_path = os.path.join(args.output_path, 'vis_mesh') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)

    scene = EgoExoScene(root_dir=sequence_path)
    scene.init_vis_smpl()
    
    time_stamps = list(range(start_time_stamp, min(end_time_stamp, scene.total_time_smpl) + 1))

    aria_human_name = 'aria01'

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t) ## loads the smpl parameters

        save_dir = os.path.join(output_path, '{:05d}'.format(t))
        scene.save_mesh_as_obj_ego(save_dir)

        save_path = os.path.join(vis_output_path, '{:05d}.jpg'.format(t))
        scene.blender_vis_ego(aria_human_name=aria_human_name, mesh_dir=save_dir, save_path=save_path)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()