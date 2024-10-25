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

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    vis_output_path = os.path.join(args.output_path, 'vis_overlay') 
    mesh_path = os.path.join(args.output_path, 'vis_mesh')

    print('sequence at {}'.format(sequence_path))

    os.makedirs(vis_output_path, exist_ok=True)
    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    ##-----------------visualize-----------------------
    time_stamps = [int(name.replace('.png', '')) for name in sorted(os.listdir(mesh_path)) if name.endswith('.png')]
    camera_name = cfg.BLENDER.OVERLAY_CAMERA
    camera_mode = 'rgb'

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)
        scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
        save_dir = vis_output_path
        save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))

        image = scene.view_camera.get_image(time_stamp=t)
        image = cv2.resize(image, (0,0), fx=1/7, fy=1/7) 
        render_image = cv2.imread(os.path.join(mesh_path, '{:05d}.png'.format(t)))

        render_image[:image.shape[0], :image.shape[1], :] = image[:, :, :]

        cv2.imwrite(save_path, render_image)

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()