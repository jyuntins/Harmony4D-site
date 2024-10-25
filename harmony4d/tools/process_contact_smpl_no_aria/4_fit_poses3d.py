import _init_paths
import os
import argparse
from tqdm import tqdm

from datasets.exo_scene import EgoExoScene

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

    output_path = os.path.join(args.output_path, 'fit_poses3d') 
    vis_output_path = os.path.join(args.output_path, 'vis_fit_poses3d') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    ##-----------------poses 3d-----------------------
    scene.init_fit_pose3d() ## load all the 3d poses in memory
    scene.init_pose2d_rgb() ## for visualization

    poses3d_trajectory = scene.fit_poses3d() # human x time x pose3d

    ##-----------------visualize-----------------------
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = scene.total_time_refine_pose3d

    time_stamps = list(range(start_time, end_time + 1))

    ## save
    print('saving!')
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        poses3d = {human_name: poses3d_trajectory[human_name][t-1] for human_name in poses3d_trajectory.keys()}

        scene.set_poses3d(poses3d) ## set the pose3d to humans

        save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        scene.save_poses3d(poses3d, save_path) ## save 3d poses

    print('visualizing!')
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        poses3d = {human_name: poses3d_trajectory[human_name][t-1] for human_name in poses3d_trajectory.keys()}

        scene.set_poses3d(poses3d) ## set the pose3d to humans

        cameras = scene.exo_camera_names_with_mode 

        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            poses2d = scene.get_projected_poses3d()

            ##-------------visualize the pose-------------------    
            ## skip cameras if not in vis list
            if scene.cfg.FIT_POSE3D.VIS_CAMERAS != [] and camera_name not in scene.cfg.FIT_POSE3D.VIS_CAMERAS:
                continue

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_projected_poses3d(poses2d, save_path)


    print('done, start:{}, end:{} -- both inclusive!. sequence-len:{} secs'.format(start_time, end_time, scene.total_time/20.0))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()