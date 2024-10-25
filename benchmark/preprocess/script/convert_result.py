import os
import argparse
import numpy as np
import torch

import pyrender
import trimesh

import smplx
# from smplx.joint_names import Body

from tqdm.auto import tqdm, trange

from pathlib import Path
import pickle

from load_prediction import load_multihmr_prediction
# Given bev output, and buddi output
# 1. load multihmr output 
# 2. For each verts in multihmr output, convert to smpl vertices
# 3. use regressor_extra to get 3d joints V
# 4. mapping 2d joints V
# 5. store converted smpl vertices, 3d joints, 2d joints in the format below: {verts, 3djoints, 2djoints}

# Load BEV output
# /media/rawalk/disk1/rawalk/datasets/ego_exo/main/inference/multihmr_inference/13_hugging/002_hugging/exo/cam01/images
prediction_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/inference/multihmr_inference' #/13_hugging/002_hugging/exo/cam01/images'
output_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/inference/multihmr_inference'
def main(args):

    multihmr_prediction_path = os.path.join(prediction_dir, args.big_sequence, args.sequence, 'exo', args.cam, 'images')
    multihmr_pred = load_multihmr_prediction(multihmr_prediction_path)

    final_pred_dir = os.path.join(output_dir, args.big_sequence, args.sequence, 'exo', args.cam)
    final_pred_path = os.path.join(final_pred_dir, 'final_pred.npy')
    np.save(final_pred_path, multihmr_pred, allow_pickle=True)
    
    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--big_sequence', type=str, default='13_hugging')
    parser.add_argument('--sequence', type=str, default='002_hugging')
    parser.add_argument('--cam', type=str, default='cam01')
    args = parser.parse_args()
    main(args = args)



