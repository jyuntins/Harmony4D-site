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

from load_prediction import load_bev_prediction, load_buddi_prediction, combine_predictions
# Given bev output, and buddi output
# 1. load bev output V
# 2. convert bev output to the format below:{verts, 3djoints, 2djoints} V
# 3. load buddi output V
# 4. use buddi output reconstruct smplx vertices V
# 5. convert smplx to smpl vertices V
# 6. use regressor_extra to get 3d joints V
# 7. mapping 2d joints V
# 6. store converted smpl vertices, 3d joints, 2d joints in the format below: {verts, 3djoints, 2djoints}

# Load BEV output
prediction_dir = '/home/rawalk/Desktop/ego/buddi/benchmark_preprocess/prediction'

# smplx2smpl_path = "/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/data/utils/smplx2smpl.pkl"
# smplx2smpl = pickle.load(open(smplx2smpl_path, 'rb'))
# smplx2smpl = torch.tensor(smplx2smpl['matrix'][None], dtype=torch.float32).cuda()

# batch_size = 1
# buddi_output_filepath = '/home/rawalk/Desktop/ego/buddi/demo/optimization/buddi_cond_bev_demo_live/fit_buddi_cond_bev_flickrci3ds/results/00230.pkl'
# smplx.create()
# smplx_vertices = np.load('buddi_output_filepath', allow_pickle=True)['']
# pred_cam_vertices = torch.matmul(smplx2smpl.repeat(batch_size, 1, 1), smplx_vertices)


def main(args):

    bev_prediction_path = os.path.join(prediction_dir, args.big_sequence, args.sequence, args.cam, 'bev')    
    bev_pred = load_bev_prediction(bev_prediction_path)
    buddi_prediction_path = os.path.join(prediction_dir, args.big_sequence, args.sequence, args.cam, 'buddi')
    buddi_pred = load_buddi_prediction(buddi_prediction_path)
    final_pred = combine_predictions(bev_pred, buddi_pred)
    final_pred_dir = os.path.join(prediction_dir, args.big_sequence, args.sequence, args.cam, 'final')
    final_pred_path = os.path.join(final_pred_dir, 'final_pred.npy')
    np.save(final_pred_path, final_pred, allow_pickle=True)
    
    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--big_sequence', type=str, default='31_mma')
    parser.add_argument('--sequence', type=str, default='003_mma')
    parser.add_argument('--cam', type=str, default='cam05')
    args = parser.parse_args()
    main(args = args)



