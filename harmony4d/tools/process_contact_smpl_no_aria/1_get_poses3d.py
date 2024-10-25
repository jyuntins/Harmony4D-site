import _init_paths
import os
import argparse
from tqdm import tqdm

from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config
import numpy as np
import cv2
import trimesh

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    parser.add_argument('--choosen_time', default="", help='choosen time')
    parser.add_argument('--override_segpose2d_load', default=False, help='override_segpose2d_load')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'poses3d') 
    vis_output_path = os.path.join(args.output_path, 'vis_poses3d') 
    print('sequence at {}'.format(sequence_path))

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(vis_output_path, exist_ok=True)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    scene.init_pose3d(override_segpose2d_load=args.override_segpose2d_load)
    scene.init_pose2d_rgb(dummy=True)
    
    ## we start with t=1
    start_time = int(args.start_time)
    end_time = int(args.end_time)

    if start_time != -1:
        if end_time == -1:
            end_time = scene.total_time_pose2d  

        time_stamps = list(range(start_time, end_time + 1))

    else:
        assert(args.choosen_time != '')
        time_stamps = [int(val) for val in args.choosen_time.split(':')]


    for t in tqdm(time_stamps):
        scene.update(time_stamp=t)

        poses3d = scene.triangulate(flag='exo', secondary_flag=None, debug=True)

        for human_name, pose3d in poses3d.items():
            # Define limbs based on keypoints
            limbs = {
                'left_upper_arm': (pose3d[5], pose3d[7]),  # Left shoulder to left elbow
                'right_upper_arm': (pose3d[6], pose3d[8]),  # Right shoulder to right elbow
                'left_forearm': (pose3d[7], pose3d[9]),    # Left elbow to left wrist
                'right_forearm': (pose3d[8], pose3d[10]),   # Right elbow to right wrist
                'left_thigh': (pose3d[11], pose3d[13]),   # Left hip to left knee
                'right_thigh': (pose3d[12], pose3d[14]),   # Right hip to right knee
                'left_lower_leg': (pose3d[13], pose3d[15]), # Left knee to left ankle
                'right_lower_leg': (pose3d[14], pose3d[16]) # Right knee to right ankle
            }

            # Calculate total height (approximation)
            mid_head = [(pose3d[1][i] + pose3d[2][i]) / 2 for i in range(3)]
            mid_shoulder = [(pose3d[5][i] + pose3d[6][i]) / 2 for i in range(3)]
            mid_hip = [(pose3d[11][i] + pose3d[12][i]) / 2 for i in range(3)]
            head_to_shoulder = sum((mid_head[i] - mid_shoulder[i])**2 for i in range(3))**0.5
            shoulder_to_hip = sum((mid_shoulder[i] - mid_hip[i])**2 for i in range(3))**0.5
            leg_length_left = sum((pose3d[11][i] - pose3d[15][i])**2 for i in range(3))**0.5
            leg_length_right = sum((pose3d[12][i] - pose3d[16][i])**2 for i in range(3))**0.5
            longer_leg_length = max(leg_length_left, leg_length_right)
            total_height = head_to_shoulder + shoulder_to_hip + longer_leg_length
            total_height_inches = total_height * 39.3701  # Convert to inches
            # print(total_height)
            # input()
            # Additional limb and body part definitions
            total_left_hand = sum(((pose3d[5][i] - pose3d[7][i])**2 for i in range(3)))**0.5 + \
                            sum(((pose3d[7][i] - pose3d[9][i])**2 for i in range(3)))**0.5
            total_right_hand = sum(((pose3d[6][i] - pose3d[8][i])**2 for i in range(3)))**0.5 + \
                            sum(((pose3d[8][i] - pose3d[10][i])**2 for i in range(3)))**0.5
            chest_length = sum(((pose3d[5][i] - pose3d[6][i])**2 for i in range(3)))**0.5

            # Convert additional measurements to inches
            total_left_hand_inches = total_left_hand * 39.3701
            total_right_hand_inches = total_right_hand * 39.3701
            chest_length_inches = chest_length * 39.3701

            height_feet = int(total_height_inches // 12)
            height_inches_remainder = total_height_inches % 12
            print(f'time: {t}, human: {human_name}, total height: {height_feet} feet {height_inches_remainder:.2f} inches')

            for limb_name, (point1, point2) in limbs.items():
                length_inches = sum((point1[i] - point2[i])**2 for i in range(3))**0.5 * 39.3701
                limb_feet = int(length_inches // 12)
                limb_inches_remainder = length_inches % 12
                print(f'  {limb_name}: {limb_feet} feet {limb_inches_remainder:.2f} inches')
            
            # Print additional measurements
            print(f'  Total left hand length: {int(total_left_hand_inches // 12)} feet {total_left_hand_inches % 12:.2f} inches')
            print(f'  Total right hand length: {int(total_right_hand_inches // 12)} feet {total_right_hand_inches % 12:.2f} inches')
            print(f'  Chest length: {int(chest_length_inches // 12)} feet {chest_length_inches % 12:.2f} inches')
        
        save_dir = vis_output_path
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
        scene.set_poses3d(poses3d) ## set the pose3d to humans

        save_path = os.path.join(output_path, '{:05d}.npy'.format(t))
        scene.save_poses3d(poses3d, save_path) ## save 3d poses

        cameras = scene.exo_camera_names_with_mode 
        
        for (camera_name, camera_mode) in cameras:
            scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
            poses2d = scene.get_projected_poses3d()

            ##-------------visualize the pose-------------------         
            ## skip cameras if not in vis list
            if scene.cfg.POSE3D.VIS_CAMERAS != [] and camera_name not in scene.cfg.POSE3D.VIS_CAMERAS:
                continue

            save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
            scene.draw_projected_poses3d(poses2d, save_path)
        

        # if t % 4 == 0:
        #     # Visualization parameters
        #     joint_radius = 0.05  # Adjust based on your data scale

        #     trimesh_scene = trimesh.Scene()
        #     # Add joints to the scene
        #     for point in poses3d['aria01']:
        #         joint_geometry = trimesh.creation.uv_sphere(radius=joint_radius)
        #         joint_geometry.apply_translation(point[:3])
        #         trimesh_scene.add_geometry(joint_geometry)

        #     # Visualization parameters for axes
        #     axis_length = 1.0
        #     axis_radius = 0.03

        #     # Rotation matrices for aligning the cylinders with X and Y axes
        #     rotation_matrix_x = trimesh.transformations.rotation_matrix(
        #         np.radians(90), [0, 1, 0])  # Rotate 90 degrees around Y
        #     rotation_matrix_y = trimesh.transformations.rotation_matrix(
        #         np.radians(-90), [1, 0, 0])  # Rotate -90 degrees around X

        #     # X-axis (red)
        #     x_axis = trimesh.creation.cylinder(radius=axis_radius, height=axis_length)
        #     x_axis.apply_transform(rotation_matrix_x)
        #     x_axis.apply_translation([axis_length / 2, 0, 0])
        #     x_axis.visual.face_colors = [255, 0, 0, 255]
        #     trimesh_scene.add_geometry(x_axis)

        #     # Y-axis (green)
        #     y_axis = trimesh.creation.cylinder(radius=axis_radius, height=axis_length)
        #     y_axis.apply_transform(rotation_matrix_y)
        #     y_axis.apply_translation([0, axis_length / 2, 0])
        #     y_axis.visual.face_colors = [0, 255, 0, 255]
        #     trimesh_scene.add_geometry(y_axis)

        #     # Z-axis (blue) - No rotation needed as it's aligned with the Z-axis by default
        #     z_axis = trimesh.creation.cylinder(radius=axis_radius, height=axis_length)
        #     z_axis.apply_translation([0, 0, axis_length / 2])
        #     z_axis.visual.face_colors = [0, 0, 255, 255]
        #     trimesh_scene.add_geometry(z_axis)

        #     # Show the scene
        #     trimesh_scene.show()

    print('done, start:{}, end:{} -- both inclusive!. sequence-len:{} secs'.format(start_time, end_time, scene.total_time/20.0))

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()