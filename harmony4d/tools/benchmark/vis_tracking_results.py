import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import cv2
from datasets.ego_exo_scene import EgoExoScene

from configs import cfg
from configs import update_config
from pycocotools.coco import COCO
import pickle

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--result_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')

    args = parser.parse_args()

    import pdb; pdb.set_trace()


    ## the results from results_path, it is a pkl file
    results = pickle.load(open(args.result_path, 'rb'))

    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    output_path = os.path.join(args.output_path) 
    os.makedirs(output_path, exist_ok=True)

    time_stamps = list(range(1, scene.total_time  + 1))

    camera_mode = 'rgb'

    if args.mode == 'all':
        camera_names = scene.aria_human_names + scene.exo_camera_names
        if len(scene.exo_camera_names) > 9:
            print('more than 9 exo cameras, only undistorting the first 9!')
            camera_names = scene.aria_human_names + ['cam01', 'cam02', 'cam03', 'cam04', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']

    elif args.mode == 'ego':
        camera_names = scene.aria_human_names

    elif args.mode == 'exo':
        camera_names = scene.exo_camera_names
        if len(scene.exo_camera_names) > 9:
            print('more than 9 exo cameras, only undistorting the first 9!')
            camera_names = ['cam01', 'cam02', 'cam03', 'cam04', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']

    ##-----------init undistort---------------
    scene.update(time_stamp=1) ## we assume the intrinsics of the camera do not change with time
    for camera_name in camera_names:
        scene.cameras[(camera_name, camera_mode)].init_undistort_map()

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        for camera_name in camera_names:
            camera = scene.cameras[(camera_name, camera_mode)]

            if camera_name.startswith('aria'):
                output_dir = os.path.join(output_path, 'ego', camera_name, 'images', 'undistorted_rgb') 
            else:
                output_dir = os.path.join(output_path, 'exo', camera_name, 'undistorted_images') 

            os.makedirs(output_dir, exist_ok=True)

            image = camera.get_undistorted_image(time_stamp=t)
            cv2.imwrite(os.path.join(output_dir, '{:05d}.jpg'.format(t)), image) ## save the aria image

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()