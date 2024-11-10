import mmcv
from mmcv.image import imwrite
import numpy as np
import cv2

#Reference https://github.com/open-mmlab/mmpose/blob/0.x/mmpose/models/detectors/top_down.py#L226
def show_result(img,
                result,
                kpt_score_thr=0.3,
                bbox_color='green',
                text_color='white',
                radius=4,
                thickness=1,
                font_scale=0.5,
                bbox_thickness=1,
                win_name='',
                show=False,
                show_keypoint_weight=False,
                wait_time=0,
                out_file=None):
    """Draw `result` over `img`.

    Args:
        img (str or Tensor): The image to be displayed.
        result (list[dict]): The results to draw over `img`
            (bbox_result, pose_result).
        skeleton (list[list]): The connection of keypoints.
            skeleton is 0-based indexing.
        kpt_score_thr (float, optional): Minimum score of keypoints
            to be shown. Default: 0.3.
        bbox_color (str or tuple or :obj:`Color`): Color of bbox lines.
        pose_kpt_color (np.array[Nx3]`): Color of N keypoints.
            If None, do not draw keypoints.
        pose_link_color (np.array[Mx3]): Color of M links.
            If None, do not draw links.
        text_color (str or tuple or :obj:`Color`): Color of texts.
        radius (int): Radius of circles.
        thickness (int): Thickness of lines.
        font_scale (float): Font scales of texts.
        win_name (str): The window name.
        show (bool): Whether to show the image. Default: False.
        show_keypoint_weight (bool): Whether to change the transparency
            using the predicted confidence scores of keypoints.
        wait_time (int): Value of waitKey param.
            Default: 0.
        out_file (str or None): The filename to write the image.
            Default: None.

    Returns:
        Tensor: Visualized img, only if not `show` or `out_file`.
    """
    img = mmcv.imread(img)
    img = img.copy()

    bbox_result = []
    bbox_labels = []
    pose_result = []
    for res in result:
        if 'bbox' in res:
            bbox_result.append(res['bbox'])
            bbox_labels.append(res.get('label', None))
        pose_result.append(res['keypoints'])

    if pose_result:
        # Reference: https://github.com/open-mmlab/mmpose/blob/0.x/mmpose/apis/inference.py#L544
        palette = np.array([[255, 128, 0], [255, 153, 51], [255, 178, 102],
                            [230, 230, 0], [255, 153, 255], [153, 204, 255],
                            [255, 102, 255], [255, 51, 255], [102, 178, 255],
                            [51, 153, 255], [255, 153, 153], [255, 102, 102],
                            [255, 51, 51], [153, 255, 153], [102, 255, 102],
                            [51, 255, 51], [0, 255, 0], [0, 0, 255],
                            [255, 0, 0], [255, 255, 255]])

        skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], [11, 12],
                    [5, 11], [6, 12], [5, 6], [5, 7], [6, 8], [7, 9],
                    [8, 10], [1, 2], [0, 1], [0, 2],
                    [1, 3], [2, 4], [3, 5], [4, 6], [15, 17], [15, 18],
                    [15, 19], [16, 20], [16, 21], [16, 22], [91, 92],
                    [92, 93], [93, 94], [94, 95], [91, 96], [96, 97],
                    [97, 98], [98, 99], [91, 100], [100, 101], [101, 102],
                    [102, 103], [91, 104], [104, 105], [105, 106],
                    [106, 107], [91, 108], [108, 109], [109, 110],
                    [110, 111], [112, 113], [113, 114], [114, 115],
                    [115, 116], [112, 117], [117, 118], [118, 119],
                    [119, 120], [112, 121], [121, 122], [122, 123],
                    [123, 124], [112, 125], [125, 126], [126, 127],
                    [127, 128], [112, 129], [129, 130], [130, 131],
                    [131, 132]]

        pose_link_color = palette[[
            0, 0, 0, 0, 7, 7, 7, 9, 9, 9, 9, 9, 16, 16, 16, 16, 16, 16, 16
        ] + [16, 16, 16, 16, 16, 16] + [
            0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 16, 16, 16,
            16
        ] + [
            0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 16, 16, 16,
            16
        ]]
        
        pose_kpt_color = palette[
            [16, 16, 16, 16, 16, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0] +
            [0, 0, 0, 0, 0, 0] + [19] * (68 + 42)]

        imshow_keypoints(img, pose_result, skeleton, kpt_score_thr,
                            pose_kpt_color, pose_link_color, radius,
                            thickness)

    if show:
        imshow(img, win_name, wait_time)

    if out_file is not None:
        imwrite(img, out_file)

    return img

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
