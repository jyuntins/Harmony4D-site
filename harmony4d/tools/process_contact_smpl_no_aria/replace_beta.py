import _init_paths
import os
import argparse
from tqdm import tqdm
import numpy as np
from datasets.exo_scene import EgoExoScene

from configs import cfg
from configs import update_config

##------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Visualization of extrinsics of camera parameters.')
    parser.add_argument('--init_smpl_dir', action='store', help='the path to the init_smpl')
    parser.add_argument('--smpl_dir', action='store', help='the path to the smpl_dir')
    parser.add_argument('--start_time', default=1, help='start time')
    parser.add_argument('--end_time', default=-1, help='end time')
    args = parser.parse_args()

    init_smpl_dir = args.init_smpl_dir
    smpl_dir = args.smpl_dir
    for file in tqdm(sorted(os.listdir(args.init_smpl_dir))):
        if not file.endswith('npy'):
            continue
        init_smpl_file_path = os.path.join(init_smpl_dir, file)
        smpl_file_path = os.path.join(smpl_dir, file)
        init_smpl = np.load(init_smpl_file_path, allow_pickle=True).item()
        smpl = np.load(smpl_file_path, allow_pickle=True).item()

        for aria in init_smpl.keys():
            init_smpl[aria]['betas'] = smpl[aria]['betas']+np.random.uniform(-1, 1)*0.000001 # hack: small random perturbation for clustering
            init_smpl[aria]['init_global_orient'] = smpl[aria]['global_orient']
            init_smpl[aria]['init_transl'] = smpl[aria]['transl']

        np.save(init_smpl_file_path, init_smpl)

##------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()