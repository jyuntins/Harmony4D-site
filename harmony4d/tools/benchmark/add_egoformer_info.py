import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import pickle
import cv2
import matplotlib.pyplot as plt
from cycler import cycle
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import mmcv
from datetime import datetime

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--egoformer_output', action='store', help='the path to the sequence for visualization')

    args = parser.parse_args()

    ##--------load detections--------------------------
    detections_path = os.path.join(args.output_path, 'coco_track', 'detections_ego_rgb.pkl')
    with open(detections_path, 'rb') as f:
        coco_detections = pickle.load(f)

    ##-------------get camera extrinsics-------------------
    tracking_path = os.path.join(args.output_path, 'coco_track', 'tracking_ego_rgb.json')
    with open(tracking_path, 'rb') as f:
        coco = json.load(f)

    camera_extrinsics = {}
    for image_info in coco['images']:
        extrinsics = np.array(image_info['extrinsics']).reshape(4, 4)
        image_path = image_info['file_name']
        camera_extrinsics[image_path] = extrinsics

    ##-----------------load egoformer bev output-----------------
    egoformer_output_path = args.egoformer_output
    with open(egoformer_output_path, 'rb') as f:
        egoformer_output = pickle.load(f)

    egoformer_output_image_path_to_camera_depth = {}
    for idx in range(len(egoformer_output['image_paths'])):
        image_path = egoformer_output['image_paths'][idx]
        camera_depth = egoformer_output['camera_depths'][idx] ## basically root_z

        egoformer_output_image_path_to_camera_depth[image_path] = camera_depth

    ##--------------make egoformer data----------------------
    coco_detections_egoformer = coco_detections.copy()

    for image_path in coco_detections_egoformer['det_bboxes'].keys():
        bboxes = coco_detections_egoformer['det_bboxes'][image_path]
        roots_3d = coco_detections_egoformer['roots_3d'][image_path]
        keypoints_3d = coco_detections_egoformer['keypoints_3d'][image_path]
        extrinsics = camera_extrinsics[image_path] ## ego rgb camera extrinsics in world coordinates

        camera_depth = egoformer_output_image_path_to_camera_depth[]

        temp = 1

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()