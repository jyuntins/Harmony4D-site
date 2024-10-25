import os
import numpy as np
import quaternion
import joblib

from utils import axan_to_rot_matrix

def load_buddi_prediction(prediction_dir):

    predictions = {}

    for cam in os.listdir(prediction_dir):
        if not cam.startswith('cam'):
            continue
        pred_cam_dir = os.path.join(prediction_dir, cam)
        pred_file_path = os.path.join(pred_cam_dir, 'final_pred.npy')
        prediction = np.load(pred_file_path, allow_pickle=True).item()
        predictions[cam] = prediction

    return predictions


def load_multihmr_prediction(prediction_dir):

    predictions = {}

    for cam in os.listdir(prediction_dir):
        if not cam.startswith('cam'):
            continue
        pred_cam_dir = os.path.join(prediction_dir, cam)
        pred_file_path = os.path.join(pred_cam_dir, 'final_pred.npy')
        prediction = np.load(pred_file_path, allow_pickle=True).item()
        predictions[cam] = prediction

    return predictions


def load_pare_prediction(prediction_dir):

    predictions = {}

    for cam in os.listdir(prediction_dir):
        if not cam.startswith('cam'):
            continue
        pred_cam_dir = os.path.join(prediction_dir, cam)

        body_pose = []
        betas = []
        keypoints_2d = []
        camera_translations = []
        prediction = {}
                    
        for timestamp_file in sorted(os.listdir(pred_cam_dir)):
            if not timestamp_file.endswith('.pkl'):
                continue

            pred_file_path = os.path.join(pred_cam_dir, timestamp_file)
            prediction = joblib.load(pred_file_path)
            body_pose.append(prediction['pred_pose'])
            betas.append(prediction['pred_shape'])
            keypoints_2d.append(prediction['smpl_joints2d'][:, :24, :])
            camera_translations.append(prediction['pred_cam'])
        
        prediction = {'body_pose': body_pose, 'betas':betas, 'keypoints_2d': keypoints_2d, 'camera_translations': camera_translations}
        predictions[cam] = prediction

    return predictions

    
def load_bev_prediction(prediction_dir):
    
    predictions = {}

    for camera in sorted(os.listdir(prediction_dir)):
        if not camera.startswith('cam'):
            continue

        pred_cam_dir = os.path.join(prediction_dir, camera)

        camera_translations = []
        body_pose = []
        betas = []
        pj2d_org = []

        prediction = {}
        for timestamp_file in sorted(os.listdir(pred_cam_dir)):
            if not timestamp_file.endswith('.npz'):
                continue

            pred_file_path = os.path.join(pred_cam_dir, timestamp_file)
            pred = np.load(pred_file_path, allow_pickle=True)['results'].item()
            camera_translations.append(pred['cam'])

            pose_params = pred['smpl_thetas']
            pose_params = axan_to_rot_matrix(pose_params).reshape(-1,24,3,3).astype(np.float32)
            body_pose.append(pose_params)

            betas.append(pred['smpl_betas'][:, :10])
            pj2d_org.append(pred['pj2d_org'][:, :24, :])

        prediction['camera_translations'] = camera_translations
        prediction['body_pose'] = body_pose
        prediction['betas'] = betas
        prediction['keypoints_2d'] = pj2d_org
        predictions[camera] = prediction

    return predictions


def load_romp_prediction(prediction_dir):

    predictions = {}
    
    for camera in sorted(os.listdir(prediction_dir)):
        if not camera.startswith('cam'):
            continue

        pred_cam_dir = os.path.join(prediction_dir, camera)

        camera_translations = []
        body_pose = []
        betas = []
        pj2d_org = []
        prediction = {}
        for timestamp_file in sorted(os.listdir(pred_cam_dir)):
            if not timestamp_file.endswith('.npz'):
                continue

            pred_file_path = os.path.join(pred_cam_dir, timestamp_file)

            pred = np.load(pred_file_path, allow_pickle=True)['results'].item()

            camera_translations.append(pred['cam'])

            global_orient_params = pred['global_orient']
            pose_params = pred['body_pose']
            pose_params = np.concatenate((global_orient_params, pose_params), axis=1)
            pose_params = axan_to_rot_matrix(pose_params).reshape(-1,24,3,3).astype(np.float32)

            body_pose.append(pose_params)
            betas.append(pred['smpl_betas'])
            pj2d_org.append(pred['pj2d_org'][:, :24, :])

        prediction['body_pose'] = body_pose
        prediction['betas'] = betas
        prediction['camera_translations'] = camera_translations
        prediction['keypoints_2d'] = pj2d_org
        predictions[camera] = prediction
    return predictions


def load_hmr2_prediction(prediction_dir):

    imgW = 3840
    imgH = 2160

    predictions = {}
    openpose_to_smpl_order = [8,12,9,8,13,10,8,14,11,8,20,23,1,5,2,0,5,2,6,3,7,4,7,4]
    for cam in os.listdir(prediction_dir):
        if not cam.startswith('cam'):
            continue
        pred_cam_dir = os.path.join(prediction_dir, cam)

        body_pose = []
        betas = []
        keypoints_2d = []
        camera_translations = []
        prediction = {}
                    
        for timestamp_file in sorted(os.listdir(pred_cam_dir)):
            if not timestamp_file.endswith('.npy'):
                continue
            pred_file_path = os.path.join(pred_cam_dir, timestamp_file)
            prediction = np.load(pred_file_path, allow_pickle=True).item()

            global_orient_params = prediction['pred_smpl_params']['global_orient'].cpu().numpy()
            pose_params = prediction['pred_smpl_params']['body_pose'].cpu().numpy()
            body_pose_params = np.concatenate((global_orient_params, pose_params), axis=1)
            body_pose.append(body_pose_params)

            betas.append(prediction['pred_smpl_params']['betas'].cpu().numpy())

            j2d = np.array([keypoint_2d.cpu().numpy() for keypoint_2d in prediction['2d_keypoints']])
            j2d = j2d[:, :24, :]
            j2d = j2d[:, openpose_to_smpl_order, :]
            keypoints_2d.append(j2d)
            camera_translations.append(prediction['cam_t_full'])
        
        prediction = {'body_pose': body_pose, 'betas':betas, 'keypoints_2d': keypoints_2d, 'camera_translations': camera_translations}
        predictions[cam] = prediction

    return predictions



'''
\textbf{Method}    & \textbf{MPJPE} & \textbf{PAMPJPE} &  \textbf{NMJE} & \textbf{MPVPE} & \textbf{PAMPVPE} &\textbf{NMVE} & \textbf{3DPCK} & \textbf{AUC} & \textbf{F1} & \textbf{Max Depth Penetration}\\
\midrule
\textbf{HMR2.0}    & 108.93         & \r60.40          & \r111.16       & 127.39         & \r67.95          & \r130.00     & 71.12          & 0.48         & \r0.98      & N/A  \\
\textbf{PARE}      & 115.04         & 65.29            & 122.38         & 135.13         & 75.22            & 143.76       & 68.71          & 0.45         & 0.94        & N/A  \\
\textbf{Buddi}     & 146.83         & \bl102.08        & 156.21         & \bl192.06      & \bl118.20        & 204.32       & 61.01          & 0.39         & 0.94        & 95.47 \\
\textbf{BEV}       & 131.53         & 93.75            & 144.54         & 163.26         & 109.11           & 179.41       & 65.63          & 0.42         & 0.91        & \bl135.59  \\
\textbf{ROMP}      & \bl152.98      & 95.80            & \bl182.11      & 191.71         & 108.83           & \bl228.24    & \bl58.31       & \bl0.38      & 0.84        & N/A  \\
\textbf{Multi-HMR} & \h106.25       & 68.96            & 132.81         & \r124.31       & 78.12            & 155.39       & \r76.44        & \r0.51       & \bl0.8      & \r18.28  \\
'''