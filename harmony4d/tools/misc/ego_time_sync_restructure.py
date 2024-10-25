import cv2
import numpy as np
import os
from tqdm import tqdm
import json
import argparse
import shutil
import concurrent.futures

##------------------------------------------------
def parse_args():
  parser = argparse.ArgumentParser(description='Time sync copy')
  parser.add_argument('--sequence', help='')
  parser.add_argument('--cameras', help='')
  parser.add_argument('--start-timestamps', help='these ego timestamps correspond to 00001.jpg to exo')
  parser.add_argument('--sequence-camera-name', help='')
  parser.add_argument('--sequence-start-timestamp', help='')
  parser.add_argument('--sequence-end-timestamp', help='')
  parser.add_argument('--data-dir', help='')
  parser.add_argument('--output-dir', help='')

  args = parser.parse_args()
  return args

# ##------------------------------------------------
def copy_file(src, dst, idx, start_idx, offset=0, extension='jpg'):
    src_image_path = os.path.join(src, '{:05d}.{}'.format(start_idx + idx, extension))
    dst_image_path = os.path.join(dst, '{:05d}.{}'.format(idx + 1 + offset, extension))
    shutil.copyfile(src_image_path, dst_image_path)
    return

def copy_selected_files(src, dst, start_image, num_images, extension='jpg'):
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)

    start_idx = int(start_image.replace('.jpg', ''))
    print(dst)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    # concurrent.processpoolexeccutor create mltiple processes to run the function
    # tdqm is the function used to show the progress bar 
    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(copy_file, [src]*num_images, [dst]*num_images, range(num_images), [start_idx]*num_images, [0]*num_images, [extension]*num_images), total=num_images))
    return

##------------------------------------------------
def copy_selected_files_offset(src, dst, start_image, num_images, offset=0, extension='jpg'):
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)

    start_idx = int(start_image.replace('.jpg', ''))
    print(dst)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(copy_file, [src]*num_images, [dst]*num_images, range(num_images), [start_idx]*num_images, [offset]*num_images, [extension]*num_images), total=num_images))
    return

##------------------------------------------------
def main():
  args = parse_args()
  print("sequence",args.sequence)
  print("cameras",args.cameras)
  print("start timestamps", args.start_timestamps)
  print("sequence_camera_name", args.sequence_camera_name)
  print("sequence_start_timestamp", args.sequence_start_timestamp)
  print("sequence_end_timestamp", args.sequence_end_timestamp)
  print("data_dir", args.data_dir)
  print("output_dir", args.output_dir)
  input()
  sequence_name = args.sequence
  root_read_dir = args.data_dir
  root_write_dir = args.output_dir
  ###----------------------------
  cameras = args.cameras.split('--')
  overall_start_timestamps_ = [int(timestamp) for timestamp in args.start_timestamps.split('--')] ## this corresponds to 00001.jpg in exo
  overall_start_timestamps = {}

  for idx, timestamp in enumerate(overall_start_timestamps_):
    overall_start_timestamps[cameras[idx]] = timestamp

  ###----------------------------
  ### check if multiple sequence start time stamps

  if len(args.sequence_start_timestamp.split(':')) == 1:
    reference_camera_name = args.sequence_camera_name
    reference_camera_start_timestamp = int(args.sequence_start_timestamp)
    reference_camera_end_timestamp = int(args.sequence_end_timestamp)
    num_images = reference_camera_end_timestamp - reference_camera_start_timestamp + 1 
    sequence_offset = reference_camera_start_timestamp - overall_start_timestamps[reference_camera_name]

    camera_names = cameras
    camera_start_image_names = {}
    for camera_name in camera_names:
      ## distance from t=1
      camera_start_timestamp = sequence_offset + overall_start_timestamps[camera_name] 
      start_image = '{:05d}.jpg'.format(camera_start_timestamp)
      camera_start_image_names[camera_name] = start_image
    # # # ##-----copy images---------
    for i, camera_name in enumerate(camera_names):
      # for dir_type in ['left', 'rgb', 'right', 'rotated_left', 'rotated_rgb', 'rotated_right']:
      for dir_type in ['left', 'rgb', 'right']:
        src_path = os.path.join(root_read_dir, camera_name, 'images', dir_type)
        dst_path = os.path.join(root_write_dir, camera_name, 'images', dir_type)

        start_image = camera_start_image_names[camera_name]
        copy_selected_files(src=src_path, dst=dst_path, \
              start_image=start_image, num_images=num_images, \
              extension='jpg')  

    # ##-----copy calib files---------
    for i, camera_name in enumerate(camera_names):
      src_path = os.path.join(root_read_dir, camera_name, 'calib')
      dst_path = os.path.join(root_write_dir, camera_name, 'calib')

      start_image = camera_start_image_names[camera_name]
      copy_selected_files(src=src_path, dst=dst_path, \
                start_image=start_image, num_images=num_images, \
                extension='txt') 

  else:
    ### subsequences with different timestamps
    all_start_timestamps = [int(val) for val in args.sequence_start_timestamp.split(':')]
    all_end_timestamps = [int(val) for val in args.sequence_end_timestamp.split(':')]
    offset = 0

    for reference_camera_start_timestamp, reference_camera_end_timestamp in zip(all_start_timestamps, all_end_timestamps):
      reference_camera_name = args.sequence_camera_name
      num_images = reference_camera_end_timestamp - reference_camera_start_timestamp + 1 
      sequence_offset = reference_camera_start_timestamp - overall_start_timestamps[reference_camera_name]

      camera_names = cameras

      camera_start_image_names = {}
      for camera_name in camera_names:
        ## distance from t=1
        camera_start_timestamp = sequence_offset + overall_start_timestamps[camera_name] 
        start_image = '{:05d}.jpg'.format(camera_start_timestamp)
        camera_start_image_names[camera_name] = start_image

      # # # ##-----copy images---------
      for i, camera_name in enumerate(camera_names):
        for dir_type in ['left', 'rgb', 'right']:
          src_path = os.path.join(root_read_dir, camera_name, 'images', dir_type)
          dst_path = os.path.join(root_write_dir, camera_name, 'images', dir_type)

          start_image = camera_start_image_names[camera_name]
          copy_selected_files_offset(src=src_path, dst=dst_path, \
                start_image=start_image, num_images=num_images, offset=offset, \
                extension='jpg')  

      # ##-----copy calib files---------
      for i, camera_name in enumerate(camera_names):
        src_path = os.path.join(root_read_dir, camera_name, 'calib')
        dst_path = os.path.join(root_write_dir, camera_name, 'calib')

        start_image = camera_start_image_names[camera_name]
        copy_selected_files_offset(src=src_path, dst=dst_path, \
                  start_image=start_image, num_images=num_images, offset=offset, \
                  extension='txt') 

      offset += num_images

  return


##------------------------------------------------
if __name__ == '__main__':
  main()
