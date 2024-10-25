import _init_paths
import os
import argparse
from tqdm import tqdm
import numpy as np
from datasets.ego_exo_scene import EgoExoScene

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

    output_path = os.path.join(args.output_path, 'extrinsics') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)

    if end_time == -1:
        end_time = len([file for file in os.listdir(scene.fit_pose3d_dir) if file.endswith('npy')])

    ## we start with t=1
    time_stamps = list(range(start_time, end_time + 1)) 

    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        for (camera_name, camera_mode) in scene.camera_names:

            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            save_dir = os.path.join(output_path, scene.viewer_name)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}'.format(t))
            np.save(save_path, scene.view_camera.extrinsics, allow_pickle=True)
            # print(scene.view_camera.intrinsics)
            # input()
    print('done, start:{}, end:{} -- both inclusive!'.format(start_time, end_time))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()