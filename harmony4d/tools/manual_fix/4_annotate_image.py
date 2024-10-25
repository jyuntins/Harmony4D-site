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
import string

from datasets.aria_camera import AriaCamera
from datasets.aria_human import AriaHuman
from datasets.ego_exo_scene import EgoExoScene

from configs import cfg
from configs import update_config


# ##------------------------------------------------------------------------------------

"""
Press r to reset
Press 1 for selecting aria01 -- always select this, it is default

a: nose
b: l-eye
c: r-eye
d: l-ear
e: r-ear
f: l-shldr
g: r-shldr
h: l-elbow
i: r-elbow
j: l-wrist
k: r-wrist
l: l-hip
m: r-hip
n: l-knee
o: r-knee
p: l-ankle
q: r-ankle

Press z to commit the pose results
Press escape to move on to next image

## press right click to set the confidence of the keypoint to zero

"""

# ##------------------------------------------------------------------------------------
def draw_pose2d(image, points_2d, radius, color):
    for idx in range(len(points_2d)):
        image = cv2.circle(image, (int(points_2d[idx, 0]), int(points_2d[idx, 1])), radius, color, -1)

    return image

def imshow_keypoints(img,
                     pose_result,
                     skeleton=None,
                     kpt_score_thr=0.3,
                     pose_kpt_color=None,
                     pose_link_color=None,
                     radius=4,
                     thickness=1,
                     show_keypoint_weight=False):
    """Draw keypoints and links on an image.
    Args:
            img (str or Tensor): The image to draw poses on. If an image array
                is given, id will be modified in-place.
            pose_result (list[kpts]): The poses to draw. Each element kpts is
                a set of K keypoints as an Kx3 numpy.ndarray, where each
                keypoint is represented as x, y, score.
            kpt_score_thr (float, optional): Minimum score of keypoints
                to be shown. Default: 0.3.
            pose_kpt_color (np.array[Nx3]`): Color of N keypoints. If None,
                the keypoint will not be drawn.
            pose_link_color (np.array[Mx3]): Color of M links. If None, the
                links will not be drawn.
            thickness (int): Thickness of lines.
    """

    img = mmcv.imread(img)
    img_h, img_w, _ = img.shape

    for kpts in pose_result:
        kpts = np.array(kpts, copy=False)

        # draw each point on image
        if pose_kpt_color is not None:
            assert len(pose_kpt_color) == len(kpts)

            for kid, kpt in enumerate(kpts):
                x_coord, y_coord, kpt_score = int(kpt[0]), int(kpt[1]), kpt[2]

                if kpt_score < kpt_score_thr or pose_kpt_color[kid] is None:
                    # skip the point that should not be drawn
                    continue

                color = tuple(int(c) for c in pose_kpt_color[kid])
                if show_keypoint_weight:
                    img_copy = img.copy()
                    cv2.circle(img_copy, (int(x_coord), int(y_coord)), radius,
                               color, -1)
                    transparency = max(0, min(1, kpt_score))
                    cv2.addWeighted(
                        img_copy,
                        transparency,
                        img,
                        1 - transparency,
                        0,
                        dst=img)
                else:
                    cv2.circle(img, (int(x_coord), int(y_coord)), radius,
                               color, -1)

        # draw links
        if skeleton is not None and pose_link_color is not None:
            assert len(pose_link_color) == len(skeleton)

            for sk_id, sk in enumerate(skeleton):
                pos1 = (int(kpts[sk[0], 0]), int(kpts[sk[0], 1]))
                pos2 = (int(kpts[sk[1], 0]), int(kpts[sk[1], 1]))

                if (pos1[0] <= 0 or pos1[0] >= img_w or pos1[1] <= 0
                        or pos1[1] >= img_h or pos2[0] <= 0 or pos2[0] >= img_w
                        or pos2[1] <= 0 or pos2[1] >= img_h
                        or kpts[sk[0], 2] < kpt_score_thr
                        or kpts[sk[1], 2] < kpt_score_thr
                        or pose_link_color[sk_id] is None):
                    # skip the link that should not be drawn
                    continue
                color = tuple(int(c) for c in pose_link_color[sk_id])
                if show_keypoint_weight:
                    img_copy = img.copy()
                    X = (pos1[0], pos2[0])
                    Y = (pos1[1], pos2[1])
                    mX = np.mean(X)
                    mY = np.mean(Y)
                    length = ((Y[0] - Y[1])**2 + (X[0] - X[1])**2)**0.5
                    angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
                    stickwidth = 2
                    polygon = cv2.ellipse2Poly(
                        (int(mX), int(mY)), (int(length / 2), int(stickwidth)),
                        int(angle), 0, 360, 1)
                    cv2.fillConvexPoly(img_copy, polygon, color)
                    transparency = max(
                        0, min(1, 0.5 * (kpts[sk[0], 2] + kpts[sk[1], 2])))
                    cv2.addWeighted(
                        img_copy,
                        transparency,
                        img,
                        1 - transparency,
                        0,
                        dst=img)
                else:
                    cv2.line(img, pos1, pos2, color, thickness=thickness)

    return img


def draw_all_pose2d(image, poses):

    if poses is None:
        return image

    palette = np.array([[255, 128, 0], [255, 153, 51], [255, 178, 102],
                            [230, 230, 0], [255, 153, 255], [153, 204, 255],
                            [255, 102, 255], [255, 51, 255], [102, 178, 255],
                            [51, 153, 255], [255, 153, 153], [255, 102, 102],
                            [255, 51, 51], [153, 255, 153], [102, 255, 102],
                            [51, 255, 51], [0, 255, 0], [0, 0, 255],
                            [255, 0, 0], [255, 255, 255]])

    skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12],
                        [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9],
                        [8, 10], [1, 2], [0, 1], [0, 2], [1, 3], [2, 4],
                        [3, 5], [4, 6]]

    pose_link_color = np.array([[  0, 255,   0],
       [  0, 255,   0],
       [255, 128,   0],
       [255, 128,   0],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [  0, 255,   0],
       [255, 128,   0],
       [  0, 255,   0],
       [255, 128,   0],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255],
       [ 51, 153, 255]])

    pose_kpt_color = np.array([[ 51, 153, 255],
                       [ 51, 153, 255],
                       [ 51, 153, 255],
                       [ 51, 153, 255],
                       [ 51, 153, 255],
                       [  0, 255,   0],
                       [255, 128,   0],
                       [  0, 255,   0],
                       [255, 128,   0],
                       [  0, 255,   0],
                       [255, 128,   0],
                       [  0, 255,   0],
                       [255, 128,   0],
                       [  0, 255,   0],
                       [255, 128,   0],
                       [  0, 255,   0],
                       [255, 128,   0]])

    radius = 3; thickness = 3

    pose_result = [pose['keypoints'] for pose in poses]
    image = imshow_keypoints(image, pose_result, skeleton, 0.3, pose_kpt_color, pose_link_color, radius, thickness)

    return image

##------------------------------------------------------------------------------------
def keyboard_input():
    text = ""
    letters = string.ascii_lowercase + string.digits
    while True:
        key = cv2.waitKey(10)
        for letter in letters:
            if key == ord(letter):
                text = text + letter
        if key == ord("\n") or key == ord("\r"): # Enter Key
            break

    return text

##------------------------------------------------------------------------------------
def find_human_idx(human_name, poses2d):
    idx = None ## human idx

    for i in range(len(poses2d)):
        if poses2d[i]['human_name'] == human_name:
            idx = i
            break

    return idx

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--image_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')

    args = parser.parse_args()
    # factor = 1.5 ## resize factor, the original image is too big
    factor = 0.8 ## resize factor, the original image is too big

    image_path = args.image_path
    save_path = args.output_path

    image_name = image_path.split('/')[-1]
    image_original = cv2.imread(image_path)
    image_original_width = image_original.shape[1]
    image_original_height = image_original.shape[0]

    image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)
    image = image_original_resized.copy()

    def click_event(event, x, y, flags, params):
        is_clicked = False

        # ----------------checking for left mouse clicks--------------
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            is_clicked = True
            if params['human_name'] is not None and params['keypoint_idx'] is not None and params['is_ongoing'] == True:
                idx = find_human_idx(params['human_name'], params['poses2d'])
                keypoint_idx = params['keypoint_idx']
                print('updating keypoint!')
                params['poses2d'][idx]['keypoints'][keypoint_idx, 0] = x
                params['poses2d'][idx]['keypoints'][keypoint_idx, 1] = y
                params['poses2d'][idx]['keypoints'][keypoint_idx, 2] = 1.0 ## if annotated by hand, 1 confidence
                params['canvas'] = params['image_original'].copy() ## refresh

        # ----------------checking for right mouse clicks--------------
        if event == cv2.EVENT_RBUTTONDOWN:
            is_clicked = True
            if params['human_name'] is not None and params['keypoint_idx'] is not None and params['is_ongoing'] == True:
                idx = find_human_idx(params['human_name'], params['poses2d'])
                keypoint_idx = params['keypoint_idx']
                print('deleting keypoint!')
                params['poses2d'][idx]['keypoints'][keypoint_idx, 2] = 0.0 ## if deleted by hand, confidence is 0
                params['canvas'] = params['image_original'].copy() ## refresh

        ##-------visualize the params['poses']----------
        if params['keypoint_idx'] is not None and is_clicked == True and params['is_ongoing'] == False:
            params['canvas'] = params['image_original'].copy() ## refresh
            params['human_name'] = None
            params['keypoint_idx'] = None

        params['canvas'] = draw_all_pose2d(params['canvas'], params['poses2d'])
        if params['human_name'] is not None:
            idx = find_human_idx(params['human_name'], params['poses2d'])
            color = params['poses2d'][idx]['color']


            if params['keypoint_idx'] is not None:
                keypoint_idx = params['keypoint_idx']
                point2d = params['poses2d'][idx]['keypoints'][keypoint_idx, :2]
                x1 = int(point2d[0])
                y1 = int(point2d[1])
                params['canvas'] = cv2.circle(params['canvas'], (x1, y1), 10, (0, 0, 255), 2)

        return

    window_title = '{}'.format(image_name)
    cv2.namedWindow(window_title)
    dummy_poses2d = [
            {'human_name': 'aria01', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            {'human_name': 'aria02', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            {'human_name': 'aria03', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            {'human_name': 'aria04', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            {'human_name': 'aria05', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            {'human_name': 'aria06', 'keypoints': np.zeros((17, 3)), 'color': [0, 255, 0]}, \
            ]

    params = {'poses2d': dummy_poses2d, 'human_name': None, \
            'keypoint_idx': None, \
            'is_ongoing': False, \
            'image_original': image_original_resized, 'canvas': image_original_resized.copy()}
    cv2.setMouseCallback(window_title, click_event, params)

    while True:
        cv2.imshow(window_title, params['canvas'])
        key = cv2.waitKey(5) & 0xFF

        ## refresh everything
        if key == ord("r"):
            params['canvas'] = image_original_resized.copy()
            params['human_name'] = None
            params['keypoint_idx'] = None
            params['is_ongoing'] = False

        elif key == ord("1") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria01'
            params['is_ongoing'] = True

        elif key == ord("2") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria02'
            params['is_ongoing'] = True

        elif key == ord("3") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria03'
            params['is_ongoing'] = True

        elif key == ord("4") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria04'
            params['is_ongoing'] = True

        elif key == ord("5") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria05'
            params['is_ongoing'] = True

        elif key == ord("6") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria06'
            params['is_ongoing'] = True

        elif key == ord("7") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria07'
            params['is_ongoing'] = True

        elif key == ord("8") and params['human_name'] is None and params['is_ongoing'] == False:
            params['human_name'] = 'aria08'
            params['is_ongoing'] = True

        ##---------------keypoints idx------------
        elif key == ord("a") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 0

        elif key == ord("b") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 1

        elif key == ord("c") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 2

        elif key == ord("d") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 3

        elif key == ord("e") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 4

        elif key == ord("f") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 5

        elif key == ord("g") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 6

        elif key == ord("h") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 7

        elif key == ord("i") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 8

        elif key == ord("j") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 9

        elif key == ord("k") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 10

        elif key == ord("l") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 11

        elif key == ord("m") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 12

        elif key == ord("n") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 13

        elif key == ord("o") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 14

        elif key == ord("p") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 15

        elif key == ord("q") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['keypoint_idx'] = 16

        elif key == ord("z") and params['human_name'] is not None and params['is_ongoing'] == True:
            params['is_ongoing'] = False
            params['human_name'] = None
            params['keypoint_idx'] = None

        ## escape
        elif key == 27:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    modified_poses2d = params['poses2d']
    for i in range(len(modified_poses2d)):
        modified_poses2d[i]['keypoints'][:, 0] *= factor
        modified_poses2d[i]['keypoints'][:, 1] *= factor

    poses2d = modified_poses2d.copy()

    image_original = draw_all_pose2d(image_original, poses2d)
    cv2.imwrite(save_path, image_original)

    print('done annotating')
        
    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()