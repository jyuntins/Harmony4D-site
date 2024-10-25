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
    parser.add_argument('--vis_cams', type=str, default='', help='camera to visualize')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'smpl_bbox') 
    vis_output_path = os.path.join(args.output_path, 'vis_smpl_bbox') 
    print('sequence at {}'.format(sequence_path))

    vis_cams = [val for val in args.vis_cams.split('---')]

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    ##-----------------------------------------------------
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = len([file for file in os.listdir(scene.fit_pose3d_dir) if file.endswith('npy')])

    ## we start with t=1
    time_stamps = list(range(start_time, end_time + 1)) 
    scene.load_smpl()
    for t in tqdm(time_stamps):
        if vis_cams != ['']:
            print('visualizing time_stamp:{}'.format(t))

        scene.update(time_stamp=t)

        cameras = scene.exo_camera_names_with_mode 

        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)

            smpl = {'aria01': scene.aria_humans['aria01'].smpl, 'aria02': scene.aria_humans['aria02'].smpl}
            bboxes = {}
            for human_name in smpl.keys():
                smpl_human = smpl[human_name]

                points_3d = smpl_human['vertices']
                points_2d = scene.view_camera.vec_project(points_3d) # mask
                x1 = round(points_2d[:, 0].min())
                x2 = round(points_2d[:, 0].max())
                y1 = round(points_2d[:, 1].min())
                y2 = round(points_2d[:, 1].max())
                bboxes[human_name] = np.array([x1, y1, x2, y2])

            save_dir = os.path.join(output_path, scene.viewer_name)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.npy'.format(t))
            np.save(save_path, bboxes, allow_pickle=True)
            ##-------------visualize the pose-------------------         

            if camera_name not in vis_cams:
                continue

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_smpl_bboxes(bboxes, save_path)
    print('done, start:{}, end:{} -- both inclusive!'.format(start_time, end_time))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()