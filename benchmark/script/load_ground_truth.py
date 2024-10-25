import os
import numpy as np
from utils import homogeneous
import pickle

##################################################################3
###     This is the file used to load the ground truth data
###     The format of the ground truth data is showed below: 
###   
###     ground_truth
###     ├── cam01 
###     │   ├── aria01
###     │   │   ├── timestamp 
###     │   │   │   ├── global_orient
###     │   │   │   ├── transl
###     │   │   │   ├── body_pose
###     │   │   │   ├── betas
###     │   │   │   ├── vertices
###     │   │   │   ├── joints
###     │   │   │   ├── cam_smpl_vertices
###     │   │   │   ├── cam_3d_joints
###     │   │   │   ├── 2d_joints
###     │   ├── aria02
###     │   │   ├── timestamp
###     │   │   │   ├── global_orient
###     │   │   │   ├── transl
###     │   │   │   ├── body_pose
###     │   │   │   ├── betas
###     │   │   │   ├── vertices
###     │   │   │   ├── joints
###     │   │   │   ├── cam_smpl_vertices
###     ├── cam02
###     │   ├── aria01
###     │   │   └── ...
###     │   ├── aria02
###     │   │   └── ...
###     └── ...
###
###
##################################################################3

def load_2d_joints(ground_truth_dir):
    ### 2djoints in format 2d_joiints[cam][aria][timestamp -1][joints]
    joints2d_dir = os.path.join(ground_truth_dir, 'smpl_2d_joints')
    joints2ds = {}
    for cam in sorted(os.listdir(joints2d_dir)):
        if not cam.startswith('cam'):
            continue

        cam_joints2d_dir = os.path.join(joints2d_dir, cam)
        total_time_joints2d = len([file for file in os.listdir(cam_joints2d_dir) if file.endswith('npy')])
        aria1_joints2d = np.zeros((total_time_joints2d, 24, 2))
        aria2_joints2d = np.zeros((total_time_joints2d, 24, 2))

        for timestamp, file in enumerate(sorted(os.listdir(cam_joints2d_dir))):
            joints2d_path = os.path.join(cam_joints2d_dir, file)
            aria1_joints2d[timestamp] = np.load(joints2d_path, allow_pickle=True).item()['aria01']
            aria2_joints2d[timestamp] = np.load(joints2d_path, allow_pickle=True).item()['aria02']

        joints2ds[cam] = {'aria01': aria1_joints2d, 'aria02': aria2_joints2d}        

    return joints2ds


def load_extrinsics(ground_truth_dir):
    ### return extrinscis in format of {cam: extrinsics}
    ### extrinsics: np.array of shape (total_time_extrinsic, 4, 4)
    extrinsics_dir = os.path.join(ground_truth_dir, 'extrinsics')
    extrinsics = {}
    for cam in sorted(os.listdir(extrinsics_dir)):
        if not cam.startswith('cam'):
            continue

        cam_extrinsic_dir = os.path.join(extrinsics_dir, cam)
        total_time_extrinsic = len([file for file in os.listdir(cam_extrinsic_dir) if file.endswith('npy')])
        cam_extrinsics = np.zeros((total_time_extrinsic, 4, 4))
        for timestamp, file in enumerate(sorted(os.listdir(cam_extrinsic_dir))):
            extrinsic_path = os.path.join(cam_extrinsic_dir, file)
            cam_extrinsics[timestamp] = np.load(extrinsic_path, allow_pickle=True)
            
        extrinsics[cam] = cam_extrinsics

    return extrinsics

def load_ground_truth(ground_truth_dir):
    ### return ground truth: smpl vetices, cam_smpl_vertices, 3d_joints, cam_3d_joints, 2d_joints 
    ### ground truth format: ground_truth[cam][human_name][time_stamp-1][vertices]
    # load extrinsics to convert 3d joints and smpl vertices to camera coordinate
    big_sequence=ground_truth_dir.split('/')[-3]
    sequence=ground_truth_dir.split('/')[-2]
    colmap_dir = os.path.join(ground_truth_dir, '../../../../../', big_sequence, sequence, 'colmap', 'workplace')

    # scale = 1.3835045
    scale = compute_scale(colmap_dir)
    extrinsics = load_extrinsics(ground_truth_dir)
    joints_2ds = load_2d_joints(ground_truth_dir)

    # load smpl
    smpl_path = os.path.join(ground_truth_dir, 'smpl')
    smpl_collision_path = os.path.join(ground_truth_dir, 'smpl_collision')
    if os.path.exists(smpl_collision_path):
        smpl_dir = smpl_collision_path
        # smpl_dir = smpl_path

    else:
        smpl_dir = smpl_path

    total_time_smpl = len([file for file in os.listdir(smpl_dir) if file.endswith('npy')])
    time_stamps = list(range(1, total_time_smpl + 1))
    aria_human_names = ['aria01', 'aria02']
    gt_smpls_trajectory = {}

    for cam in sorted(os.listdir(os.path.join(ground_truth_dir,'..', 'exo'))):
        if not cam.startswith('cam'):
            continue

        smpls_trajectory = {aria_human_name:[] for aria_human_name in aria_human_names}       
        for time_stamp in time_stamps:
            smpl_path = os.path.join(smpl_dir, '{:05d}.npy'.format(time_stamp))
            smpls = np.load(smpl_path, allow_pickle=True).item()
            for aria_human_name in smpls.keys():
                if aria_human_name in aria_human_names:
                    cam_smpl_vertices = scale * extrinsics[cam][time_stamp-1] @ homogeneous(smpls[aria_human_name]['vertices']).T # 4 x 6890
                    cam_3d_joints = scale * extrinsics[cam][time_stamp-1] @ homogeneous(smpls[aria_human_name]['joints'][:, :]).T # 4 x 24
                    # cam_3d_joints = compute_3d_joint(smpls[aria_human_name]['joints'], extrinsics[cam][time_stamp-1], colmap_dir)
                    smpls[aria_human_name]['cam_smpl_vertices'] = cam_smpl_vertices[:3, :].T
                    smpls[aria_human_name]['cam_3d_joints'] = cam_3d_joints[:3, :].T
                    smpls[aria_human_name]['2d_joints'] = joints_2ds[cam][aria_human_name][time_stamp-1]

                    smpls_trajectory[aria_human_name].append(smpls[aria_human_name]) ## dict_keys(['global_orient', 'transl', 'body_pose', 'betas', 'epoch_loss', 'vertices', 'joints'])

        gt_smpls_trajectory[cam] = smpls_trajectory

    return gt_smpls_trajectory

def compute_3d_joint(smpl_joints, extrinsics, colmap_dir):
    # scale is the scale from colmap coordinate to metric coordinate
    if os.path.exists(os.path.join(colmap_dir, 'scale.npy')):
        transform = np.load(os.path.join(colmap_dir, 'scale.npy'))
        raw_extrinsics = extrinsics @ transform
        scale = np.linalg.norm(transform[0, :3])

        # rotation_temp = transform[:3, :3]/scale
        # rotation = np.eye(4)
        # rotation[:3, :3] = rotation_temp
        # translation = np.linalg.solve(rotation_temp*scale, transform[:3, 3])
        # metric_translation = np.eye(4)
        # metric_translation[:3, 3] = translation
        # inverse_metric_translation = np.linalg.inv(metric_translation)
        # inverse_metric_translation[:3, 3] = inverse_metric_translation[:3, 3]*scale

        # extrinsics_rotation = np.eye(4)
        # extrinsics_rotation[:3, :3] = raw_extrinsics[:3, :3]

        # extrinsics_translation = raw_extrinsics[:3, 3]  
        # metric_extrinsics_translation = np.eye(4)
        # metric_extrinsics_translation[:3, 3] = extrinsics_translation
        # metric_extrinsics_translation[:3, 3] = metric_extrinsics_translation[:3, 3]*scale
        
        # cam_3d_joints = metric_extrinsics_translation @ extrinsics_rotation @ inverse_metric_translation @ np.linalg.inv(rotation) @ homogeneous(smpl_joints).T
        # breakpoint()
        inv_transform = np.linalg.inv(transform)
        scale_matrix = np.eye(4)
        scale_matrix[:3, :3] = np.eye(3)*scale
        
        # cam_3d_joints = scale_matrix @ raw_extrinsics @ inv_transform @ homogeneous(smpl_joints).T
        scaled_raw_extrinsics = scale_matrix.copy()
        scaled_raw_extrinsics[:3,3] = scaled_raw_extrinsics[:3,3]*scale
        cam_3d_joints = scale_matrix @ raw_extrinsics @  inv_transform @ homogeneous(smpl_joints).T

        breakpoint()
        return cam_3d_joints
        # breakpoint()


def compute_scale(colmap_dir):
    if os.path.exists(os.path.join(colmap_dir, 'scale.npy')):
        transform = np.load(os.path.join(colmap_dir, 'scale.npy'))
        scale = np.linalg.norm(transform[0, :3])
        return scale

    else:
        colmap_transforms_file = os.path.join(colmap_dir, 'aria_from_colmap_transforms.pkl') 
        with open(colmap_transforms_file, 'rb') as handle:
            colmap_from_aria_transforms = pickle.load(handle)
        transforms = colmap_from_aria_transforms['aria01']
        scale = np.linalg.norm(transforms[0, :3])
        # breakpoint()
        return scale
