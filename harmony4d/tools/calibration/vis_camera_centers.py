import cv2
import numpy as np
import os
from tqdm import tqdm
import json
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import argparse

import _init_paths
from utils import icp
##------------------------------------------------
# https://github.com/colmap/colmap/blob/d6f528ab59fd653966e857f8d0c2203212563631/scripts/python/read_write_model.py#L453
def qvec2rotmat(qvec):
  return np.array([
      [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
       2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
       2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
      [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
       1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
       2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
      [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
       2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
       1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

##------------------------------------------------
def parse_args():
  parser = argparse.ArgumentParser(description='ICP alignment')
  parser.add_argument('--colmap-workplace-dir', help='path to the colmap dir')
  parser.add_argument('--aria-workplace-dir', help='path to the colmap dir')

  parser.add_argument(
      '--work-dir', help='the dir to save evaluation results')

  args = parser.parse_args()
    
  return args

##------------------------------------------------
def read_aria_calibration(aria_calibration_path, time_stamp):
    time_stamp_string = '{:05d}'.format(time_stamp)
    calibration_file = os.path.join(aria_calibration_path, '{}.txt'.format(time_stamp_string))

    with open(calibration_file) as f:
        lines = f.readlines()
        lines = lines[1:] ## drop the header, eg. Serial, intrinsics (radtanthinprsim), extrinsic (3x4)
        lines = [line.strip() for line in lines]

    output = {}
    assert(len(lines) % 7 == 0) # 1 for person id, 2 lines each for rgb, left and right cams. Total 7 lines per person
    num_persons = len(lines)//7

    for idx in range(num_persons):
        data = lines[idx*7:(idx+1)*7]

        person_id = data[0]
        rgb_intrinsics = np.asarray([float(x) for x in data[1].split(' ')])
        rgb_extrinsics = np.asarray([float(x) for x in data[2].split(' ')]).reshape(4, 3).T

        left_intrinsics = np.asarray([float(x) for x in data[3].split(' ')])
        left_extrinsics = np.asarray([float(x) for x in data[4].split(' ')]).reshape(4, 3).T

        right_intrinsics = np.asarray([float(x) for x in data[5].split(' ')])
        right_extrinsics = np.asarray([float(x) for x in data[6].split(' ')]).reshape(4, 3).T

        ###--------------store everything as nested dicts---------------------
        rgb_cam = {'intrinsics': rgb_intrinsics, 'extrinsics': rgb_extrinsics}
        left_cam = {'intrinsics': left_intrinsics, 'extrinsics': left_extrinsics}
        right_cam = {'intrinsics': right_intrinsics, 'extrinsics': right_extrinsics}

        output[idx] = {'rgb': rgb_cam, 'left': left_cam, 'right':right_cam, 'person_id_string': person_id}

    return output[0]['rgb']['extrinsics'] ## only the person of interest is returned

def get_aria_camera_center(aria_dir, camera_name, image_name):
  aria_calibration_path = os.path.join(aria_dir, camera_name, 'calib')
  time_stamp = int(image_name.replace('.jpg', ''))

  extrinsics = read_aria_calibration(aria_calibration_path, time_stamp)
  rotation = extrinsics[:3, :3]
  translation = extrinsics[:3, 3]
  aria_camera_center = -1*np.dot(rotation.T, translation) ## -R^t * T
  return aria_camera_center

##------------------------------------------------
def process_data(aria_dir, colmap_dir):
  colmap_extrinsics_path = os.path.join(colmap_dir, 'images.txt')

  with open(colmap_extrinsics_path) as f:
    data = f.readlines()
    data = data[4:] ## drop the first 3 lines
    data = data[0::2] ## only alternate lines, these have extrinsics

  data = [line.strip().split() for line in data]
  ##-------------get total number of aria cameras----------------
  aria_cameras = []
  for line in data:
    image_path = line[-1]
    camera_name = image_path.split('/')[0]
    image_name = image_path.split('/')[1]

    if camera_name not in aria_cameras and camera_name.startswith('cam'):
      aria_cameras.append(camera_name)

  ##-------------now per camera, store the points by time, both colmap and aria calib
  output = {aria_camera:[] for aria_camera in aria_cameras} ## list of points stored by time

  ##-----------------------------------------
  for line in data:
    image_path = line[-1]
    camera_name = image_path.split('/')[0]
    image_name = image_path.split('/')[1]

    if camera_name in aria_cameras:
      qvec = np.asarray([float(element) for element in line[1:5]]) ## QW, QX, QY, QZ
      translation = np.asarray([float(element) for element in line[5:8]]) ## TX, TY, TZ
      rotmat = qvec2rotmat(qvec=qvec)
      colmap_camera_center = -1*np.dot(rotmat.T, translation) ## -R^t * T

      aria_camera_center = None

      point_info = {
                    'colmap_camera_center': colmap_camera_center, \
                    'aria_camera_center': aria_camera_center, \
                    'image_name': image_name
                    }

      output[camera_name].append(point_info)

  return output

##------------------------------------------------
def vis_aria_trajectory(aria_dir):
  camera_name = 'aria01'
  aria_centers = []

  for time_stamp in range(5200):
  # for time_stamp in range(5200, 13000):
  # for time_stamp in range(5200, 5400):
  # for time_stamp in range(10000, 11000):

    image_name = '{:05d}.jpg'.format(time_stamp)
    aria_camera_center = get_aria_camera_center(aria_dir, camera_name, image_name)
    print(time_stamp, aria_camera_center)

    aria_centers.append(aria_camera_center.reshape(1, 3))

  ##-------------------------------------
  aria_centers = np.concatenate(aria_centers, axis=0)
  ax = plt.axes(projection='3d')
  xline = aria_centers[:, 0]
  yline = aria_centers[:, 1]
  zline = aria_centers[:, 2]

  ax.plot3D(xline, yline, zline, 'blue')
  ax.scatter3D(xline, yline, zline, 'red');
  plt.show()


  return

##------------------------------------------------
def run_icp(aria_dir, colmap_dir):
  
  data = process_data(aria_dir, colmap_dir)

  ##-------------------------------------
  camera = 'aria01'
  colmap_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in data[camera]] ## camera center according to colmap
  colmap_centers = np.concatenate(colmap_centers, axis=0)

  ax = plt.axes(projection='3d')
  xline = colmap_centers[:, 0]
  yline = colmap_centers[:, 1]
  zline = colmap_centers[:, 2]

  all_x = xline  
  all_y = yline  
  all_z = zline  

  return

##------------------------------------------------
def main():
  args = parse_args()
  # run_icp(aria_dir=args.aria_workplace_dir, colmap_dir=args.colmap_workplace_dir)
  vis_aria_trajectory(aria_dir=args.aria_workplace_dir)
  return


##------------------------------------------------
if __name__ == '__main__':
  main()