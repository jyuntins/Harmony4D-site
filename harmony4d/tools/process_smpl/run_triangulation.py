import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
import trimesh
from colour import Color
import cv2
import matplotlib.pyplot as plt
from cycler import cycle
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import mmcv

from datasets.aria_camera import AriaCamera
from datasets.aria_human import AriaHuman

np.random.seed(0)

##------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')

def run_debug(p0, p1, p2, p3):
    p0_sphere = p0.get_sphere_mesh(point_3d=p0.location, radius=0.4)
    p1_sphere = p1.get_sphere_mesh(point_3d=p1.location, radius=0.4)
    p2_sphere = p2.get_sphere_mesh(point_3d=p2.location, radius=0.4)
    p3_sphere = p3.get_sphere_mesh(point_3d=p3.location, radius=0.4)

    scene_list = [p0_sphere, p1_sphere, p2_sphere, p3_sphere]
    
    scene = trimesh.Scene(scene_list)
    scene.show()

    return

##------------------------------------------------------------------------------------
def main(sequence_path, output_path, debug=False):
    ego_dir = os.path.join(sequence_path, 'ego')    
    aria_human_names = sorted(os.listdir(ego_dir))

    colmap_transforms_file = os.path.join(sequence_path, 'colmap', 'workplace', 'aria_to_colmap_transforms.pkl')
    aria_humans = [AriaHuman(
                            root_dir=ego_dir, aria_human_name=aria_human_name, \
                            person_id=person_idx, colmap_transforms_file=colmap_transforms_file) \
                    for person_idx, aria_human_name in enumerate(aria_human_names)]

    ##----------------------------------------------------------
    ## aria01, rgb cam
    pose2d_correspondences = {
                        200: []
                        201:
                        202:
                        203:
                        204:
                        205:
                        206:
                        207:
                        208:
                        209:
                        210:
    }


    ##----------------------------------------------------------
    selected_time_stamps = list(range(200, 210 + 1))

    for t in tqdm(time_stamps):
        for human in aria_humans:
            human.update(time_stamp=t)

        if debug == True:
            run_debug(aria_humans[0], aria_humans[1], aria_humans[2], aria_humans[3])

        for viewer in aria_humans:
            for cam_id, cam_type in enumerate(['rgb', 'left', 'right']):
                
                other_human_bboxes = []

                for other_human in aria_humans:
                    if viewer.person_id == other_human.person_id:
                        continue

                    if cam_type == 'rgb':
                        bbox_2d = viewer.get_rgb_bbox_2d(aria_human=other_human)

                    elif cam_type == 'left':
                        bbox_2d = viewer.get_left_bbox_2d(aria_human=other_human)

                    elif cam_type == 'right':
                        bbox_2d = viewer.get_right_bbox_2d(aria_human=other_human)

                    other_human_bboxes.append({'bbox': bbox_2d, 'person_id': other_human.person_id, 'color': other_human.color})

                ##---------draw the bboxes----------
                if cam_type == 'rgb':
                    image = viewer.get_rgb_image()

                elif cam_type == 'left':
                    image = viewer.get_left_image()

                elif cam_type == 'right':
                    image = viewer.get_right_image()

                for bbox_2d_info in other_human_bboxes:
                    bbox_2d = bbox_2d_info['bbox']
                    color = bbox_2d_info['color']

                    if bbox_2d is not None:
                        image = cv2.rectangle(image, (bbox_2d[0], bbox_2d[1]), (bbox_2d[2], bbox_2d[3]), color, 2)

                save_dir = os.path.join(output_path, viewer.aria_human_name, cam_type)
                os.makedirs(save_dir, exist_ok=True)
                cv2.imwrite(os.path.join(save_dir, '{:05d}.jpg'.format(t)), image)


    # cmd = 'convert -delay 100 -loop 0 {}/*.jpg {}/output.gif'.format(output_path, output_path)
    # os.system(cmd)

    return

##------------------------------------------------------------------------------------
if __name__ == "__main__":
    args = parser.parse_args()
    sequence_path = args.sequence_path
    output_path = os.path.join(args.output_path, 'bboxes') ## save the bboxes
    os.makedirs(output_path, exist_ok=True)
    print('sequence at {}'.format(sequence_path))

    debug = False
    # debug = True

    main(sequence_path, output_path, debug=debug)
    print('done')
