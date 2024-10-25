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
    parser.add_argument('--testing_scale', action='store_true')
    args = parser.parse_args()
    sequence_path = args.sequence_path
    sequence_name = sequence_path.split('/')[-1]
    parent_sequence = sequence_name.split('_')[-1]
    config_file = os.path.join(_init_paths.root_path, 'configs', parent_sequence, '{}.yaml'.format(sequence_name))
    update_config(cfg, config_file)

    print('sequence at {}'.format(sequence_path))

    ## make cfg mutable
    cfg.defrost()
    cfg.CALIBRATION.LOAD_METRIC_SCALE_TRANSFORM = False
    cfg.freeze()
    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path)
    
    target_camera_name = 'cam{:02d}'.format(int(args.target_camera_name))
    time_stamp = int(args.timestamp)
    camera_names = ['cam{:02d}'.format(int(num)) for num in args.cameras.split(':')]

    camera_mode = 'rgb'
    factor = 3.0 ## resize factor, the original image is too big

    triangulator = Triangulator(scene.cfg, 1, [], [], [], [], {}, {})

    ###----------------------------------
    target_p1_p2_length_inch = 17.91338  #white tube is 36 inches
    target_p1_p2_length = target_p1_p2_length_inch*0.0254

    target_p3_p4_length_inch = 15.748 # 50.78        #48
    target_p3_p4_length = target_p3_p4_length_inch*0.0254

    target_p1 = np.zeros((3, ))
    target_p2 = np.array([0, 0, target_p1_p2_length])
    if not args.testing_scale:
        print('Please annotated four points')
        print('p1: origin of the coordinate system [0, 0, 0]')
        print('p2: end point of the z axis [0, 0, {}]'.format(target_p1_p2_length))
        print('p3: leg of any tripod')
        print('p4: top of the same tripod, distance between p3 and p4 is {} meters'.format(target_p3_p4_length))
    else:
        print('Testing mode:')
        print('Please annotated two points')
        print('p1: the first black point on one of the tripod leg')
        print('p2: the second black point on one of the tripod leg')

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
                # params['canvas'] = cv2.putText(params['canvas'], 'id:{}'.format(params['points_idx']), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
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
    # print(num_points)
    # input()
    ###--------------triangulate----------------
    points_3d = np.zeros((num_points, 3))
    for point_idx in range(num_points):

        proj_matricies = []
        points = []

        for camera_name in camera_names:
            camera = scene.cameras[(camera_name, camera_mode)]
            point_2d = points_2d[camera_name][point_idx]
            extrinsics = camera.extrinsics[:3, :] ## 3x4
            ray_3d = camera.cam_from_image(point_2d=point_2d) # in camera coordinate
            assert(len(ray_3d) == 3 and ray_3d[2] == 1)  
            point = ray_3d.copy()
            points.append(point)
            proj_matricies.append(extrinsics)

        point_3d, inlier_views, reprojection_error_vector = triangulator.triangulate_ransac(proj_matricies, points, \
                        n_iters=100, reprojection_error_epsilon=0.01, direct_optimization=True) # in world coordinate

        points_3d[point_idx, :] = point_3d[:]

    # ##------------------------------------------------------------------------------------
    # def compute_transformation(p1, p2, z_length=0.9144):
    #     # Translation vector to move p1 to the origin
    #     T_translate = np.eye(4)
    #     T_translate[:3, 3] = -p1

    #     # Direction vector from p1 to p2, normalized
    #     direction = (p2 - p1)
    #     direction_length = np.linalg.norm(direction)
    #     z_axis = direction / direction_length

    #     # Find two orthogonal vectors to define the new x and y axes
    #     x_axis = np.cross([0, 1, 0], z_axis)
    #     x_axis /= np.linalg.norm(x_axis)
    #     y_axis = np.cross(z_axis, x_axis)

    #     # Rotation matrix to align p2 with the z-axis
    #     R = np.eye(4)
    #     R[:3, :3] = np.vstack([x_axis, y_axis, z_axis]).T

    #     # Scale factor for the z-axis
    #     scale = z_length / direction_length
    #     S = np.eye(4)
    #     S[2, 2] = scale

    #     # The transformation matrix: first translate, then rotate and scale
    #     T = R @ S @ T_translate

    #     return T

    def compute_transformation(source_p1, source_p2, source_p3, source_p4, 
                           target_p1, target_p2, target_p1_p2_length, target_p3_p4_length):
    
        # Compute translation matrix
        T_translate = np.eye(4)
        T_translate[:3, 3] = -source_p1

        # Apply translation to source points
        source_p2_translated = source_p2 - source_p1
        source_p3_translated = source_p3 - source_p1
        source_p4_translated = source_p4 - source_p1

        # Compute scaling factor
        # source_p1_p2_length = np.linalg.norm(source_p2_translated)
        # scale_factor = target_p1_p2_length / source_p1_p2_length
        source_p3_p4_length = np.linalg.norm(source_p4_translated - source_p3_translated)
        scale_factor = target_p3_p4_length / source_p3_p4_length
        print(scale_factor)
        # Create scaling matrix
        T_scale = np.eye(4) * scale_factor
        T_scale[3, 3] = 1  # No scaling for the homogeneous coordinate

        # Apply scaling to translated source points
        source_p2_scaled = source_p2_translated * scale_factor
        source_p3_scaled = source_p3_translated * scale_factor
        source_p4_scaled = source_p4_translated * scale_factor

        # Compute rotation (assuming alignment along one axis for simplicity)
        # This part is ambiguous and may require additional constraints or methods
        # For now, we align p1-p2 of source and target
        target_direction = target_p2 - target_p1
        source_direction = source_p2_scaled

        target_direction /= np.linalg.norm(target_direction)
        source_direction /= np.linalg.norm(source_direction)

        # Compute the rotation matrix using axis-angle method
        # The cross product is the axis used for rotation.
        # The dot product gives us how much rotation is needed for the source direction to align with the tatget direction 
        # Reference: https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
        axis = np.cross(source_direction, target_direction)
        axis = axis / np.linalg.norm(axis)
        angle = np.arccos(np.dot(source_direction, target_direction))

        # Rodrigues' rotation formula
        K = np.array([[0, -axis[2], axis[1]],
                    [axis[2], 0, -axis[0]],
                    [-axis[1], axis[0], 0]])
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)

        # Extend R to 4x4 transformation matrix
        T_rotate = np.eye(4)
        T_rotate[:3, :3] = R

        # Combine transformations
        T = np.dot(T_rotate, np.dot(T_scale, T_translate))
        # T = np.dot(T_scale, np.dot(T_rotate, T_translate))
        
        return T

    ##------------------------------------------------------------------------------------
    print('points_3d in colmap frame')

    points_3d_colmap = linear_transform(points_3d, scene.primary_transform) # Apply transform (this is still in colmap coordinate system, primary transform is identity matrix)

    if args.testing_scale:
        scale = np.load(f'{args.sequence_path}/colmap/workplace/scale.npy', allow_pickle=True)
        points_3d_test = linear_transform(points_3d_colmap, scale) # Apply scale transform
        print('points after scaling:', points_3d_test)
        print('points distance are:',np.linalg.norm(points_3d_test[0] - points_3d_test[1]))
        input("You are in testing mode. The distance between two fixed points on the tripod should be 30cm.")

    ## assert the transform is np.eye(4)
    assert(np.allclose(scene.primary_transform, np.eye(4)))
    print(repr(points_3d_colmap)); print()
    # input()
    ##------------------------------------------------------------------------------------
    # Using the compute_transformation function to get the transformation matrix
    source_p1 = points_3d_colmap[0, :]
    source_p2 = points_3d_colmap[1, :]
    source_p3 = points_3d_colmap[2, :]
    source_p4 = points_3d_colmap[3, :]

    T = compute_transformation(source_p1, source_p2, source_p3, source_p4, target_p1, target_p2, target_p1_p2_length, target_p3_p4_length)
    # input()
    # Apply transformation to p1, p2, p3, p4
    target_p1_transformed = (T @ np.append(target_p1, 1))[:3]
    target_p2_transformed = (T @ np.append(target_p2, 1))[:3]
    target_p3_transformed = (T @ np.append(source_p3, 1))[:3]
    target_p4_transformed = (T @ np.append(source_p4, 1))[:3]

    transformed_points_3d = np.zeros((num_points, 3))
    for idx in range(num_points):
        transformed_points_3d[idx, :] = (T @ np.append(points_3d_colmap[idx, :], 1))[:3]

    # Errors after transformation
    error_1 = np.linalg.norm(target_p1_transformed - target_p1)
    error_2 = np.linalg.norm(target_p2_transformed - target_p2)

    print('Transformation matrix T:\n', T)
    print('Transformed target_p1: {}, error: {}'.format(target_p1_transformed, error_1))
    print('Transformed target_p2: {}, error: {}'.format(target_p2_transformed, error_2))

    # Save the transformation matrix to disk
    np.save(os.path.join(scene.colmap_dir, 'scale.npy'), T)

    ##---------------------------visualization-------------------------------------------
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
    
    ##------------------------------------------------------------------------------------
    print('labelled points_2d for target camera')        
    print(repr(points_2d[target_camera_name])); print()

    print('projected points_2d (has error) for target camera')        
    print(repr(target_projected_points_2d)); print()

    ##------------------------------------------------------------------------------------
    ## verify if the transformation is correct
    cfg.defrost()
    cfg.CALIBRATION.LOAD_METRIC_SCALE_TRANSFORM = True
    cfg.freeze()

    scene = EgoExoScene(cfg=cfg, root_dir=sequence_path) ## reload the scene with the new cfg
    scene.update(time_stamp=t)

    for camera_name in camera_names + [target_camera_name]:
        camera = scene.cameras[(camera_name, camera_mode)]
        image_path = camera.get_image_path(time_stamp=t)
        image = cv2.imread(image_path)

        projected_points_2d = camera.vec_project(transformed_points_3d)

        if camera_name == target_camera_name:
            target_projected_points_2d = projected_points_2d

        for idx in range(num_points):
            image = cv2.circle(image, (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1])), 10, (0, 0, 255), -1)
            image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(projected_points_2d[idx, 0]), round(projected_points_2d[idx, 1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

        ## visualize the X, Y, Z axis
        extra_points_3d = np.zeros((4, 3))
        extra_points_3d[0, :] = np.array([0, 0, 0])
        extra_points_3d[1, :] = np.array([1, 0, 0]) ## X axis
        extra_points_3d[2, :] = np.array([0, 1, 0]) ## Y axis
        extra_points_3d[3, :] = np.array([0, 0, 1]) ## Z axis

        extra_points_2d = camera.vec_project(extra_points_3d)

        ## draw x axis in red, y axis in green, z axis in blue
        image = cv2.line(image, (round(extra_points_2d[0, 0]), round(extra_points_2d[0, 1])), (round(extra_points_2d[1, 0]), round(extra_points_2d[1, 1])), (0, 0, 255), 5)
        image = cv2.line(image, (round(extra_points_2d[0, 0]), round(extra_points_2d[0, 1])), (round(extra_points_2d[2, 0]), round(extra_points_2d[2, 1])), (0, 255, 0), 5)
        image = cv2.line(image, (round(extra_points_2d[0, 0]), round(extra_points_2d[0, 1])), (round(extra_points_2d[3, 0]), round(extra_points_2d[3, 1])), (255, 0, 0), 5)

        ## also draw a unit sphere
        unit_sphere_3d = np.zeros((100, 3))
        for idx in range(100):
            theta = 2*np.pi*idx/100
            unit_sphere_3d[idx, 0] = np.cos(theta)
            unit_sphere_3d[idx, 1] = np.sin(theta)
            unit_sphere_3d[idx, 2] = 0
        
        unit_sphere_2d = camera.vec_project(unit_sphere_3d)

        for idx in range(100):
            image = cv2.circle(image, (round(unit_sphere_2d[idx, 0]), round(unit_sphere_2d[idx, 1])), 5, (0, 0, 255), -1)

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

    return


##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()