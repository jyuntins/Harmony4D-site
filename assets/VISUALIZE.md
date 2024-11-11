# Visualization

We provide scripts to visualize 2D bboxes, 2D poses, 3D poses and SMPL meshes.  

## Download SMPL models

Please go to [SMPL website](https://smpl.is.tue.mpg.de/)
and register to get access to the downloads section.
Download the SMPL model (version 1.1.0), unzip it, and rename the neutral model file to 
```SMPL_NEUTRAL.pkl``` as follows.

```shell
unzip SMPL_python_v.1.1.0.zip
mv SMPL_python_v.1.1.0/smpl/models/basicmodel_neutral_lbs_10_207_0_v1.1.0.pkl SMPL_NEUTRAL.pkl
```
Then, update the SMPL model path in ```config/default.py``` 
by setting the ```_C.SMPL_MODEL_DIR``` variable to the directory containing
```SMPL_NEUTRAL.pkl```.

## Visualization Scripts
We provide shell scripts for better visualization control. Scripts are located in the ```scripts``` directory.

All scripts follow the same format. 
Here, we use ```scripts/1_poses3d_ego_exo.sh``` as an example to visualize the 
```01_hugging/001_hugging``` sequence in the ```train``` set.

### Setup Instructions
Inside ```scripts/1_poses3d_ego_exo.sh```

- Set Data Path: Update the $SEQUENCE_ROOT_DIR variable with the absolute path to your data.
- Select Sequence: Define the main sequence and subsequence for visualization by setting $BIG_SEQUENCE and $SEQUENCE variables.
```
BIG_SEQUENCE='01_hugging'
SEQUENCE='001_hugging';
```
- Run the Script:
```
cd scripts
chmod +x 1_poses3d_ego_exo.sh
./1_poses3d_ego_exo.sh
```

The images will be saved to ```$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/processed_data/vis_poses3d```
