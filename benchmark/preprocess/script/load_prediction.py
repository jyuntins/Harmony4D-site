
import os
import numpy as np
import joblib
import torch
import smplx
import pickle
import sys
# sys.path.insert(1, '/home/rawalk/Desktop/ego/buddi')

def load_multihmr_prediction(multihmr_prediction_path):
    smplx2smpl_joint = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,20,21]
    vertices = []
    keypoints_3d = []   
    keypoints_2d = []
    timestamp = []

    smplx2smpl = pickle.load(open('/home/rawalk/Desktop/ego/buddi/benchmark_preprocess/data/utils/smplx2smpl.pkl', 'rb'))
    smplx2smpl = torch.tensor(smplx2smpl['matrix'][None], dtype=torch.float32).cuda()

    smpl = smplx.SMPL(model_path='/home/rawalk/Desktop/models/smpl/models', batch_size=2, create_transl=True).to('cuda')
    smpl_model = smplx.create(
        model_path='/home/rawalk/Desktop/ego/buddi/essentials/body_models', 
        model_type='smplx',
        # kid_template_path=kid_template, 
        # age='kid',
        batch_size=2
    ).to('cuda')

    # /home/rawalk/Desktop/ego/ego_exo/scripts/benchmark/harmony4d_evaluation/benchmark_proprocess/multihmr/prediction/31_mma/003_mma/cam05
    for file in sorted(os.listdir(multihmr_prediction_path)):

        if not file.endswith('.npy'):
            continue
        file_path = os.path.join(multihmr_prediction_path, file)
        pred = np.load(file_path, allow_pickle=True)
        # verts_smplx
        # breakpoint()
        smplx_verts = torch.tensor(np.array([human['verts_smplx'].cpu().numpy() for human in pred])).to('cuda')
        # smplx_verts = get_smplx_pred(pred, smpl_model)
        smpl_verts = torch.matmul(smplx2smpl.repeat(smplx_verts.shape[0], 1, 1), smplx_verts)
        smpl_joints = torch.matmul(smpl.J_regressor, smpl_verts)
        smpl_verts = smpl_verts.detach().cpu().numpy()
        smpl_joints = smpl_joints.detach().cpu().numpy()
        vertices.append(smpl_verts)
        keypoints_3d.append(smpl_joints)

        j2d = np.array([human['j2d_smplx'].cpu().numpy() for human in pred])
        j2d = j2d * (3840/896, 3840/896)
        j2d[:, :, 1] = j2d[:, :, 1] - 896
        j2d = j2d[:, smplx2smpl_joint, :]
        keypoints_2d.append(j2d)

    multihmr_pred = {'vertices': np.array(vertices), 'keypoints_3d': np.array(keypoints_3d), 'keypoints_2d': np.array(keypoints_2d)}
    # breakpoint()
    return multihmr_pred 




def load_bev_prediction(bev_prediction_path):
    # Load the BEV predictions
    vertices = []
    keypoints_3d = []
    keypoints_2d = []
    
    for file in sorted(os.listdir(bev_prediction_path)):
        if not file.endswith('.npz'):
            continue
        file_path = os.path.join(bev_prediction_path, file)
        pred = np.load(file_path, allow_pickle=True)['results'].item()
        # breakpoint()
        vertices.append(pred['verts']+pred['cam_trans'].reshape(-1, 1,3))
        keypoints_3d.append(pred['joints'][:, :24, :]+pred['cam_trans'].reshape(-1, 1,3))
        keypoints_2d.append(pred['pj2d_org'][:, :24, :])
    
    bev_pred = {'vertices': np.array(vertices), 'keypoints_3d': np.array(keypoints_3d), 'keypoints_2d': np.array(keypoints_2d)}
    return bev_pred


def get_smplx_pred(human, body_model_smplx=None):
    """
    Returns the SMPL parameters of a human.
    """
    def to_tensor(x):
        return torch.tensor(x).to('cuda')

    params = dict(
        #betas = torch.cat([to_tensor(human[f'betas']),to_tensor(human[f'scale'])], dim=1),
        global_orient = to_tensor(human[f'global_orient']),
        body_pose = to_tensor(human[f'body_pose']),
        betas = to_tensor(human[f'betas']),
        scale = to_tensor(human[f'scale']),
        transl = to_tensor(human[f'transl']),
    )

    verts, joints = None, None
    if body_model_smplx is not None:
        body = body_model_smplx(**params)
        verts = body.vertices.detach() 

    return verts

def load_buddi_prediction(buddi_prediction_path):
    vertices = []
    keypoints_3d = []   
    keypoints_2d = []
    timestamp = []

    smplx2smpl = pickle.load(open('/home/rawalk/Desktop/ego/buddi/benchmark_preprocess/data/utils/smplx2smpl.pkl', 'rb'))
    smplx2smpl = torch.tensor(smplx2smpl['matrix'][None], dtype=torch.float32).cuda()

    smpl = smplx.SMPL(model_path='/home/rawalk/Desktop/models/smpl/models', batch_size=2, create_transl=True).to('cuda')
    smpl_model = smplx.create(
        model_path='/home/rawalk/Desktop/ego/buddi/essentials/body_models', 
        model_type='smplx',
        # kid_template_path=kid_template, 
        # age='kid',
        batch_size=2
    ).to('cuda')
    cfg = default_config
    cfg.camera.perspective.iw = 3840
    cfg.camera.perspective.ih = 2160
    camera = build_camera(
        camera_cfg=cfg.camera,
        camera_type=cfg.camera.type,
        batch_size=cfg.batch_size,
        device=cfg.device
    ).to(cfg.device)

    for file in sorted(os.listdir(buddi_prediction_path)):
        if not file.endswith('.pkl'):
            continue
        file_path = os.path.join(buddi_prediction_path, file)
        pred = joblib.load(file_path)['humans']
        smplx_verts = get_smplx_pred(pred, smpl_model)
        smpl_verts = torch.matmul(smplx2smpl.repeat(2, 1, 1), smplx_verts)
        smpl_joints = torch.matmul(smpl.J_regressor, smpl_verts)
        proj_2d = camera.project(smpl_joints).detach().cpu().numpy()
        proj_2d = np.array([3840, 2160]) - proj_2d -1

        smpl_joints = smpl_joints.detach().cpu().numpy()
        vertices.append(smpl_verts.detach().cpu().numpy())
        keypoints_3d.append(smpl_joints)
        keypoints_2d.append(proj_2d)
        timestamp.append(int(file.split('.')[0]) -1)

    buddi_pred = {'vertices': np.array(vertices), 'keypoints_3d': np.array(keypoints_3d), 'timestamp': np.array(timestamp), 'keypoints_2d': np.array(keypoints_2d)}

    return buddi_pred 

def combine_predictions(bev_pred, buddi_pred):
    for buddi_index, timestamp in enumerate(buddi_pred['timestamp']):
        bev_pred['vertices'][timestamp] = buddi_pred['vertices'][buddi_index]
        bev_pred['keypoints_3d'][timestamp] = buddi_pred['keypoints_3d'][buddi_index]
        bev_pred['keypoints_2d'][timestamp] = buddi_pred['keypoints_2d'][buddi_index]
    final_pred = bev_pred

    return final_pred