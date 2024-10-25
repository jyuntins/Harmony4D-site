import cv2
import numpy as np
import os
from tqdm import tqdm
import json
import argparse
import shutil

##------------------------------------------------
def parse_args():
  parser = argparse.ArgumentParser(description='Time sync copy')
  parser.add_argument('--sequence', help='')
  parser.add_argument('--cameras', help='')
  parser.add_argument('--frame_rate', help='')
  parser.add_argument('--qr-timestamps', help='these ego timestamps correspond to 00001.jpg to exo')
  parser.add_argument('--sequence-camera-name', help='')
  parser.add_argument('--sequence-start-timestamp', help='')
  parser.add_argument('--sequence-end-timestamp', help='')
  parser.add_argument('--data-dir', help='')
  parser.add_argument('--output-dir', help='')

  args = parser.parse_args()
    
  return args

##------------------------------------------------
def copy_selected_files(src, dst, start_image, num_images, extension='jpg'):
  if not os.path.exists(dst):
    os.makedirs(dst, exist_ok=False)

  start_idx = int(start_image.replace('.jpg', ''))
  print(dst)
  for idx in tqdm(range(num_images)):
    src_image_path = os.path.join(src, '{:05d}.{}'.format(start_idx + idx, extension))
    dst_image_path = os.path.join(dst, '{:05d}.{}'.format(idx + 1, extension))
    shutil.copyfile(src_image_path, dst_image_path)

  return

##------------------------------------------------
def copy_selected_files_offset(src, dst, start_image, num_images, offset=0, extension='jpg'):
  if not os.path.exists(dst):
    os.makedirs(dst, exist_ok=False)

  start_idx = int(start_image.replace('.jpg', ''))
  print(dst)
  for idx in tqdm(range(num_images)):
    src_image_path = os.path.join(src, '{:05d}.{}'.format(start_idx + idx, extension))
    dst_image_path = os.path.join(dst, '{:05d}.{}'.format(idx + 1 + offset, extension))
    shutil.copyfile(src_image_path, dst_image_path)

  return

##------------------------------------------------
def main():
  args = parse_args()

  sequence_name = args.sequence
  root_read_dir = args.data_dir
  root_write_dir = args.output_dir
  frame_rate = int(args.frame_rate)

  ###----------------------------
  cameras = args.cameras.split('--')
  overall_start_timestamps_ = [int(timestamp.split(':')[0]) for timestamp in args.qr_timestamps.split('--')] ## this corresponds to 00001.jpg in exo
  overall_qr_start_timestamps_ = [int(timestamp.split(':')[1]) for timestamp in args.qr_timestamps.split('--')] ## this corresponds to 00001.jpg in exo

  overall_start_timestamps = {}
  overall_qr_start_timestamps = {}

  for idx, timestamp in enumerate(overall_start_timestamps_):
    overall_start_timestamps[cameras[idx]] = timestamp
  
  for idx, qr_timestamp in enumerate(overall_qr_start_timestamps_):
    overall_qr_start_timestamps[cameras[idx]] = qr_timestamp

  ###----------------------------
  ### check if multiple start time stamps
  if len(args.sequence_start_timestamp.split(':')) == 1:
    reference_camera_name = args.sequence_camera_name
    reference_camera_start_timestamp = int(args.sequence_start_timestamp)
    reference_camera_end_timestamp = int(args.sequence_end_timestamp)
    num_images = reference_camera_end_timestamp - reference_camera_start_timestamp + 1 
    sequence_offset = reference_camera_start_timestamp - overall_start_timestamps[reference_camera_name] ## nuumber of frames to start of sequence

    ##---------compute the reference qr camera start-------------
    reference_camera_qr_start_timestamp = round(overall_qr_start_timestamps[reference_camera_name] + sequence_offset * (1000/frame_rate)) ## qr timestamps in milliseconds, start of the sequence
    camera_names = [val for val in sorted(os.listdir(root_read_dir)) if val.startswith('cam')]

    camera_start_image_names = {}
    for camera_name in camera_names:

      if camera_name not in overall_start_timestamps.keys():
        print('{} not used for this sequence'.format(camera_name))
        continue

      ## distance from t=1
      camera_qr_start_timestamp = overall_qr_start_timestamps[camera_name] ## time in milliseconds
      frames_to_start_of_sequence = round(((reference_camera_qr_start_timestamp - camera_qr_start_timestamp)/1000)*frame_rate)  ## time to sequence
      camera_start_timestamp = frames_to_start_of_sequence + overall_start_timestamps[camera_name] 
      start_image = '{:05d}.jpg'.format(camera_start_timestamp)
      camera_start_image_names[camera_name] = start_image

    # # # # ##-----copy images---------
    for i, camera_name in enumerate(camera_names):
      src_path = os.path.join(root_read_dir, camera_name, 'images')
      dst_path = os.path.join(root_write_dir, camera_name, 'images')

      if camera_name not in overall_start_timestamps.keys():
        continue

      start_image = camera_start_image_names[camera_name]
      copy_selected_files(src=src_path, dst=dst_path, \
            start_image=start_image, num_images=num_images, \
            extension='jpg')  
  else:
    ### subsequences with different timestamps
    all_start_timestamps = [int(val) for val in args.sequence_start_timestamp.split(':')]
    all_end_timestamps = [int(val) for val in args.sequence_end_timestamp.split(':')]
    offset = 0

    for reference_camera_start_timestamp, reference_camera_end_timestamp in zip(all_start_timestamps, all_end_timestamps):
      reference_camera_name = args.sequence_camera_name
      num_images = reference_camera_end_timestamp - reference_camera_start_timestamp + 1 
      sequence_offset = reference_camera_start_timestamp - overall_start_timestamps[reference_camera_name]

      camera_names = [val for val in sorted(os.listdir(root_read_dir)) if val.startswith('cam')]

      camera_start_image_names = {}
      for camera_name in camera_names:

        if camera_name not in overall_start_timestamps.keys():
          print('{} not used for this sequence'.format(camera_name))
          continue

        ## distance from t=1
        camera_start_timestamp = sequence_offset + overall_start_timestamps[camera_name] 
        start_image = '{:05d}.jpg'.format(camera_start_timestamp)
        camera_start_image_names[camera_name] = start_image


      # # # # ##-----copy images---------
      for i, camera_name in enumerate(camera_names):
        src_path = os.path.join(root_read_dir, camera_name, 'images')
        dst_path = os.path.join(root_write_dir, camera_name, 'images')

        if camera_name not in overall_start_timestamps.keys():
          continue

        start_image = camera_start_image_names[camera_name]
        copy_selected_files_offset(src=src_path, dst=dst_path, \
              start_image=start_image, num_images=num_images, offset=offset, \
              extension='jpg')  

      offset += num_images

  return


##------------------------------------------------
if __name__ == '__main__':
  main()