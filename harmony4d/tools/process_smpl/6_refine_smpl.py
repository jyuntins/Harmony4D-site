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

    args = parser.parse_args()
    sequence_path = args.sequence_path
    output_path = os.path.join(args.output_path, 'refine_smpl') 
    vis_output_path = os.path.join(args.output_path, 'vis_refine_smpl') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(root_dir=sequence_path)
    scene.init_refine_smpl()
    
    ## we start with t=1
    time_stamps = list(range(1, scene.total_time_pose3d + 1)) 

    for t in tqdm(time_stamps):
        print('time_stamp:{}'.format(t))
        scene.update(time_stamp=t)
        

        import pdb; pdb.set_trace()

        # smpl = scene.get_smpl()
        # save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        # scene.save_smpl(smpl, save_path)

        # camera_names = scene.camera_names
        # for (camera_name, camera_mode) in camera_names:
        #     scene.set_view(camera_name=camera_name, camera_mode=camera_mode)

        #     save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
        #     os.makedirs(save_dir, exist_ok=True)
        #     save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
        #     scene.draw_smpl(smpl, save_path)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()