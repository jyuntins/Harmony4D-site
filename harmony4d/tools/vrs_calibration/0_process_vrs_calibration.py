import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import cv2
import ast
import pandas as pd

# https://github.com/facebookresearch/vrs/blob/f1d97cebcf4b5d4e7082c3080503f9440bf8c738/vrs/utils/DataExtractorReadMe.hpp

## Reference for trajectory: https://projectaria.com/docs#/en/0.1.0/mps/Trajectory.md
## Referecen to read the online calibration.jsonl: https://projectaria.com/docs#/en/0.1.0/mps/Trajectory.md

###------------------------------------------------------
def quaternion_rotation_matrix(Q):
    """
    https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/
    Convert a quaternion into a full three-dimensional rotation matrix.
 
    Input
    :param Q: A 4 element array representing the quaternion (q0,q1,q2,q3) 
 
    Output
    :return: A 3x3 element matrix representing the full 3D rotation matrix. 
             This rotation matrix converts a point in the local reference 
             frame to a point in the global reference frame.
    """
    # Extract the values from Q
    q0 = Q[0]
    q1 = Q[1]
    q2 = Q[2]
    q3 = Q[3]
     
    # First row of the rotation matrix
    r00 = 2 * (q0 * q0 + q1 * q1) - 1
    r01 = 2 * (q1 * q2 - q0 * q3)
    r02 = 2 * (q1 * q3 + q0 * q2)
     
    # Second row of the rotation matrix
    r10 = 2 * (q1 * q2 + q0 * q3)
    r11 = 2 * (q0 * q0 + q2 * q2) - 1
    r12 = 2 * (q2 * q3 - q0 * q1)
     
    # Third row of the rotation matrix
    r20 = 2 * (q1 * q3 - q0 * q2)
    r21 = 2 * (q2 * q3 + q0 * q1)
    r22 = 2 * (q0 * q0 + q3 * q3) - 1
     
    # 3x3 rotation matrix
    rot_matrix = np.array([[r00, r01, r02],
                           [r10, r11, r12],
                           [r20, r21, r22]])
                            
    return rot_matrix



##-------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Process vrs calibration data')
    parser.add_argument('--trajectory_dir', action='store', help='trajectory directory of the vrs file')
    parser.add_argument('--images_dir', action='store', help='image directory of the extracted')
    parser.add_argument('--vrs_calib_dir', action='store', help='calibration directory of the vrs')

    args = parser.parse_args()

    TRAJECTORY_FILE = os.path.join(args.trajectory_dir, 'closed_loop_trajectory.csv')
    CALIBRATION_FILE = os.path.join(args.trajectory_dir, 'online_calibration.jsonl')
    ALL_IMAGE_DIR = args.images_dir ## contains 214-1 (rgb), 1201-1 (left), 1201-2 (right)
    SAVE_DIR = args.vrs_calib_dir

    ###------------------------------------------------------
    RGB_IMAGE_DIR = os.path.join(ALL_IMAGE_DIR, '214-1')
    LEFT_IMAGE_DIR = os.path.join(ALL_IMAGE_DIR, '1201-1')
    RIGHT_IMAGE_DIR = os.path.join(ALL_IMAGE_DIR, '1201-2')

    HEADER = 'Serial, intrinsics (radtanthinprsim), extrinsic (3x4)' + '\n'
    SECOND_HEADER = 'aria' + '\n'

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    ##-------------read camera calibration tranforms---------------------------------
    ##-------------per timestamp, the transforms to jump from device to the sensor frame---------------------------------
    ##-------------- sensor can be: camera-slam-left, camera-slam-right, camera-rgb-----------------------------------
    calibration_data = {}

    with open(CALIBRATION_FILE, "r") as f:
        data = f.readlines()

    for line_idx in tqdm(range(len(data))):
        line = json.loads(data[line_idx])
        timestamp = int(line['tracking_timestamp_us']) ## in microseconds
        calibration = line['CameraCalibrations']

        ## if type of calibration is string, convert to list of dictionary
        if type(calibration) == str:
            calibration = ast.literal_eval(calibration)

        camera_info = {}

        for camera_calibration in calibration:
            if camera_calibration['Calibrated'] == False:
                continue
            
            label = camera_calibration['Label']
            camera_type = label.replace('camera-slam-', '').replace('camera-', '')

            intrinsics = np.array(camera_calibration['Projection']['Params']) ## 15 params
            translation = np.array(camera_calibration['T_Device_Camera']['Translation'])

            rotation_info = camera_calibration['T_Device_Camera']['UnitQuaternion']
            quat_w = rotation_info[0]
            quat_rot = rotation_info[1]
            rotation_quaternion = np.array([quat_w, quat_rot[0], quat_rot[1], quat_rot[2]])
            rotation = quaternion_rotation_matrix(rotation_quaternion)

            extrinsics = np.concatenate([rotation, translation.reshape(-1, 1)], axis=1) ## 3 x 4 
            extrinsics = np.concatenate([extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4, sensor from device coordinate system

            inv_extrinsics = np.linalg.inv(extrinsics)

            ## Note, extrinsics, is the transform to go from device frame to sensor!
            camera_info[camera_type] = {'intrinsics': intrinsics, 'translation': translation, 'rotation': rotation, 'extrinsics': inv_extrinsics} 

        calibration_data[timestamp] = camera_info

    ##-------------read closed_loop_trajectory.csv---------------------------------
    ##--------------device pose in world coordinates----------------------
    trajectory_data = {}
    df = pd.read_csv(TRAJECTORY_FILE)

    for i in range(len(df)):
        timestamp = df.loc[i, 'tracking_timestamp_us']
        
        tx = df.loc[i, 'tx_world_device']
        ty = df.loc[i, 'ty_world_device']
        tz = df.loc[i, 'tz_world_device']
        translation = np.array([tx, ty, tz])

        qx = df.loc[i, 'qx_world_device']
        qy = df.loc[i, 'qy_world_device']
        qz = df.loc[i, 'qz_world_device']
        qw = df.loc[i, 'qw_world_device']
        quaternion = np.array([qw, qx, qy, qz])
        rotation  = quaternion_rotation_matrix(quaternion)

        ###------------------version 1-------------------------------------
        # https://math.stackexchange.com/questions/82602/how-to-find-camera-position-and-rotation-from-a-4x4-matrix
        ## So assuming the translation and rotation is the device's position and pose in the world coordinates
        ## It is not the world to device transform. So we compute the transforms as follows
        ## translation is camera center C, rotation is rotation.T

        ## pose_rotation = rotation.T
        ## pose_translation = -rotation.T * translation

        ## rotation = pose_rotation.T
        ## translation = -rotation * pose_translation = -pose_rotation.T * pose_translation

        pose_rotation = rotation.copy()
        pose_translation = translation.copy()

        rotation = pose_rotation.T ## world to device coordinate system
        translation = -1*np.dot(pose_rotation.T, pose_translation)

        extrinsics = np.concatenate([rotation, translation.reshape(-1, 1)], axis=1) ## 3 x 4 
        extrinsics = np.concatenate([extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4, sensor from device coordinate system

        # import pdb; pdb.set_trace()
        # temp_extrinsics = np.concatenate([pose_rotation, pose_translation.reshape(-1, 1)], axis=1)
        # temp_extrinsics = np.concatenate([temp_extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4, sensor from device coordinate system
        # check = np.dot(extrinsics, temp_extrinsics)

        trajectory_data[timestamp] = {'translation': translation, 'rotation': rotation, 'extrinsics': extrinsics}

    ###------------------------------------------------------------------------------------------------
    camera_timestamps = np.array(list(calibration_data.keys()))
    imu_timestamps = np.array(list(trajectory_data.keys()))

    valid_timestamps = [timestamp for timestamp in camera_timestamps if timestamp in imu_timestamps]

    image_timestamps = {}
    _image_timestamps = sorted([name.replace('.jpg', '').replace('214-1-', '') for name in os.listdir(RGB_IMAGE_DIR) if name.endswith('.jpg')])
    for image_timestamp in _image_timestamps:
        timestamp = float(image_timestamp.split('-')[-1])
        image_timestamps[timestamp] = image_timestamp

    ###------------------------------------------------------------------------------------------------
    ## match nearest neighbour timestamp to the trajectory
    for i, timestamp in enumerate(valid_timestamps):
        timestamp_in_seconds = round(timestamp/1e6, 3) ## to match the image_stamps which are in seconds

        if timestamp_in_seconds in image_timestamps.keys():
            save_name = image_timestamps[timestamp_in_seconds]
        else:
            dist = (np.array(list(image_timestamps.keys())) - timestamp_in_seconds)**2
            idx = dist.argmin()
            nn_timestamp_in_seconds = list(image_timestamps.keys())[idx]
            print('exact match not found for t:{}, using nn:{}'.format(timestamp_in_seconds, nn_timestamp_in_seconds))
            save_name = image_timestamps[nn_timestamp_in_seconds]

        save_path = os.path.join(SAVE_DIR, '{}.txt'.format(save_name))

        device_from_world_extrinsics = trajectory_data[timestamp]['extrinsics'] ## 4 x 4

        ## rgb
        rgb_intrinsics = calibration_data[timestamp]['rgb']['intrinsics'] ## 15
        rgb_intrinsics[:3] = rgb_intrinsics[:3] / 2 ## the factory rgb intrinsics are not matching with UVP directly. Do this transform
        rgb_intrinsics[1] -= 16.25
        rgb_intrinsics[2] -= 16.25

        rgb_from_device_extrinsics = calibration_data[timestamp]['rgb']['extrinsics'] ## 4 x 4
        rgb_extrinsics = np.dot(rgb_from_device_extrinsics, device_from_world_extrinsics)
        rgb_extrinsics = rgb_extrinsics[:3, :] ## 3 x 4

        ## left
        left_intrinsics = calibration_data[timestamp]['left']['intrinsics'] ## 15
        left_from_device_extrinsics = calibration_data[timestamp]['left']['extrinsics'] ## 4 x 4
        left_extrinsics = np.dot(left_from_device_extrinsics, device_from_world_extrinsics)
        left_extrinsics = left_extrinsics[:3, :] ## 3 x 4

        ## right
        right_intrinsics = calibration_data[timestamp]['right']['intrinsics'] ## 15
        right_from_device_extrinsics = calibration_data[timestamp]['right']['extrinsics'] ## 4 x 4
        right_extrinsics = np.dot(right_from_device_extrinsics, device_from_world_extrinsics)
        right_extrinsics = right_extrinsics[:3, :] ## 3 x 4

        ##---------parameters to string------------------
        rgb_intrinsics_string = ' '.join(["%.16f" % number for number in rgb_intrinsics]) + '\n'
        rgb_extrinsics_string = ' '.join(["%.16f" % number for number in rgb_extrinsics.T.reshape(-1)]) + '\n'

        left_intrinsics_string = ' '.join(["%.16f" % number for number in left_intrinsics]) + '\n'
        left_extrinsics_string = ' '.join(["%.16f" % number for number in left_extrinsics.T.reshape(-1)]) + '\n'

        right_intrinsics_string = ' '.join(["%.16f" % number for number in right_intrinsics]) + '\n'
        right_extrinsics_string = ' '.join(["%.16f" % number for number in right_extrinsics.T.reshape(-1)]) + '\n'

        ##-------------------------------------
        lines = [HEADER, SECOND_HEADER]
        lines += [rgb_intrinsics_string, rgb_extrinsics_string]
        lines += [left_intrinsics_string, left_extrinsics_string]
        lines += [right_intrinsics_string, right_extrinsics_string]

        with open(save_path, "w") as f:
            f.writelines(lines)


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    print('done!')












