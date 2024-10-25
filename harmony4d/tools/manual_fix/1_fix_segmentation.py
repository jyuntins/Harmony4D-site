import _init_paths
import numpy as np
import os
import argparse
from tqdm import tqdm
import cv2
from datasets.ego_exo_scene import EgoExoScene
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

    output_path = os.path.join(args.output_path, 'segmentation') 
    vis_output_path = os.path.join(args.output_path, 'vis_segmentation') 
    print('sequence at {}'.format(sequence_path))

    camera_names = args.cameras
    camera_names = ['cam{:02d}'.format(int(val)) for val in camera_names.split(':')]

    ## load all exo_camera names from sequence_path
    all_exo_cameras = sorted(os.listdir(os.path.join(sequence_path, 'exo')))

    ## set exo_cameras not in camera_names as invalid
    for camera_name in all_exo_cameras:
        if camera_name not in camera_names:
            cfg.INVALID_EXOS.append(camera_name)

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    scene.init_segmentation()

    time_stamps = [int(timestamp) for timestamp in args.timestamps.split(":")]
    
    camera_mode = 'rgb'
    factor = 3.0 ## resize factor, the original image is too big

    for t, camera_name in tqdm(zip(time_stamps, camera_names)):
        scene.update(time_stamp=t)

        scene.set_view(camera_name=camera_name, camera_mode=camera_mode)
        segmentation = scene.load_segmentation()

        segmentation_resized = segmentation.copy()

        for i, human_name in enumerate(segmentation_resized):
            segmentation_resized[human_name]['bbox'] = segmentation_resized[human_name]['bbox'][:4]/factor if segmentation_resized[human_name]['bbox'] is not None else None
            
            mask = segmentation_resized[human_name]['segmentation']
            if mask is not None:
                mask = cv2.resize(mask*1.0, (int(mask.shape[1]/factor), int(mask.shape[0]/factor)), interpolation=cv2.INTER_AREA)
                segmentation_resized[human_name]['segmentation'] = mask

        image_path = scene.view_camera.get_image_path(time_stamp=t)
        image_name = image_path.split('/')[-1]
        image_original = cv2.imread(image_path)
        image_original_width = image_original.shape[1]
        image_original_height = image_original.shape[0]

        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)

        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

        # Display the image
        cv2.imshow('Image', image_original_resized)

        # Wait for a key press and close the window
        cv2.waitKey(1)
        cv2.destroyAllWindows()


        def click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                if params['human_name'] is not None:
                    params['drawing'] = True
                    params['current_contour'].append((x, y))
            elif event == cv2.EVENT_MOUSEMOVE:
                if params['drawing']:
                    cv2.circle(params['mask'], (x, y), 5, 255, -1)
                    params['current_contour'].append((x, y))
            elif event == cv2.EVENT_LBUTTONUP:
                if params['drawing']:
                    params['drawing'] = False
                    cv2.circle(params['mask'], (x, y), 5, 255, -1)
                    params['current_contour'].append((x, y))
                    params['contours'].append(params['current_contour'])
                    params['current_contour'] = []

            # Save the segmentation mask for the current human
            if event == cv2.EVENT_KEYPRESS and chr(flags) == 's':
                filled_mask = np.zeros_like(params['mask'])
                for contour in params['contours']:
                    cv2.fillPoly(filled_mask, np.array([contour], dtype=np.int32), 255)
                params['segmentation'][params['human_name']]['segmentation'] = filled_mask
                params['mask'] = np.zeros(image_original_resized.shape[:2], dtype=np.uint8)
                params['contours'] = []

            # Update the display image with the drawn mask
            display_image = cv2.addWeighted(params['image_original'], 0.7, cv2.cvtColor(params['mask'], cv2.COLOR_GRAY2BGR), 0.3, 0)
            params['canvas'] = display_image

            return

        window_title = '{}-{}'.format(camera_name, image_name)
        cv2.namedWindow(window_title)
        params = {'segmentation': segmentation_resized, 'human_name': None, \
                    'drawing': False, 'mask': np.zeros(image_original_resized.shape[:2], dtype=np.uint8),
                    'contours': [], 'current_contour': [],
                    'image_original': image_original_resized, 'canvas': image_original_resized.copy()}

        cv2.setMouseCallback(window_title, click_event, params)

        while True:
            print("Inside the while loop")
            cv2.imshow(window_title, params['canvas'])
            key = cv2.waitKey(1) & 0xFF

            ## refresh everything
            if key == ord("r"):
                params['canvas'] = image_original_resized.copy()
                params['human_name'] = None

            elif key == ord("1"):
                params['human_name'] = 'aria01'

            elif key == ord("2"):
                params['human_name'] = 'aria02'

           ## escape
            elif key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        modified_segmentation = params['segmentation']
        for i, human_name in enumerate(modified_segmentation):
            mask = modified_segmentation[human_name]['segmentation']
            if mask is not None:
                mask = cv2.resize(mask, (image_original_width, image_original_height), interpolation=cv2.INTER_AREA)
                modified_segmentation[human_name]['segmentation'] = mask

        segmentation = modified_segmentation.copy()

        ##-----------save segmentation--------------
        save_dir = os.path.join(output_path, scene.viewer_name, scene.view_camera_type)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, '{:05d}.npy'.format(t))
        scene.save_segmentation(segmentation, save_path)

        ##-------------visualize the segmentation-------------------
        save_dir = os.path.join(vis_output_path, scene.viewer_name, scene.view_camera_type)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, '{:05d}.jpg'.format(t))
        scene.draw_segmentation(segmentation, save_path)


    print('done annotating')
        
    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()