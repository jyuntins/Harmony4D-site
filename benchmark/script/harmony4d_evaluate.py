import os
import numpy as np
import pickle as pkl
import joblib
import argparse
from utils import *
import torch
from tqdm import tqdm

import glob
import cv2
import sys
from SMPL import SMPLModel
from collision import penetration, solid_intersection_volume

PCK_THRESH = 50.0
AUC_MIN = 0.0
AUC_MAX = 200.0
NUM_SEQS = 87

SMPL_NR_JOINTS = 24

SMPL_MAJOR_JOINTS = np.array([1, 2, 4, 5, 7, 8, 16, 17, 18, 19, 20, 21])


def evaluation_buddi(ground_truth, prediction, smpl_faces_path, compute_collision=False):
    gt_cam_set = set(ground_truth.keys())
    pred_cam_set = set(prediction.keys())
    evaluated_cam_set = gt_cam_set.intersection(pred_cam_set)
    evaluated_cam_set = sorted(list(evaluated_cam_set))
    aria_human_names = ['aria01', 'aria02']
    sequence_length = len(ground_truth['cam01']['aria01'])

    count = sequence_length * 2

    smpl_model_faces = np.load(smpl_faces_path)

    eval_metric = {}
    for cam in evaluated_cam_set:
        gt = ground_truth[cam]
        pred = prediction[cam]

        MPJPEs, PA_MPJPEs, MPVPEs, PA_MPVPEs, PCKs, AUCs = [], [], [], [], [], []

        miss = 0

        max_gt_penetr_val, max_pred_penetr_val = 0, 0
        max_gt_penetr_timestamp, max_pred_penetr_timestamp = 0, 0

        for timestamp in tqdm(range(sequence_length)): 
            breakpoint()
            gt_2d_kps = [ground_truth[cam][aria_human][timestamp]['2d_joints'] for aria_human in aria_human_names]
            pred_2d_kps = list(pred['keypoints_2d'][timestamp])

            np.save('../testing/multihmr2d/gt2d.npy', np.array(gt_2d_kps), allow_pickle=True)
            np.save('../testing/multihmr2d/pred2d.npy', np.array(pred_2d_kps), allow_pickle=True)
            bestMatch, falsePositives, misses = match_2d_greedy(pred_2d_kps, gt_2d_kps) 
            # breakpoint()
            miss += len(misses)

            aria1_gt_vertices, aria1_pred_vertices = np.zeros((6890, 3)), np.zeros((6890, 3))
            aria2_gt_vertices, aria2_pred_vertices = np.zeros((6890, 3)), np.zeros((6890, 3))
            
            for i, pair in enumerate(bestMatch):
                ####################Testing 2D joints####################
                # if pair[1] == 1:
                #     np.save('../testing/4dhumans2d/pred/{:05d}.npy'.format(timestamp), pred_2d_kps[pair[0]], allow_pickle=True)
                #     np.save('../testing/4dhumans2d/gt/{:05d}.npy'.format(timestamp), gt_2d_kps[pair[1]], allow_pickle=True)
                ####################Testing 3D joints####################
                # np.save('debug/harmony4d/3d_joints/aria1_pred_3d_joints', pred['3d_joints'][timestamp][pair[0]][:, :], allow_pickle=True)
                # np.save('debug/harmony4d/3d_joints/aria1_gt_3d_joints',gt[aria_human_names[pair[1]]][timestamp]['cam_3d_joints'][:, :], allow_pickle=True)
                ####################Initialize smpl model to get 3d joints##############

                ### Prediction ###
                # pose_params = pred['body_pose'][timestamp][pair[0]]
                # pose_params = np.expand_dims(pose_params, axis=0) # batch

                # shape_params = pred['betas'][timestamp][pair[0]].reshape(-1, 10)
                # cam_params = pred['camera_translations'][timestamp][pair[0]].reshape(-1, 3)

                # pred_vertices, pred_3d_joints = smpl_model.get_vertices_and_joints(torch.from_numpy(shape_params).to('cuda'), torch.from_numpy(pose_params).to('cuda'), torch.from_numpy(cam_params).to('cuda'))
                pred_vertices = pred['vertices'][timestamp][pair[0]]
                pred_3d_joints = pred['keypoints_3d'][timestamp][pair[0]]

                ###Ground Truth###
                cam_gt_vertices = gt[aria_human_names[pair[1]]][timestamp]['cam_smpl_vertices']
                cam_gt_3d_joints = gt[aria_human_names[pair[1]]][timestamp]['cam_3d_joints']

                # compute MPJPE and PA-MPJPE, MVE and PA-MVE
                pred_3d_joints = np.expand_dims(pred_3d_joints[:24, :], axis=0)
                pred_vertices = np.expand_dims(pred_vertices, axis=0)
                cam_gt_3d_joints = np.expand_dims(cam_gt_3d_joints[:24, :], axis=0)
                cam_gt_vertices = np.expand_dims(cam_gt_vertices, axis=0)
                if pair[1] == 1:
                    np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_pred_3d_joints', pred_3d_joints[0, :24, :], allow_pickle=True)
                    np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_gt_3d_joints',cam_gt_3d_joints[0], allow_pickle=True)
                breakpoint()
                MPJPE, PA_MPJPE, MPVPE, PA_MPVPE, PCK, AUC = compute_errors(pred_3d_joints[:, :24, :], cam_gt_3d_joints, pred_vertices, cam_gt_vertices)

                MPJPEs.append(MPJPE)
                PA_MPJPEs.append(PA_MPJPE)
                MPVPEs.append(MPVPE)
                PA_MPVPEs.append(PA_MPVPE)
                PCKs.append(PCK)
                AUCs.append(AUC)

                if pair[1] == 0:
                    # aria1_gt_vertices = cam_gt_vertices[0]
                    aria1_pred_vertices = pred_vertices[0]
                if pair[1] == 1:
                    # aria2_gt_vertices = cam_gt_vertices[0]
                    aria2_pred_vertices = pred_vertices[0]

            if compute_collision and len(bestMatch) == 2: # if we want to compute collision and if the method reconstruct both people, compute penetration and intersection
                # compute pred penetration
                pred_penetr_val1, n_inside_vertices = penetration(aria1_pred_vertices, smpl_model_faces, aria2_pred_vertices, mode="max")
                pred_penetr_val2, n_inside_vertices = penetration(aria2_pred_vertices, smpl_model_faces, aria1_pred_vertices, mode="max")
                pred_penetr_val = max(pred_penetr_val1, pred_penetr_val2)
                if pred_penetr_val > max_pred_penetr_val:
                    max_pred_penetr_val = pred_penetr_val
                    max_pred_penetr_timestamp = timestamp

            if compute_collision:
                # compute gt penetration
                aria1_gt_vertices = gt[aria_human_names[0]][timestamp]['cam_smpl_vertices']
                aria2_gt_vertices = gt[aria_human_names[1]][timestamp]['cam_smpl_vertices']
                gt_penetr_val1, n_inside_vertices = penetration(aria1_gt_vertices, smpl_model_faces, aria2_gt_vertices, mode="max")
                gt_penetr_val2, n_inside_vertices = penetration(aria2_gt_vertices, smpl_model_faces, aria1_gt_vertices, mode="max")
                gt_penetr_val = max(gt_penetr_val1, gt_penetr_val2)
                if gt_penetr_val > max_gt_penetr_val:
                    max_gt_penetr_val = gt_penetr_val
                    max_gt_penetr_timestamp = timestamp
            # if timestamp == 202:
            #     np.save('../testing/multihmr_col/aria1_pred_vertices.npy', aria1_pred_vertices, allow_pickle=True)
            #     np.save('../testing/multihmr_col/aria2_pred_vertices.npy', aria2_pred_vertices, allow_pickle=True)
            #     breakpoint()

        # Compute MPJPE, PA-MPJPE, MPVPE, PA-MPVPE, PCK, AUC
        mpjpe = np.mean(np.array(MPJPEs))
        pa_mpjpe = np.mean(np.array(PA_MPJPEs))
        mpvpe = np.mean(np.array(MPVPEs))
        pa_mpvpe = np.mean(np.array(PA_MPVPEs))
        pck = np.mean(np.array(PCKs))
        auc = np.mean(np.array(AUCs))

        # Compute Precision, Recall, F1 
        precision, recall, f1 = compute_prf1(count, miss, 0) # There is no scenario of false positive, since in our scenario we don't have negative labels.

        # Compute NMJE and NMVE
        nmje = mpjpe/f1
        nmve = mpvpe/f1

        eval_metric[cam] = {'MPJPE': mpjpe, 'PA_MPJPE': pa_mpjpe, 'MPVPE': mpvpe, 'PA_MPVPE': pa_mpvpe, 'PCK': pck, 'AUC': auc, 'Precision': precision, 'Recall': recall, 'F1': f1, 'NMJE': nmje, 'NMVE': nmve, 'sequence_length': sequence_length, 'miss': miss}
        if compute_collision:
            eval_metric[cam]['max_gt_penetr_val'] = max_gt_penetr_val
            eval_metric[cam]['max_gt_penetr_timestamp'] = max_gt_penetr_timestamp
            eval_metric[cam]['max_pred_penetr_val'] = max_pred_penetr_val
            eval_metric[cam]['max_pred_penetr_timestamp'] = max_pred_penetr_timestamp
    return eval_metric


def evaluation(ground_truth, prediction, smpl_faces_path, compute_collision=False):
    gt_cam_set = set(ground_truth.keys())
    pred_cam_set = set(prediction.keys())
    evaluated_cam_set = gt_cam_set.intersection(pred_cam_set)
    evaluated_cam_set = sorted(list(evaluated_cam_set))
    aria_human_names = ['aria01', 'aria02']
    sequence_length = len(ground_truth['cam01']['aria01'])

    count = sequence_length * 2

    smpl_model = SMPLModel()
    smpl_model_faces = np.load(smpl_faces_path)

    eval_metric = {}
    for cam in evaluated_cam_set:
        gt = ground_truth[cam]
        pred = prediction[cam]

        MPJPEs, PA_MPJPEs, MPVPEs, PA_MPVPEs, PCKs, AUCs = [], [], [], [], [], []

        miss = 0

        max_gt_penetr_val, max_pred_penetr_val = 0, 0
        max_gt_penetr_timestamp, max_pred_penetr_timestamp = 0, 0
        # breakpoint()
        for timestamp in tqdm(range(sequence_length)): 
            gt_2d_kps = [ground_truth[cam][aria_human][timestamp]['2d_joints'] for aria_human in aria_human_names]
            pred_2d_kps = list(pred['keypoints_2d'][timestamp])

            bestMatch, falsePositives, misses = match_2d_greedy(pred_2d_kps, gt_2d_kps) 

            miss += len(misses)

            aria1_gt_vertices, aria1_pred_vertices = np.zeros((6890, 3)), np.zeros((6890, 3))
            aria2_gt_vertices, aria2_pred_vertices = np.zeros((6890, 3)), np.zeros((6890, 3))
            for i, pair in enumerate(bestMatch):
                ####################Testing 2D joints####################
                # if pair[1] == 1:
                #     np.save('../testing/4dhumans2d/pred/{:05d}.npy'.format(timestamp), pred_2d_kps[pair[0]], allow_pickle=True)
                #     np.save('../testing/4dhumans2d/gt/{:05d}.npy'.format(timestamp), gt_2d_kps[pair[1]], allow_pickle=True)
                ####################Testing 3D joints####################
                # np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_pred_3d_joints', pred['3d_joints'][timestamp][pair[0]][:, :], allow_pickle=True)
                # np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_gt_3d_joints',gt[aria_human_names[pair[1]]][timestamp]['cam_3d_joints'][:, :], allow_pickle=True)
                # breakpoint()
                ####################Initialize smpl model to get 3d joints##############

                ### Prediction ###
                pose_params = pred['body_pose'][timestamp][pair[0]]
                pose_params = np.expand_dims(pose_params, axis=0) # batch

                shape_params = pred['betas'][timestamp][pair[0]].reshape(-1, 10)
                cam_params = pred['camera_translations'][timestamp][pair[0]].reshape(-1, 3)

                pred_vertices, pred_3d_joints = smpl_model.get_vertices_and_joints(torch.from_numpy(shape_params).to('cuda'), torch.from_numpy(pose_params).to('cuda'), torch.from_numpy(cam_params).to('cuda'))

                ###Ground Truth###
                cam_gt_vertices = gt[aria_human_names[pair[1]]][timestamp]['cam_smpl_vertices']
                cam_gt_3d_joints = gt[aria_human_names[pair[1]]][timestamp]['cam_3d_joints']

                # compute MPJPE and PA-MPJPE, MVE and PA-MVE
                cam_gt_3d_joints = np.expand_dims(cam_gt_3d_joints[:24, :], axis=0)
                cam_gt_vertices = np.expand_dims(cam_gt_vertices, axis=0)
                # if pair[1] == 1:
                #     np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_pred_3d_joints', pred_3d_joints[0, :24, :], allow_pickle=True)
                #     np.save('/home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/testing/4dhumans3d/aria1_gt_3d_joints',cam_gt_3d_joints[0], allow_pickle=True)

                MPJPE, PA_MPJPE, MPVPE, PA_MPVPE, PCK, AUC = compute_errors(pred_3d_joints[:, :24, :], cam_gt_3d_joints, pred_vertices, cam_gt_vertices)
                # breakpoint()

                MPJPEs.append(MPJPE)
                PA_MPJPEs.append(PA_MPJPE)
                MPVPEs.append(MPVPE)
                PA_MPVPEs.append(PA_MPVPE)
                PCKs.append(PCK)
                AUCs.append(AUC)

                if pair[1] == 0:
                    # aria1_gt_vertices = cam_gt_vertices[0]
                    aria1_pred_vertices = pred_vertices[0]
                if pair[1] == 1:
                    # aria2_gt_vertices = cam_gt_vertices[0]
                    aria2_pred_vertices = pred_vertices[0]

            if compute_collision and len(bestMatch) == 2: # if we want to compute collision and if the method reconstruct both people, compute penetration and intersection
                # compute pred penetration
                pred_penetr_val1, n_inside_vertices = penetration(aria1_pred_vertices, smpl_model_faces, aria2_pred_vertices, mode="max")
                pred_penetr_val2, n_inside_vertices = penetration(aria2_pred_vertices, smpl_model_faces, aria1_pred_vertices, mode="max")
                pred_penetr_val = max(pred_penetr_val1, pred_penetr_val2)
                if pred_penetr_val > max_pred_penetr_val:
                    max_pred_penetr_val = pred_penetr_val
                    max_pred_penetr_timestamp = timestamp

            if compute_collision:
                # compute gt penetration
                aria1_gt_vertices = gt[aria_human_names[0]][timestamp]['cam_smpl_vertices']
                aria2_gt_vertices = gt[aria_human_names[1]][timestamp]['cam_smpl_vertices']
                gt_penetr_val1, n_inside_vertices = penetration(aria1_gt_vertices, smpl_model_faces, aria2_gt_vertices, mode="max")
                gt_penetr_val2, n_inside_vertices = penetration(aria2_gt_vertices, smpl_model_faces, aria1_gt_vertices, mode="max")
                gt_penetr_val = max(gt_penetr_val1, gt_penetr_val2)
                if gt_penetr_val > max_gt_penetr_val:
                    max_gt_penetr_val = gt_penetr_val
                    max_gt_penetr_timestamp = timestamp
            # if timestamp == 208:
            #     np.save('../testing/pare_col/aria1_pred_vertices.npy', aria1_pred_vertices, allow_pickle=True)
            #     np.save('../testing/pare_col/aria2_pred_vertices.npy', aria2_pred_vertices, allow_pickle=True)
        # Compute MPJPE, PA-MPJPE, MPVPE, PA-MPVPE, PCK, AUC
        mpjpe = np.mean(np.array(MPJPEs))
        pa_mpjpe = np.mean(np.array(PA_MPJPEs))
        mpvpe = np.mean(np.array(MPVPEs))
        pa_mpvpe = np.mean(np.array(PA_MPVPEs))
        pck = np.mean(np.array(PCKs))
        auc = np.mean(np.array(AUCs))

        # Compute Precision, Recall, F1 
        precision, recall, f1 = compute_prf1(count, miss, 0) # There is no scenario of false positive, since in our scenario we don't have negative labels.

        # Compute NMJE and NMVE
        nmje = mpjpe/f1
        nmve = mpvpe/f1

        eval_metric[cam] = {'MPJPE': mpjpe, 'PA_MPJPE': pa_mpjpe, 'MPVPE': mpvpe, 'PA_MPVPE': pa_mpvpe, 'PCK': pck, 'AUC': auc, 'Precision': precision, 'Recall': recall, 'F1': f1, 'NMJE': nmje, 'NMVE': nmve, 'sequence_length': sequence_length, 'miss': miss}
        if compute_collision:
            eval_metric[cam]['max_gt_penetr_val'] = max_gt_penetr_val
            eval_metric[cam]['max_gt_penetr_timestamp'] = max_gt_penetr_timestamp
            eval_metric[cam]['max_pred_penetr_val'] = max_pred_penetr_val
            eval_metric[cam]['max_pred_penetr_timestamp'] = max_pred_penetr_timestamp
        # breakpoint()
    return eval_metric

# python demo/estimate_smpl.py configs/pare/hrnet_w32_conv_pare_mix_no_mosh.py data/checkpoints/hrnet_w32_conv_pare_coco.pth --multi_person_demo --tracking_config demo/mmtracking_cfg/deepsort_faster-rcnn_fpn_4e_mot17-private-half.py --input_path /media/rawalk/disk1/rawalk/datasets/ego_exo/main/31_mma/003_mma/exo/cam05/images/rgb.mp4 --show_path pare_output/003_mma.mp4 --smooth_type savgol --speed_up_type deciwatch
