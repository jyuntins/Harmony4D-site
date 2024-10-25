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
    parser.add_argument('--choosen_time', default="", help='choosen time')


    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    vis_output_path = os.path.join(args.output_path, 'vis_aria_locations') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    
    vis_camera_name = ['cam01', 'cam05', 'cam10', 'cam15']
    ## we start with t=1
    if args.choosen_time != ":::":
        time_stamps = [int(val) for val in args.choosen_time.split(':')]
    else:
        time_stamps = list(range(1, scene.total_time + 1))  

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)
                
        #  ##------------------debug visualize aria center-----------
        for (camera_name, camera_mode) in scene.ego_camera_names_with_mode + scene.exo_camera_names_with_mode:
            if camera_name in vis_camera_name == False:
                continue

            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            locations = scene.get_camera_locations()

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_camera_locations(locations, save_path)    

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()