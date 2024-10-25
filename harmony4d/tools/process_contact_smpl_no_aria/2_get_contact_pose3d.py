import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config

from models.pose_motion_model import PoseMotionModel

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    parser.add_argument('--motion_model_window_size', default=10, help='motion model window size')
    parser.add_argument('--override_contact_segpose3d', default=False, help='override_contact_segpose3d')
    
    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'contact_poses3d') 
    poses3d_output_path = os.path.join(args.output_path, 'poses3d')
    vis_output_path = os.path.join(args.output_path, 'vis_contact_poses3d') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    vis_segmentation_output_path = os.path.join(args.output_path, 'vis_segmentation')
    vis_kf_poses3d_output_path = os.path.join(args.output_path, 'vis_kf_poses3d')
    vis_segpose2d_output_path = os.path.join(args.output_path, 'vis_segposes2d')
    os.makedirs(vis_segmentation_output_path, exist_ok=True)
    os.makedirs(vis_kf_poses3d_output_path, exist_ok=True)
    os.makedirs(vis_segpose2d_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    ##-----------------poses 3d-----------------------
    scene.init_refine_pose3d(override_contact_segpose3d=args.override_contact_segpose3d)
    scene.init_segmentation()
    scene.init_segpose2d() 
    ## init pose motion model
    pose_motion_models = {human_name: PoseMotionModel(num_keypoints=17) for human_name in scene.aria_human_names}

    for human_name in scene.aria_human_names:
        if len(scene.aria_humans[human_name].poses3d_trajectory) < scene.total_time:

            print('adding residual poses3d for {}'.format(human_name))
            residual_len = scene.total_time - len(scene.aria_humans[human_name].poses3d_trajectory)
            residual = np.zeros((residual_len, 17, 4))
            residual[:, :, 3] = 1
            scene.aria_humans[human_name].poses3d_trajectory = np.vstack([scene.aria_humans[human_name].poses3d_trajectory, residual])

    ## init the pose motion model with the first 10 frames or if start_time is specified, then the first 10 frames after start_time
    motion_model_window_size = int(args.motion_model_window_size)
    window_start = max(0, int(args.start_time) - 1 - motion_model_window_size)
    window_end = window_start + motion_model_window_size
    for human_name in scene.aria_human_names:
        pose3d_trajectory_window = scene.aria_humans[human_name].poses3d_trajectory[window_start:window_end, :, :3] ## size 10, from t = 1 to 10, index 0 to 9,
        ## start_time = 130 mean index 119 to 128 (means time 120 to 129)
        pose_motion_models[human_name].train(pose3d_trajectory_window)

    ##-----------------visualize-----------------------
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)
    
    if end_time == -1:
        end_time = scene.total_time

    time_stamps = list(range(start_time, end_time + 1))
    ## save
    print('saving!')
    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        ## for t=1 to 10, we do not have the motion model yet
        ##---------------------------------------------------------------------------        
        kf_poses3d = {}
        if t > motion_model_window_size:
            ## obtain the pose at timestep t from the motion model (as t is 1-indexed, index is t-1)
            for human_name in scene.aria_human_names:
                pose3d = scene.aria_humans[human_name].poses3d_trajectory[t-2] ## t is 1-indexed, 17 x 4 - x,y,z,vis
                predicted_pose = pose_motion_models[human_name].predict_next_pose(pose3d[:, :3]) ## 17 x 3, at timestep t, index is t-1

                ## contentate the vis, 4th dim, it is all 1s
                predicted_pose = np.concatenate([predicted_pose, pose3d[:, 3:]], axis=1) ## 17 x 4
                kf_poses3d[human_name] = predicted_pose ## pose at timestep t, index is t-1
        else:
            for human_name in scene.aria_human_names:
                kf_poses3d[human_name] = scene.aria_humans[human_name].poses3d_trajectory[t-1] ## t is 1-indexed, 17 x 4 - x,y,z,vis

        scene.set_poses3d(kf_poses3d) ## set the kf_pose3d to humans
        cameras = scene.exo_camera_names_with_mode 

        ##---------------------------------------------------------------------------        
        ## obtain segmentations, then segmentation conditioned poses2d, visualize!
        segposes2d = {}
        segmentations = {}
        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            segmentation = scene.get_segmentation() ## using kf_pose3d
            segpose2d = scene.get_segposes2d(segmentations=segmentation)
            segposes2d[(camera_name, camera_mode)] = segpose2d
            segmentations[(camera_name, camera_mode)] = segmentation

        ##---------------------------------------------------------------------------
        ## triangulate the segmentation conditioned poses2d to obtain the poses3d
        poses3d = scene.triangulate(flag='exo', secondary_flag=None, debug=True, pose2d=segposes2d)   
        scene.set_poses3d(poses3d) ## set the pose3d to humans

        ## save the poses3d to disk
        save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        scene.save_poses3d(poses3d, save_path) ## save 3d poses

        ## also save to poses3d to disk, to load better
        if t > motion_model_window_size:
            save_path = os.path.join(poses3d_output_path, '{:05d}.npy'.format(t))
            scene.save_poses3d(poses3d, save_path) ## save 3d poses

        ## update the pose_trajectory to be used by the motion model
        for human_name in scene.aria_human_names:
            scene.aria_humans[human_name].poses3d_trajectory[t-1] = poses3d[human_name] ## as t is 1-indexed, index is t-1

        ##---------------------------------------------------------------------------
        ## visualization
        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            poses2d = scene.get_projected_poses3d()  

            ##-------------visualize the pose-------------------         
            ## skip cameras if not in vis list
            if scene.cfg.POSE3D.VIS_CAMERAS != [] and camera_name not in scene.cfg.POSE3D.VIS_CAMERAS:
                continue
            
            ## visualize poses3d
            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_projected_poses3d(poses2d, save_path)
        
        
        ## update the pose motion model if t is greated than the start window size
        if t > motion_model_window_size:
            window_start += 1
            window_end += 1
            for human_name in scene.aria_human_names:
                pose3d_trajectory_window = scene.aria_humans[human_name].poses3d_trajectory[window_start:window_end, :, :3]
                pose_motion_models[human_name].train(pose3d_trajectory_window)

    print('done, start:{}, end:{} -- both inclusive!. sequence-len:{} secs'.format(start_time, end_time, scene.total_time/20.0))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()