cd ../..

## conda activate mmp_vis
source ~/anaconda3/etc/profile.d/conda.sh
# conda activate mmp_vis

###----------------------------------------------------------------
RUN_FILE='tools/manual_fix/5_metric_scale_scene.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

######---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='001_hugging'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='001_grappling3'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='18_sword'
# SEQUENCE='001_sword'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='19_sword2'
# SEQUENCE='002_sword2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='001_ballroom'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='22_ballroom2'
# SEQUENCE='001_ballroom2'; DEVICES=3,
######---------------------------------------------------------------------
BIG_SEQUENCE='23_ballroom3'
SEQUENCE='001_ballroom3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='011_karate'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='004_karate2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='011_karate3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='003_mma'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='003_mma2'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='metric_mma3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='34_mma4'
# SEQUENCE='006_mma4'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='35_mma5'
# SEQUENCE='004_mma5'; DEVICES=3,
# ###---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='001_karate'; DEVICES=0,
 

# 23_ballroom3 001_ballroom3
CAMERAS="1:7:10:16:19"
TARGET_CAMERA_NAME='18' 

#19_sword2 002_sword2
# CAMERAS="5:6:9"
# TARGET_CAMERA_NAME='15' 

# grappling sword14 18 7 8 5 6 1
# CAMERAS="14:5:6:7:1"
# TARGET_CAMERA_NAME='18' 

# mma
# CAMERAS="7:9:11:17"
# TARGET_CAMERA_NAME='8' 

# karate
# CAMERAS="4:6:9:11"
# TARGET_CAMERA_NAME='19'

TIMESTAMP="1"

###----------------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

###----------------------------------------------------------------------
mkdir -p ${OUTPUT_DIR}; 

###----------------------------------------------------------------
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --target_camera_name $TARGET_CAMERA_NAME \
                    --cameras $CAMERAS \
                    --timestamp $TIMESTAMP \
                    --testing_scale 



