from load_prediction import load_multihmr_prediction
import argparse
import os
import numpy as np
from vis_utils import visualize_vertices, visualize_keypoints_3d, visualize_keypoints_2d

prediction_dir = '/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/benchmark_preprocess/multihmr/prediction'

def main(args):

    if args.method == 'multihmr':
        multihmr_prediction_path = os.path.join(prediction_dir, args.big_sequence, args.sequence, args.cam)
        pred = load_multihmr_prediction(multihmr_prediction_path)
        # breakpoint()
    if args.mode == 'vertices':
        vertices = pred['vertices']
        visualize_vertices(vertices)

    elif args.mode == 'keypoints_3d':
        keypoints_3d = pred['keypoints_3d']
        visualize_keypoints_3d(keypoints_3d)

    elif args.mode == 'keypoints_2d':
        keypoints_2d = pred['keypoints_2d']
        visualize_keypoints_2d(keypoints_2d)

    else:
        print('Invalid mode')

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--big_sequence', type=str, default='31_mma')
    parser.add_argument('--sequence', type=str, default='003_mma')
    parser.add_argument('--cam', type=str, default='cam05')
    parser.add_argument('--method', type=str, default='multihmr')
    parser.add_argument('--mode', type=str, default='vertices', help = 'vertices, keypoints_3d, keypoints_2d')
    args = parser.parse_args()
    main(args = args)



