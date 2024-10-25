import os
import numpy as np
import argparse
import textwrap
import _init_paths
import pickle

from datasets.exo_camera import ExoCamera
from datasets.aria_human_exo import AriaHuman
from datasets.exo_scene import EgoExoScene
from tqdm import tqdm

from configs import cfg
from configs import update_config

def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    parser.add_argument('--vis', action='store_true')
    parser.add_argument('--ego', action='store_true')
    args = parser.parse_args()

    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(sequence_path, 'processed_data/fit_poses3d_metric')
    vis_output_path = os.path.join(sequence_path, 'processed_data/vis_fit_poses3d_metric') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    scene.load_fit_pose3d_flag = True
    scene.total_time_fit_pose3d = len([file for file in os.listdir(scene.fit_pose3d_dir) if file.endswith('npy')])

    ##-----------------visualize-----------------------
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = scene.total_time_fit_pose3d

    time_stamps = list(range(start_time, end_time + 1))

    scene.init_pose2d_rgb(dummy=True)

    if args.ego:
        colmap_transforms_file = f'{args.sequence_path}/colmap/workplace/colmap_from_aria_transforms.pkl'
        if os.path.exists(colmap_transforms_file):
            with open(colmap_transforms_file, 'rb') as handle:
                colmap_from_aria_transforms = pickle.load(handle)
        else:
            raise Exception("No colmap_from_aria_transforms.pkl file found!")
    # save
    print('saving!')
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)
        # handle the sequence with ego cameras
        if args.ego:
            scene.aria_humans['aria01'].pose3d = np.dot(colmap_from_aria_transforms['aria02'], scene.aria_humans['aria01'].pose3d.T).T
            scene.aria_humans['aria02'].pose3d = np.dot(colmap_from_aria_transforms['aria02'], scene.aria_humans['aria02'].pose3d.T).T

        scene.aria_humans['aria01'].pose3d = np.dot(np.linalg.inv(scene.primary_transform), scene.aria_humans['aria01'].pose3d.T).T
        scene.aria_humans['aria02'].pose3d = np.dot(np.linalg.inv(scene.primary_transform), scene.aria_humans['aria02'].pose3d.T).T

        cameras = scene.exo_camera_names_with_mode 
        pose3d = np.array({'aria01': scene.aria_humans['aria01'].pose3d, 'aria02': scene.aria_humans['aria02'].pose3d}, dtype=object)
        save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        scene.save_poses3d(pose3d, save_path) ## save 3d poses

        # Visualize
        if args.vis:
            for (camera_name, camera_mode) in cameras:
                scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
                poses2d = scene.get_projected_poses3d()
                # input()
                ##-------------visualize the pose-------------------         
                ## skip cameras if not in vis list
                if scene.cfg.POSE3D.VIS_CAMERAS != [] and camera_name not in scene.cfg.POSE3D.VIS_CAMERAS:
                    continue

                save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
                scene.draw_projected_poses3d(poses2d, save_path)
            
    return


if __name__ == "__main__":  
    main()


