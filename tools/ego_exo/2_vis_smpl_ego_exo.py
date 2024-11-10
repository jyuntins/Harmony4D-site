import sys
import numpy as np
import os
import argparse
from tqdm import tqdm
import cv2

import _init_paths
from datasets.ego_exo_scene import EgoExoSceneVis
from config import cfg

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of SMPLs of sequences.')
    parser.add_argument('--sequence_path', action='store', help='the input path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the output path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    parser.add_argument('--choosen_time', default="", help='choosen time')
    parser.add_argument('--single_camera', action="store_true")

    args = parser.parse_args()
    sequence_path = args.sequence_path
    print('sequence at {}'.format(sequence_path))

    ##-----------------load the scene-----------------------
    scene = EgoExoSceneVis(cfg=cfg, root_dir=sequence_path)

    ##-----------------load smpl-----------------------
    start_time = int(args.start_time)
    end_time = int(args.end_time)

    scene.load_smpl()
    if end_time == -1:
        end_time = scene.total_time_smpl  

    ##-----------------create output folder-----------------------
    vis_output_path = os.path.join(args.output_path, 'vis_smpl')
    os.makedirs(vis_output_path, exist_ok=True)

    ##-----------------time stamps-----------------------
    if args.choosen_time != '':
        time_stamps = [int(val) for val in args.choosen_time.split(':')]
    else:
        time_stamps = list(range(start_time, end_time + 1))

    ##-----------------visualize-----------------------
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)
        cameras = scene.exo_camera_names_with_mode + scene.ego_camera_names_with_mode
        smpl = {human_name: scene.aria_humans[human_name].smpl for human_name in scene.aria_human_names}

        if args.single_camera: # Only visualize Cam01 and Aria01
            cameras = [('cam01', 'rgb')]

        for (camera_name, camera_mode) in tqdm(cameras):
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