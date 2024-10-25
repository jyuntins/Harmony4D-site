import cv2
import numpy as np
import os
from tqdm import tqdm
import json
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import argparse
import pickle
import shutil
from scipy.spatial.transform import Rotation as R

import _init_paths
from utils import procrustes_alignment
from utils.transforms import linear_transform

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
  parser.add_argument('--aria-workplace-dir', help='path to the aria dir')
  parser.add_argument('--exo-workplace-dir', help='path to the exo dir')

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
  # colmap_extrinsics_path = os.path.join(colmap_dir, 'images.txt')
  colmap_extrinsics_path = os.path.join(colmap_dir, 'images_ba.txt') ## bundle adjusted file used!

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

    if camera_name not in aria_cameras and camera_name.startswith('aria'):
      aria_cameras.append(camera_name)

  ##-------------now per camera, store the points by time, both colmap and aria calib
  output = {aria_camera:[] for aria_camera in aria_cameras} ## list of points stored by time

  ##-----------------------------------------
  for line in data:
    image_path = line[-1]
    camera_name = image_path.split('/')[0]
    image_name = image_path.split('/')[1]

    if camera_name.startswith('aria'):
      qvec = np.asarray([float(element) for element in line[1:5]]) ## QW, QX, QY, QZ
      translation = np.asarray([float(element) for element in line[5:8]]) ## TX, TY, TZ
      rotmat = qvec2rotmat(qvec=qvec)
      colmap_camera_center = -1*np.dot(rotmat.T, translation) ## -R^t * T

      aria_camera_center = get_aria_camera_center(aria_dir, camera_name, image_name)

      point_info = {
                    'colmap_camera_center': colmap_camera_center, \
                    'aria_camera_center': aria_camera_center, \
                    'image_name': image_name
                    }

      output[camera_name].append(point_info)

  return output

# # ##------------------------------------------------

def reformat_colmap(raw_colmap_dir, colmap_dir, exo_dir, camera_mapping):
  """
    Renames the camera names to the code's format
    raw_colmap_dir is in Minh's format, camera names as 0, 1, 2, ...
    colmap_dir is in the code's format, camera names as aria01, aria02, aria03....
  """
  os.makedirs(colmap_dir, exist_ok=True)

  source_intrinsics_file = os.path.join(raw_colmap_dir, 'cameras.txt')
  source_extrinsics_file = os.path.join(raw_colmap_dir, 'images.txt')
  source_points_file = os.path.join(raw_colmap_dir, 'points3D.txt')

  target_intrinsics_file = os.path.join(colmap_dir, 'cameras.txt')
  target_extrinsics_file = os.path.join(colmap_dir, 'images.txt')
  target_points_file = os.path.join(colmap_dir, 'points3D.txt')

  shutil.copy(source_intrinsics_file, target_intrinsics_file)
  shutil.copy(source_points_file, target_points_file)

  with open(source_extrinsics_file) as f:
    data = f.readlines()

  modified_data = data[:4]
  data = data[4:]

  image_infos = data[0::2]
  point2d_infos = data[1::2]

  assert(len(image_infos) == len(point2d_infos))

  for (image_info, point2d_info) in zip(image_infos, point2d_infos):
    image_info = image_info.split()
    image_path = image_info[-1]
    camera_name = image_path.split('/')[0]
    image_name = image_path.split('/')[1]

    modified_camera_name = camera_mapping[camera_name]
    modified_image_path = os.path.join(modified_camera_name, image_name)

    modified_image_info = image_info.copy()
    modified_image_info[-1] = modified_image_path
    modified_image_info = ' '.join(modified_image_info) + '\n'
    modified_data.append(modified_image_info)
    modified_data.append(point2d_info)

  f = open(target_extrinsics_file, "w")
  f.writelines(modified_data)
  f.close()

  print('generating bundle adjusted camera parameters for aria and exo')

  bundle_adjusted_file = os.path.join(raw_colmap_dir, 'BA_Camera_AllParams_after.txt')
  if os.path.exists(bundle_adjusted_file):
    read_bundle_adjusted_data(bundle_adjusted_file, target_extrinsics_file, exo_dir)

  else:
    print('BA file not found!')
    exit()
  return

# --------------------------------------------------
# int lensType, shutterModel, width, height;
# double fx, fy, skew, u0, v0, r1, r2, r3, t1, t2, p1, p2, omega, DistCtrX, DistCtrY, rt[6];  
def read_bundle_adjusted_data(ba_file, extrinsics_file, exo_dir, debug=True):
  with open(ba_file) as f:
    ba_data = f.readlines()
    ba_data = ba_data[1:] ## drop the first line

  ## load extrinsics file
  with open(extrinsics_file) as f:
    data = f.readlines()
    header = data[:4]
    data = data[4:]

  image_infos = data[0::2]
  point2d_infos = data[1::2]
  image_ids = [int(info.split()[0]) for info in image_infos]
  camera_names = [(info.split()[-1]).split('/')[0] for info in image_infos]
  image_names = [(info.split()[-1]).split('/')[1] for info in image_infos]

  all_info = {} ## image_id to info
  for image_id, image_info, point2d_info, camera_name, image_name in zip(image_ids, image_infos, point2d_infos, camera_names, image_names):
    all_info[image_id] = {'image_info': image_info, 'point2d_info': point2d_info, 'camera_name': camera_name, 'image_name': image_name}

  for i, line in enumerate(ba_data):
    line = line.split()
    assert(line[0].endswith('.png'))
    image_id = int(line[0].replace('.png', ''))
    lens_type = int(line[1])
    shutter_model = int(line[2])
    image_width = int(line[3])
    image_height = int(line[4])

    if image_id not in all_info.keys():
      continue

    info = all_info[image_id]
    camera_name = info['camera_name']
    image_name = info['image_name']
    image_info = info['image_info']
    original_qvec = [float(val) for val in image_info.split()[1:5]]
    original_translation = [float(val) for val in image_info.split()[5:8]]

    ## this line contains the intrinsics and the extrinsics of the aria camera
    ## 21 parameters, 1 + 2 + 6 + 2 + 4 + 6 (extrinsics)
    if camera_name.startswith('aria'):
      # focal_length = float(line[5])
      # c_u, c_v = float(line[6]), float(line[7])
      # k0, k1, k2, k3, k4, k5 = float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]),
      # p0, p1 = float(line[14]), float(line[15])
      # s0, s1, s2, s3 = float(line[16]), float(line[17]), float(line[18]), float(line[19])
      # rotvec = [float(line[20]), float(line[21]), float(line[22])]
      # translation = [float(line[23]), float(line[24]), float(line[25])]

      # rotation = R.from_rotvec(rotvec)
      # qvec = rotation.as_quat()
      # qvec = [qvec[3], qvec[0], qvec[1], qvec[2]] ## reorder, guesswork

      fx = float(line[5])
      fy = float(line[6])
      skew = float(line[7])
      u0 = float(line[8])
      v0 = float(line[9])
      r1, r2, r3 = float(line[10]), float(line[11]), float(line[12])
      t1, t2 = float(line[13]), float(line[14])
      p1, p2 = float(line[15]), float(line[16])
      rotvec = [float(line[17]), float(line[18]), float(line[19])]
      translation = np.array([float(line[20]), float(line[21]), float(line[22])])
      rotation = R.from_rotvec(rotvec)
      qvec = rotation.as_quat()
      qvec = [qvec[3], qvec[0], qvec[1], qvec[2]] ## reorder, guesswork
      rotmat = qvec2rotmat(qvec)

    ## radial tangential prism, 21 parameters
    ## fscanf(fp, "%lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf ", &fx, &fy, &skew, &u0, &v0,
    # &r1, &r2, &r3, &t1, &t2, &p1, &p2,
    # &rt[0], &rt[1], &rt[2], &rt[3], &rt[4], &rt[5]);
    else:
      assert(camera_name.startswith('cam'))
      fx = float(line[5])
      fy = float(line[6])
      skew = float(line[7])
      u0 = float(line[8])
      v0 = float(line[9])
      r1, r2, r3 = float(line[10]), float(line[11]), float(line[12])
      t1, t2 = float(line[13]), float(line[14])
      p1, p2 = float(line[15]), float(line[16])
      rotvec = [float(line[17]), float(line[18]), float(line[19])]
      translation = np.array([float(line[20]), float(line[21]), float(line[22])])
      rotation = R.from_rotvec(rotvec)
      qvec = rotation.as_quat()
      qvec = [qvec[3], qvec[0], qvec[1], qvec[2]] ## reorder, guesswork
      rotmat = qvec2rotmat(qvec)

    if debug == True:
      print(camera_name, image_name)
      print('original_qvec', original_qvec, 'original_transl', original_translation)
      print('qvec', qvec, 'transl', translation)
      print('original_rotmat', qvec2rotmat(original_qvec))
      print('rotmat', qvec2rotmat(qvec))
      print()

    modified_image_info = [image_info.split()[0]] + [str(val) for val in qvec] + [str(val) for val in translation] + [image_info.split()[-2]] + [image_info.split()[-1]]
    modified_image_info = ' '.join(modified_image_info) + '\n'
    all_info[image_id]['modified_image_info'] = modified_image_info
    all_info[image_id]['camera_name'] = camera_name
    all_info[image_id]['image_name'] = image_name
    all_info[image_id]['intrinsics'] = '{} {} {} {} {} {} {} {} {} {} {} {}\n'.format(fx, fy, skew, u0, v0, r1, r2, r3, t1, t2, p1, p2)

    extrinsics = np.concatenate([rotmat, translation.reshape(3, 1)], axis=1)
    extrinsics_flat = extrinsics.reshape(-1)
    extrinsics_string = ' '.join([str(val) for val in extrinsics_flat.tolist()]) + '\n'
    all_info[image_id]['extrinsics'] = extrinsics_string

  ##---------------write the new ba extrinsics file for PA---------------------
  ## we mimic the colmap format, generate new images.txt
  ## we also generate calib/ files for the exo camera - custom camera model
  ba_extrinsics_file = extrinsics_file.replace('images.txt', 'images_ba.txt')

  writelines = header

  for image_id in all_info.keys():
    info = all_info[image_id]
    image_info = info['image_info']
    modified_image_info = info['modified_image_info']
    point2d_info = info['point2d_info']

    writelines.append(modified_image_info)
    writelines.append(point2d_info)

  f = open(ba_extrinsics_file, "w")
  f.writelines(writelines)
  f.close()

  ##----------write the exo camera parameters----------------
  exo_camera_names = sorted(os.listdir(exo_dir))
  header = 'Serial, intrinsics (radtanthinprsim), extrinsic (3x4)\n'


  for image_id in all_info.keys():
    info = all_info[image_id]
    image_info = info['image_info']
    modified_image_info = info['modified_image_info']
    image_name = info['image_name']
    camera_name = info['camera_name']
    intrinsics = info['intrinsics']
    extrinsics = info['extrinsics']

    if camera_name.startswith('aria'):
      continue

    calibration_file = image_name.replace('.jpg', '.txt')
    calibration_dir = os.path.join(exo_dir, camera_name, 'calib')
    os.makedirs(calibration_dir, exist_ok=True)

    calibration_path = os.path.join(calibration_dir, calibration_file)

    writelines = [header] + ['{}\n'.format(camera_name)]
    writelines.append(intrinsics)
    writelines.append(extrinsics)

    f = open(calibration_path, "w")
    f.writelines(writelines)
    f.close()


  return



# # ##------------------------------------------------
def runner(aria_dir, exo_dir, colmap_dir):
  all_camera_names = ['aria01', 'aria02', 'aria03', 'aria04', 'aria05', 'aria06', \
      'cam01', 'cam02', 'cam03', 'cam04', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09','cam10']

  camera_mapping = {str(i): camera_name for i, camera_name in enumerate(all_camera_names)}
  print(camera_mapping)
  print('please set the camera mapping! and uncomment the exit!')
  # exit()

  reformat_colmap(colmap_dir.replace('workplace', 'raw_workplace'), colmap_dir, exo_dir, camera_mapping)

  data = process_data(aria_dir, colmap_dir)
  aria_to_colmap_transforms = {}

  for aria_camera in data.keys():
    ## we compute colmap to aria
    T, l2_error, output = run_procrustes_alignment(data, camera=aria_camera, transform_type='aria2colmap')
    print('camera {} to colmap -- mean error:{}, scale:{}'.format(aria_camera, l2_error, output['scale']))
    aria_to_colmap_transforms[aria_camera] = T ## aria to colmap

  print('saving transforms to {}'.format(os.path.join(colmap_dir, 'colmap_from_aria_transforms.pkl')))
  with open(os.path.join(colmap_dir, 'colmap_from_aria_transforms.pkl'), 'wb') as handle:
    pickle.dump(aria_to_colmap_transforms, handle, protocol=pickle.HIGHEST_PROTOCOL)
  print('done')

  ###-------------------------
  colmap_to_aria_transforms = {}

  for aria_camera in data.keys():
    ## we compute colmap to aria
    T, l2_error, output = run_procrustes_alignment(data, camera=aria_camera, transform_type='colmap2aria')
    print('camera colmap to {} -- mean error:{}, scale:{}'.format(aria_camera, l2_error, output['scale']))
    colmap_to_aria_transforms[aria_camera] = T ## aria to colmap

  print('saving transforms to {}'.format(os.path.join(colmap_dir, 'aria_from_colmap_transforms.pkl')))
  with open(os.path.join(colmap_dir, 'aria_from_colmap_transforms.pkl'), 'wb') as handle:
    pickle.dump(colmap_to_aria_transforms, handle, protocol=pickle.HIGHEST_PROTOCOL)
  print('done')  

  return

# # ##------------------------------------------------
def run_procrustes_alignment(data, camera, transform_type='aria2colmap'):
  colmap_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in data[camera]] ## camera center according to colmap
  aria_centers = [val['aria_camera_center'].reshape(-1, 3) for val in data[camera]] ## camera center according to aria
  colmap_centers = np.concatenate(colmap_centers, axis=0)
  aria_centers = np.concatenate(aria_centers, axis=0)
  ## src, dest, maps points src to dest
  ## maps colmapcenters to aria centers
  if transform_type == 'colmap2aria':
    T, l2_error, output = procrustes_alignment.procrustes_alignment(colmap_centers, aria_centers) 
  elif transform_type == 'aria2colmap':
    T, l2_error, output = procrustes_alignment.procrustes_alignment(aria_centers, colmap_centers) 

  ###------compute l2 error for aria to colmap---------------------
  if transform_type == 'aria2colmap':
    colmap_centers_hat = linear_transform(points_3d=aria_centers, T=T)
    l2_error = np.mean((colmap_centers_hat - colmap_centers)**2)
  elif transform_type == 'colmap2aria':
    aria_centers_hat = linear_transform(points_3d=colmap_centers, T=T)
    l2_error = np.mean((aria_centers_hat - aria_centers)**2)

  return T, l2_error, output


##------------------------------------------------
def main():
  args = parse_args()
  runner(aria_dir=args.aria_workplace_dir, exo_dir=args.exo_workplace_dir, colmap_dir=args.colmap_workplace_dir)
  return


##------------------------------------------------
if __name__ == '__main__':
  main()