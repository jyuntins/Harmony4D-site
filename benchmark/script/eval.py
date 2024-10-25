import os
import numpy as np
import pickle as pkl
import joblib
import argparse
from utils import *
import torch
from tqdm import tqdm
import hydra
from omegaconf import DictConfig, OmegaConf
import time
import sys
sys.path.append('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation')

import glob
import cv2
import sys
from SMPL import SMPLModel
from collision import penetration, solid_intersection_volume
from harmony4d_evaluate import evaluation, evaluation_buddi
from load_prediction import load_hmr2_prediction, load_romp_prediction, load_bev_prediction, load_pare_prediction, load_multihmr_prediction, load_buddi_prediction
from load_ground_truth import load_ground_truth

PCK_THRESH = 50.0
AUC_MIN = 0.0
AUC_MAX = 200.0

SMPL_NR_JOINTS = 24

SMPL_MAJOR_JOINTS = np.array([1, 2, 4, 5, 7, 8, 16, 17, 18, 19, 20, 21])


@hydra.main(config_path='../config', config_name='config', version_base=None)
def main(cfg:DictConfig):
    print(OmegaConf.to_yaml(cfg))
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--method', type=str, default='hmr2', help='[hmr2, pare, romp, bev, multihmr, buddi]')
    # parser.add_argument('--big_sequence', type=str, default='13_hugging')
    # parser.add_argument('--sequence', type=str, default='002_hugging')
    # parser.add_argument('--output_dir', type=str, default='../evaluation_result')
    # args = parser.parse_args()

    method = cfg.method
    big_sequence = cfg.big_sequence
    sequence = cfg.sequence
    output_dir = cfg.output_dir
    # Load Ground Truth    
    ground_truth_root_dir = cfg.path.ground_truth_path
    ground_truth_dir = os.path.join(ground_truth_root_dir, big_sequence, sequence, 'processed_data')
    ground_truth = load_ground_truth(ground_truth_dir)

    # Load Prediction Data
    prediction_root_dir = cfg.path.predictions_path
    prediction_dir = os.path.join(prediction_root_dir, method+'_inference', big_sequence, sequence, 'exo')

    # prepare smpl faces to build smpl
    smpl_faces_path = cfg.path.smpl_faces_path

    # Evaluate
    if method == 'hmr2':
        prediction = load_hmr2_prediction(prediction_dir)
        eval_metric = evaluation(ground_truth, prediction, smpl_faces_path)

    elif method == 'finetuned_hmr2':
        prediction = load_hmr2_prediction(prediction_dir)
        eval_metric = evaluation(ground_truth, prediction, smpl_faces_path)

    elif method == 'pare':
        prediction = load_pare_prediction(prediction_dir)
        eval_metric = evaluation(ground_truth, prediction, smpl_faces_path, compute_collision=True)

    elif method == 'romp':
        prediction = load_romp_prediction(prediction_dir)
        eval_metric = evaluation(ground_truth, prediction, smpl_faces_path)

    elif method == 'bev':
        prediction = load_bev_prediction(prediction_dir)
        eval_metric = evaluation(ground_truth, prediction, smpl_faces_path, compute_collision=True)

    elif method == 'multihmr':
        prediction = load_multihmr_prediction(prediction_dir)
        eval_metric = evaluation_buddi(ground_truth, prediction, smpl_faces_path, compute_collision=True)

    elif method == 'buddi':
        prediction_dir = os.path.join(prediction_root_dir, 'buddi_inference', 'testing', big_sequence, sequence, 'exo')
        prediction = load_buddi_prediction(prediction_dir)
        eval_metric = evaluation_buddi(ground_truth, prediction, smpl_faces_path, compute_collision=True)

    else:
        raise ValueError('Invalid method')
    
    output_dir = os.path.join(output_dir, method, big_sequence, sequence)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'result.npy')
    np.save(output_path, eval_metric, allow_pickle=True)
    print("********************************************")
    print("eval_metric:", eval_metric)
    print()
    print("********************************************")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print('Total time taken: ', time.time() - start_time)