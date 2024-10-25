import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import cv2
import shutil


##-------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Process vrs calibration data')
    parser.add_argument('--source_images_dir', action='store', help='image directory of the extracted')
    parser.add_argument('--source_calib_dir', action='store', help='calibration directory of the vrs')
    parser.add_argument('--target_images_dir', action='store', help='image directory of the extracted')
    parser.add_argument('--target_calib_dir', action='store', help='calibration directory of the vrs')

    args = parser.parse_args()

    source_images_dir = args.source_images_dir
    source_calib_dir = args.source_calib_dir

    target_images_dir = args.target_images_dir
    target_calib_dir = args.target_calib_dir

    if not os.path.exists(target_images_dir):
        os.makedirs(target_images_dir)

    if not os.path.exists(target_calib_dir):
        os.makedirs(target_calib_dir)

    ##---------------------------------------
    target_rgb_dir = os.path.join(target_images_dir, 'rotated_rgb')
    target_left_dir = os.path.join(target_images_dir, 'rotated_left')
    target_right_dir = os.path.join(target_images_dir, 'rotated_right')
    
    if not os.path.exists(target_rgb_dir):
        os.makedirs(target_rgb_dir)

    if not os.path.exists(target_left_dir):
        os.makedirs(target_left_dir)

    if not os.path.exists(target_right_dir):
        os.makedirs(target_right_dir)

    ##----------------------------------------
    RGB_PREFIX = '214-1'
    LEFT_PREFIX = '1201-1'
    RIGHT_PREFIX = '1201-2'

    source_rgb_images = [os.path.join(source_images_dir, RGB_PREFIX, name) for name in sorted(os.listdir(os.path.join(source_images_dir, RGB_PREFIX)))]
    source_left_images = [os.path.join(source_images_dir, LEFT_PREFIX, name) for name in sorted(os.listdir(os.path.join(source_images_dir, LEFT_PREFIX)))]
    source_right_images = [os.path.join(source_images_dir, RIGHT_PREFIX, name) for name in sorted(os.listdir(os.path.join(source_images_dir, RIGHT_PREFIX)))]
    
    min_len = min(len(source_rgb_images), len(source_left_images), len(source_right_images))

    if len(source_rgb_images) > min_len or len(source_left_images) > min_len or len(source_right_images) > min_len:
        source_rgb_images = source_rgb_images[:min_len]
        source_left_images = source_left_images[:min_len]
        source_right_images = source_right_images[:min_len]

    assert(len(source_rgb_images) == len(source_left_images) == len(source_right_images))

    ##---------------------------------------
    source_calibration_files = [os.path.join(source_calib_dir, name) for name in sorted(os.listdir(source_calib_dir))]
    calibration_timestamps = {((source_calibration_file.split('/')[-1]).replace('.txt', '').split('-'))[-1]: source_calibration_file for source_calibration_file in sorted(source_calibration_files)}

    ##---------------------------------------
    save_timestamp = 0

    for i, (source_rgb_image, source_left_image, source_right_image) in enumerate(zip(source_rgb_images, source_left_images, source_right_images)):
        rgb_timestamp = (source_rgb_image.split('/')[-1]).replace('.jpg', '').split('-')[-1]
        left_timestamp = (source_left_image.split('/')[-1]).replace('.jpg', '').split('-')[-1]
        right_timestamp = (source_right_image.split('/')[-1]).replace('.jpg', '').split('-')[-1]

        print('{}/{}: {}'.format(i+1, len(source_rgb_images), rgb_timestamp))

        if left_timestamp not in calibration_timestamps.keys():

            ## find nearest calibration timestamp by searching for the closest timestamp
            found_min = False
            nn_calibration_timestamp = None

            ## create a numpy array of from the calibration timestamps
            calibration_timestamps_array = np.array([float(calibration_timestamp) for calibration_timestamp in calibration_timestamps.keys()])
            calibration_timestamps_array = calibration_timestamps_array.reshape(-1, 1)

            ## compute the difference between the timestamps
            diff = np.abs(calibration_timestamps_array - float(left_timestamp))

            ## find the minimum difference
            min_diff = np.min(diff)
            index = np.argmin(diff)

            temp = list(calibration_timestamps.keys())
            nn_calibration_timestamp = temp[index]

            if min_diff > 1e-3 + 1e-6:
                print('could not find calibration timestamp for left image: {}, nearest timestamp: {} diff: {}'.format(left_timestamp, nn_calibration_timestamp, min_diff))
                continue
            else:
                print('found nn calibration timestamp for left image: {} as {}'.format(left_timestamp, nn_calibration_timestamp))
                left_timestamp = nn_calibration_timestamp


        ## assert that the difference between the timestamps is less than 5e-2
        assert(abs(float(rgb_timestamp) - float(left_timestamp)) < 1e-3 + 1e-6)
        assert(abs(float(rgb_timestamp) - float(right_timestamp)) < 1e-3 + 1e-6)
        assert(abs(float(left_timestamp) - float(right_timestamp)) <1e-3 + 1e-6)

        source_calibration_file = calibration_timestamps[left_timestamp]

        save_timestamp += 1
        shutil.copy(source_rgb_image, os.path.join(target_rgb_dir, '{:05d}.jpg'.format(save_timestamp)))
        shutil.copy(source_left_image, os.path.join(target_left_dir, '{:05d}.jpg'.format(save_timestamp)))
        shutil.copy(source_right_image, os.path.join(target_right_dir, '{:05d}.jpg'.format(save_timestamp)))
        shutil.copy(source_calibration_file, os.path.join(target_calib_dir, '{:05d}.txt'.format(save_timestamp)))

    return

##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    print('done!')












