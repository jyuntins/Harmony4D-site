import cv2
import numpy as np
import os
from tqdm import tqdm
import json
from mpl_toolkits import mplot3d
import matplotlib
matplotlib.use('Agg')
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

###---------------------------------------------------------------
def process_data(aria_name, aria_dir, colmap_dir):
  aria_extrinsics_path = os.path.join(aria_dir, 'images.txt') ## colmap extrinsics of aria for the entire trajectory
  colmap_extrinsics_path = os.path.join(colmap_dir, 'images.txt') ## colmap extrinsisncs of aria for few timestamps

  ###-----------------------load the trajectory from the overall colmap---------------------------------
  with open(colmap_extrinsics_path) as f:
    data = f.readlines()
    data = data[4:] ## drop the first 3 lines
    data = data[0::2] ## only alternate lines, these have extrinsics

  data = [line.strip().split() for line in data]
  
  ##-------------now per camera, store the points by time, both colmap and aria calib
  overall_output = [] ## list of points stored by time
  overall_image_names = []

  for line in data:
    image_path = line[-1]
    camera_name = image_path.split('/')[0]
    image_name = image_path.split('/')[1]

    if camera_name == aria_name:
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

      overall_output.append(point_info)
      overall_image_names.append(image_name)

  ##---------------------------------------------------------------------------------------------
  ##--------------------now load the single aria camera trajectory-----------------------------------
  with open(aria_extrinsics_path) as f:
    data = f.readlines()
    data = data[4:] ## drop the first 3 lines
    data = data[0::2] ## only alternate lines, these have extrinsics

  data = [line.strip().split() for line in data]

  ##-------------now per camera, store the points by time, both colmap and aria calib
  aria_output = [] ## list of points stored by time
  overall_aria_output = []

  for line in data:
    image_path = line[-1]
    camera_name = aria_name
    image_name = image_path

    if camera_name == aria_name:
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

      if image_name in overall_image_names:
        aria_output.append(point_info)

      overall_aria_output.append(point_info)

  return overall_output, aria_output, overall_aria_output

###------------------------------------------------------------
def run_procrustes_alignment(overall_output, aria_output, transform_type='aria2colmap'):
  colmap_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in overall_output] ## camera center according to colmap with gopros
  aria_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in aria_output] ## camera center according to colmap without gopros
  
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



###---------------------------------------------------------------
aria_name = 'aria02'
# aria_name = 'aria03'
# aria_name = 'aria04'

debug = True

##----------------------------------------------------------------
aria_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/06_volleyball/calibration_volleyball/ego/{}/calib_colmap/'.format(aria_name) ## contains the aria trajectory by colmap
colmap_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/06_volleyball/calibration_volleyball/colmap/workplace/' ## the colmap calib with the gopros

overall_output, aria_output, overall_aria_output = process_data(aria_name, aria_dir, colmap_dir)

## overall_output is aria cam centers by colmap with gopros
## aria_output is the aria cam centers for the same time steps without gopros
## overall_aria_output is the entire camera trajectory

aria_to_colmap_transforms = {}
## we compute colmap to aria
T, l2_error, output = run_procrustes_alignment(overall_output, aria_output, transform_type='aria2colmap')
print('camera {} to colmap -- mean error:{}, scale:{}'.format(aria_name, l2_error, output['scale']))
aria_to_colmap_transforms[aria_name] = T ## aria to colmap

print('saving transforms to {}'.format(os.path.join(colmap_dir, 'colmap_from_aria_{}_transforms.pkl'.format(aria_name))))
with open(os.path.join(colmap_dir, 'colmap_from_aria_{}_transforms.pkl'.format(aria_name)), 'wb') as handle:
  pickle.dump(aria_to_colmap_transforms, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('done')

##---------------------debug------------------
if debug == True:
  colmap_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in overall_output] ## camera center according to colmap with gopros
  aria_centers = [val['colmap_camera_center'].reshape(-1, 3) for val in aria_output] ## camera center according to colmap without gopros
  
  colmap_centers = np.concatenate(colmap_centers, axis=0)
  aria_centers = np.concatenate(aria_centers, axis=0)

  ax = plt.axes(projection='3d')
  # # Data for a three-dimensional line
  xline = aria_centers[:, 0]
  yline = aria_centers[:, 1]
  zline = aria_centers[:, 2]

  ax.plot3D(xline, yline, zline, 'blue')
  ax.scatter3D(xline, yline, zline, 'red');
  plt.show()
  plt.savefig('{}_aria.png'.format(aria_name))
  plt.close()


  ax = plt.axes(projection='3d')
  xline = colmap_centers[:, 0]
  yline = colmap_centers[:, 1]
  zline = colmap_centers[:, 2]

  ax.plot3D(xline, yline, zline, 'blue')
  ax.scatter3D(xline, yline, zline, 'red');
  plt.show()
  plt.savefig('{}_colmap.png'.format(aria_name))
  plt.close()