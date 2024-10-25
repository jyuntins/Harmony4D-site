import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
from colour import Color
import cv2
import matplotlib.pyplot as plt
from cycler import cycle
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
import mmcv

from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config
##------------------------------------------------------------------------------------

"""
Press r to reset
Press 1 for selecting aria01
Press 2 for selecting aria02 and so on (till aria08)

Then click on the top-left and bottom right to change the bbox annotation
Press escape to move on to next image

"""


##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--timestamps', default='[1]', help='start time')
    parser.add_argument('--cameras', default='cam01', help='end time')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    output_path = os.path.join(args.output_path, 'bboxes') 
    vis_output_path = os.path.join(args.output_path, 'vis_bboxes') 
    print('sequence at {}'.format(sequence_path))

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    scene.init_bbox()

    time_stamps = [int(timestamp) for timestamp in args.timestamps.split(":")]
    camera_names = args.cameras
    camera_names = ['cam{:02d}'.format(int(val)) for val in camera_names.split(':')]

    camera_mode = 'rgb'
    factor = 3.0 ## resize factor, the original image is too big


    for t, camera_name in tqdm(zip(time_stamps, camera_names)):
        scene.update(time_stamp=t)

        scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
        bboxes = scene.load_bboxes()

        bboxes_resized = bboxes.copy()
        for i in range(len(bboxes_resized)):
            bboxes_resized[i]['bbox'][:4] = bboxes_resized[i]['bbox'][:4]/factor

        image_path = scene.view_camera.get_image_path(time_stamp=t)
        image_name = image_path.split('/')[-1]
        image_original = cv2.imread(image_path)
        image_original_width = image_original.shape[1]
        image_original_height = image_original.shape[0]

        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)
        image = image_original_resized.copy()

        def click_event(event, x, y, flags, params):

            # ----------------checking for left mouse clicks--------------
            if event == cv2.EVENT_LBUTTONDOWN:

                # displaying the coordinates
                # on the Shell
                # print(params['human_name'])
                if params['human_name'] is not None:
                    idx = None
                    # print(len(params['bboxes']))
                    for i in range(len(params['bboxes'])):
                        if params['bboxes'][i]['human_name'] == params['human_name']:
                            idx = i
                            break

                    ## top left
                    if params['top_left'] is None:
                        params['top_left'] = [x, y]
                        cv2.circle(params['canvas'], (x, y), 5, (0, 0, 255), -1)

                    ## bottom right
                    else:
                        assert(len(params['top_left']) == 2)
                        assert(params['top_left'][0] is not None)
                        assert(params['top_left'][1] is not None)

                        params['bottom_right'] = [x, y]
                        cv2.circle(params['canvas'], (x, y), 5, (0, 0, 255), -1)

                        ##--update params[bboxes]---
                        # print(type(params['bboxes']))
                        # print(idx)
                        # print(type(params['bboxes'][idx]))
                        params['bboxes'][idx]['bbox'][0] = params['top_left'][0]
                        params['bboxes'][idx]['bbox'][1] = params['top_left'][1]
                        params['bboxes'][idx]['bbox'][2] = params['bottom_right'][0]
                        params['bboxes'][idx]['bbox'][3] = params['bottom_right'][1]
                        params['bboxes'][idx]['bbox'][4] = 1.0 ## confidence is 1 for hand drawn

                    
            ##-------visualize the params['bboxes']----------
            if params['bottom_right'] is not None:
                params['canvas'] = params['image_original'].copy() ## refresh
                params['human_name'] = None
                params['top_left'] = None
                params['bottom_right'] = None


            for bbox_info in params['bboxes']:
                x1 = int(bbox_info['bbox'][0])
                y1 = int(bbox_info['bbox'][1])
                x2 = int(bbox_info['bbox'][2])
                y2 = int(bbox_info['bbox'][3])
                cv2.rectangle(params['canvas'], (x1, y1), (x2, y2), bbox_info['color'], 5)
            return

        window_title = '{}-{}'.format(camera_name, image_name)
        cv2.namedWindow(window_title)
        params = {'bboxes': bboxes_resized, 'human_name': None, \
                'top_left': None, 'bottom_right': None, \
                'image_original': image_original_resized, 'canvas': image_original_resized.copy()}
        cv2.setMouseCallback(window_title, click_event, params)

        while True:
            cv2.imshow(window_title, params['canvas'])
            key = cv2.waitKey(5) & 0xFF

            ## refresh everything
            if key == ord("r"):
                params['canvas'] = image_original_resized.copy()
                params['human_name'] = None
                params['top_left'] = None
                params['bottom_right'] = None

            elif key == ord("1"):
                params['human_name'] = 'aria01'

            elif key == ord("2"):
                params['human_name'] = 'aria02'

            elif key == ord("3"):
                params['human_name'] = 'aria03'

            elif key == ord("4"):
                params['human_name'] = 'aria04'

            elif key == ord("5"):
                params['human_name'] = 'aria05'

            elif key == ord("6"):
                params['human_name'] = 'aria06'

            elif key == ord("7"):
                params['human_name'] = 'aria07'

            elif key == ord("8"):
                params['human_name'] = 'aria08'

           ## escape
            elif key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        modified_bboxes = params['bboxes']
        for i in range(len(modified_bboxes)):
            modified_bboxes[i]['bbox'][:4] = modified_bboxes[i]['bbox'][:4]*factor

        bboxes = modified_bboxes.copy()

        ##-----------save poses--------------
        save_dir = os.path.join(output_path, scene.viewer_name, scene.view_camera_type)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, '{:05d}.npy'.format(t))
        scene.save_bboxes(bboxes, save_path)
        
        ##-------------visualize the bboxes-------------------            
        save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
        scene.draw_bboxes(bboxes, save_path)

    print('done annotating')
        
    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()