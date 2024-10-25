import _init_paths
import numpy as np
import os
import argparse
import cv2

from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config
from utils.transforms import linear_transform
from utils.triangulation import Triangulator
from scipy.optimize import fsolve, least_squares

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--sequence_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--output_path', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--target_camera_name', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--cameras', action='store', help='the path to the sequence for visualization')
    parser.add_argument('--timestamp', action='store', help='the path to the sequence for visualization')

    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    print('sequence at {}'.format(sequence_path))

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)

    target_camera_name = 'cam{:02d}'.format(int(args.target_camera_name))
    time_stamp = int(args.timestamp)
    camera_names = ['cam{:02d}'.format(int(num)) for num in args.cameras.split(':')]

    camera_mode = 'rgb'
    factor = 3.0 ## resize factor, the original image is too big

    triangulator = Triangulator(scene.cfg, 1, [], [], [], [], {}, {})


    ###----------------------------------

    print('Please annotated the top and the bottom three points of a fully stretched tripod in the camera images')
    print('p1: top of the tripod')
    print('p2: bottom left of the tripod')
    print('p3: bottom center of the tripod')
    print('p4: bottom right of the tripod')

    t = time_stamp
    scene.update(time_stamp=t)
    points_2d = {}

    for camera_name in camera_names + [target_camera_name]:
        camera = scene.cameras[(camera_name, camera_mode)]

        image_path = camera.get_image_path(time_stamp=t)
        image_original = cv2.imread(image_path)
        image_original_width = image_original.shape[1]
        image_original_height = image_original.shape[0]

        image_original_resized = cv2.resize(image_original, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)
        image = image_original_resized.copy()

        ###------------------------------------------------------------------------------------
        def click_event(event, x, y, flags, params):
            # ----------------checking for left mouse clicks--------------
            if event == cv2.EVENT_LBUTTONDOWN:
                params['points_idx'] += 1
                cv2.circle(params['canvas'], (x, y), 5, (0, 0, 255), -1)
                params['canvas'] = cv2.putText(params['canvas'], 'id:{}'.format(params['points_idx']), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                params['points'].append((x, y))

            return

        ###------------------------------------------------------------------------------------
        window_title = '{}-{}'.format(camera_name, t)
        cv2.namedWindow(window_title)
        params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}
        cv2.setMouseCallback(window_title, click_event, params)

        while True:
            cv2.imshow(window_title, params['canvas'])
            key = cv2.waitKey(5) & 0xFF

            ## refresh everything
            if key == ord("r"):
                params = {'points_idx': 0, 'points':[], 'image_original': image_original_resized, 'canvas': image_original_resized.copy()}

            ## escape
            elif key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        camera_points_2d = np.zeros((len(params['points']), 2))
        for idx, point in enumerate(params['points']):
            camera_points_2d[idx, 0] = point[0]*factor 
            camera_points_2d[idx, 1] = point[1]*factor

        points_2d[camera_name] = camera_points_2d

    num_points = len(points_2d[camera_names[0]])
    print('num_points:', num_points)
    print(points_2d)
    input()
    ###--------------triangulate----------------
    points_3d = np.zeros((num_points, 3))
    for point_idx in range(num_points):

        proj_matricies = []
        points = []

        for camera_name in camera_names:
            camera = scene.cameras[(camera_name, camera_mode)]
            point_2d = points_2d[camera_name][point_idx]
            extrinsics = camera.extrinsics[:3, :] ## 3x4
            ray_3d = camera.cam_from_image(point_2d=point_2d)
            print(ray_3d)
            # input()
            assert(len(ray_3d) == 3 and ray_3d[2] == 1)  
            point = ray_3d.copy()
            points.append(point)
            proj_matricies.append(extrinsics)

        point_3d, inlier_views, reprojection_error_vector = triangulator.triangulate_ransac(proj_matricies, points, \
                        n_iters=100, reprojection_error_epsilon=0.01, direct_optimization=True)
        
        points_3d[point_idx, :] = point_3d[:]
    print("points3d", points_3d)
    input()
    ##-----------reproject---------------
    target_projected_points_2d = None
    for camera_name in camera_names + [target_camera_name]:
        camera = scene.cameras[(camera_name, camera_mode)]
        image_path = camera.get_image_path(time_stamp=t)
        image = cv2.imread(image_path)

        projected_points_2d = camera.vec_project(points_3d)

        if camera_name == target_camera_name:
            target_projected_points_2d = projected_points_2d

        for idx in range(num_points):
            image = cv2.circle(image, (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1])), 10, (0, 0, 255), -1)
            image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

        window_title = '{}-{}'.format(camera_name, t)

        if camera_name == target_camera_name:
            window_title += '---target!'

        cv2.namedWindow(window_title)
        image_resized = cv2.resize(image, (int(image_original_width/factor), int(image_original_height/factor)), interpolation=cv2.INTER_AREA)

        while True:
            cv2.imshow(window_title, image_resized)
            key = cv2.waitKey(5) & 0xFF

            if key == 27:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print('points_3d in colmap frame')
    print("primary_transform:", scene.primary_transform)
    points_3d_colmap = linear_transform(points_3d, scene.primary_transform)
    print(repr(points_3d_colmap)); print()

    print('labelled points_2d for target camera')        
    print(repr(points_2d[target_camera_name])); print()

    print('projected points_2d (has error) for target camera')        
    print(repr(target_projected_points_2d)); print()

    ##-----------------compute scale factor-----------------
    ## tripod leg is 45 inches which is 1.143 meters

    metric_tripod_length = 1.143


    ## geometry processing
    p1 = points_3d_colmap[0, :] #top of tripod
    p2 = points_3d_colmap[1, :] #left bottom of tripod
    p3 = points_3d_colmap[2, :] #center bottom of tripod
    p4 = points_3d_colmap[3, :] #right bottom of tripod

    # compute the vectors from p1 to p2, p1 to p3, and p1 to p4
    v12 = p2 - p1
    v13 = p3 - p1
    v14 = p4 - p1


    # scale the data
    scale = np.linalg.norm(v12)
    v12 /= scale
    v13 /= scale
    v14 /= scale
    metric_tripod_length /= scale

    # function to compute the difference between the computed length of v_prime and the actual length
    def func(x):
        sx, sy, sz = x
        v_prime_12 = np.array([v12[0]*sx, v12[1]*sy, v12[2]*sz])
        v_prime_13 = np.array([v13[0]*sx, v13[1]*sy, v13[2]*sz])
        v_prime_14 = np.array([v14[0]*sx, v14[1]*sy, v14[2]*sz])
        return [np.linalg.norm(v_prime_12) - metric_tripod_length,
                np.linalg.norm(v_prime_13) - metric_tripod_length,
                np.linalg.norm(v_prime_14) - metric_tripod_length,
                0.1*(sx**2 + sy**2 + sz**2 - 3)]  # regularization term

    # initial guess for the scale factors
    x0 = [1, 1, 1]

    # bounds for the scale factors
    bounds = [(0.1, 10), (0.1, 10), (0.1, 10)]

    # solve for the scale factors
    res = least_squares(func, x0, bounds=np.transpose(np.array(bounds)))

    sx, sy, sz = res.x

    # compute the error
    v_prime_12 = np.array([v12[0]*sx, v12[1]*sy, v12[2]*sz])
    v_prime_13 = np.array([v13[0]*sx, v13[1]*sy, v13[2]*sz])
    v_prime_14 = np.array([v14[0]*sx, v14[1]*sy, v14[2]*sz])
    error_12 = np.abs(np.linalg.norm(v_prime_12) - metric_tripod_length)
    error_13 = np.abs(np.linalg.norm(v_prime_13) - metric_tripod_length)
    error_14 = np.abs(np.linalg.norm(v_prime_14) - metric_tripod_length)

    # scale back the data
    v12 *= scale
    v13 *= scale
    v14 *= scale
    metric_tripod_length *= scale

    # create the transformation matrix
    T = np.array([[sx, 0, 0, 0],
                [0, sy, 0, 0],
                [0, 0, sz, 0],
                [0, 0, 0, 1]])

    # transform the points to the metric coordinate system
    points_3d_metric = np.dot(points_3d_colmap, T[:3,:3].T)

    # save the transformation matrix to disk
    np.save(os.path.join(scene.colmap_dir, 'scale.npy'), T)

    print("Scale factor in x direction:", sx)
    print("Scale factor in y direction:", sy)
    print("Scale factor in z direction:", sz)
    print("Error for p1 to p2:", error_12)
    print("Error for p1 to p3:", error_13)
    print("Error for p1 to p4:", error_14)


    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()