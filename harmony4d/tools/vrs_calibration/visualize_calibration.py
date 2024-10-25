import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import cv2
import ast
import pandas as pd
import trimesh
import matplotlib.pyplot as plt

##-------------------------------------------------------
CALIB_DIR = '/home/rawalk/Desktop/datasets/surreal_bypass/new_calib'
calibration_files = [os.path.join(CALIB_DIR, name) for name in sorted(os.listdir(CALIB_DIR))]


##--------------------------------------------------------
def get_mesh_sphere(location, radius=0.02, color=[255, 0, 0], alpha=0.7):
    transform = np.eye(4) ##4x4
    transform[:3, 3] = location 
    mesh = trimesh.primitives.Sphere(radius=radius)
    mesh.apply_transform(transform)

    mesh.visual.face_colors = [color[0], color[1], color[2], 255*alpha]

    return mesh

def read_calibration(calibration_file):
    with open(calibration_file) as f:
        lines = f.readlines()
        lines = lines[1:] ## drop the header, eg. Serial, intrinsics (radtanthinprsim), extrinsic (3x4)
        lines = [line.strip() for line in lines]

    output = {}
    assert(len(lines) % 7 == 0) # 1 for person id, 2 lines each for rgb, left and right cams. Total 7 lines per person
    num_persons = len(lines)//7
    assert(num_persons == 1) ## we assume only single person per calib directory

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

    return output[0] 

def get_camera_center(extrinsics):
    extrinsics = np.concatenate([extrinsics, [[0, 0, 0, 1]]], axis=0) ## 4 x 4
    inv_extrinsics = np.linalg.inv(extrinsics)

    ## finding a XYZ such that [0, 0, 0, 1] = [R, T; 0 1] * [XYZ1];
    center = np.dot(inv_extrinsics, np.array([0, 0, 0, 1]).reshape(4, 1))

    center = center[:3].reshape(-1)
    return center

##--------------------------------------------------------
plt.figure(figsize=(5, 5))
scene_list = []
trajectory_length = 20

for i, calibration_file in enumerate(calibration_files):

    print(len(scene_list))

    if i % trajectory_length == 0 and i > 0:
        ## refresh
        scene = trimesh.Scene(scene_list)
        scene.show()
        scene_list = []

    parameters = read_calibration(calibration_file)
    
    rgb_extrinsics = parameters['rgb']['extrinsics'] ## 3 x 4
    left_extrinsics = parameters['left']['extrinsics'] ## 3 x 4
    right_extrinsics = parameters['right']['extrinsics'] ## 3 x 4

    rgb_camera_center = get_camera_center(rgb_extrinsics)
    left_camera_center = get_camera_center(left_extrinsics)
    right_camera_center = get_camera_center(right_extrinsics)

    # ------------------------------------------------
    alpha = ((i % trajectory_length)*1.0 + 1)/trajectory_length
    rgb_mesh = get_mesh_sphere(location=rgb_camera_center, radius=0.01, color=[255,0,0], alpha=alpha)
    left_mesh = get_mesh_sphere(location=left_camera_center, radius=0.01, color=[0,255,0], alpha=alpha)
    right_mesh = get_mesh_sphere(location=right_camera_center, radius=0.01, color=[0,0,255], alpha=alpha)

    # segments = np.random.random((100, 2, 3))
    segments = np.zeros((3, 2, 3))
    segments[0, 0, :] = rgb_camera_center; segments[0, 1, :] = left_camera_center; 
    segments[1, 0, :] = rgb_camera_center; segments[1, 1, :] = right_camera_center; 
    segments[2, 0, :] = left_camera_center; segments[2, 1, :] = right_camera_center; 

    rays = trimesh.load_path(segments)

    # ------------------------------------------------
    scene_list += [rgb_mesh, left_mesh, right_mesh, rays]
    # ------------------------------------------------

# create a visualization scene with rays, hits, and mesh
scene = trimesh.Scene(scene_list)
scene.show()





