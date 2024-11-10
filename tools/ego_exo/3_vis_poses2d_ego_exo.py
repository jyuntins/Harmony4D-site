import sys
import numpy as np
import os
import argparse
from tqdm import tqdm
import cv2

import _init_paths
from datasets.ego_exo_scene import EgoExoSceneVis
from config import cfg
from utils.transforms import fast_circle

def main():
    parser = argparse.ArgumentParser(description='Visualization of 2D poses of the sequence.')
    parser.add_argument('--sequence_path', action='store', help='the input path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the output path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    print('sequence at {}'.format(sequence_path))

    ##-----------------load the scene-----------------------
    scene = EgoExoSceneVis(cfg=cfg, root_dir=sequence_path)

    ##-----------------load smpl-----------------------
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = len([file for file in os.listdir(scene.pose3d_dir) if file.endswith('npy')])

    time_stamps = list(range(start_time, end_time + 1)) 

    ##-----------------create output folder-----------------------
    vis_output_path = os.path.join(args.output_path, 'vis_poses2d') 
    os.makedirs(vis_output_path, exist_ok=True)

    ##-------------------------Visualize----------------------------
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)
        cameras = scene.exo_camera_names_with_mode + scene.ego_camera_names_with_mode

        for (camera_name, camera_mode) in tqdm(cameras):
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)

            if camera_name in ['aria01', 'aria02']:
                joints_2d = np.load(sequence_path + '/processed_data/poses2d/{}/{}/{:05d}.npy'.format(camera_name, camera_mode, t), allow_pickle=True).item()
            else:
                joints_2d = np.load(sequence_path + '/processed_data/poses2d/{}/{:05d}.npy'.format(camera_name, t), allow_pickle=True).item()
            
            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))

            scene.draw_pose2d(joints_2d, save_path)

    print('done, start:{}, end:{} -- both inclusive!'.format(start_time, end_time))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()