DEVICES=0
RUN_FILE='../tools/ego_exo/3_vis_poses2d_ego_exo.py'

## Change the sequence root dir path to where you put the data
SEQUENCE_ROOT_DIR='/media/rawalk/disk2/camera_ready/train'
# SEQUENCE_ROOT_DIR='/media/rawalk/disk2/camera_ready/test'

########################################## Train ##############################################
BIG_SEQUENCE='01_hugging'
SEQUENCE='001_hugging';
######---------------------------------------------------------------------
# BIG_SEQUENCE='02_grappling'
# SEQUENCE='001_grappling';
######---------------------------------------------------------------------
# BIG_SEQUENCE='03_grappling2'
# SEQUENCE='001_grappling2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='04_sword'
# SEQUENCE='001_sword';
######---------------------------------------------------------------------
# BIG_SEQUENCE='05_sword2'
# SEQUENCE='001_sword2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='07_ballroom'
# SEQUENCE='001_sword3';
######---------------------------------------------------------------------
# BIG_SEQUENCE='08_ballroom2'
# SEQUENCE='001_ballroom';
######---------------------------------------------------------------------
# BIG_SEQUENCE='09_karate'
# SEQUENCE='004_karate';
######---------------------------------------------------------------------
# BIG_SEQUENCE='10_karate2'
# SEQUENCE='001_karate2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='11_karate3'
# SEQUENCE='001_karate3';
######---------------------------------------------------------------------
# BIG_SEQUENCE='12_mma'
# SEQUENCE='001_mma';
######---------------------------------------------------------------------
# BIG_SEQUENCE='13_mma2'
# SEQUENCE='001_mma2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='14_mma3'
# SEQUENCE='001_mma3';
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_mma4'
# SEQUENCE='001_mma4';
########################################################################################



########################################## Test ##############################################
# BIG_SEQUENCE='01_hugging'
# SEQUENCE='001_hugging';
######---------------------------------------------------------------------
# BIG_SEQUENCE='03_grappling2'
# SEQUENCE='025_grappling2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='05_sword2'
# SEQUENCE='009_sword2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='06_sword3'
# SEQUENCE='001_sword3';
######---------------------------------------------------------------------
# BIG_SEQUENCE='08_ballroom2'
# SEQUENCE='007_ballroom2';
######---------------------------------------------------------------------
# BIG_SEQUENCE='11_karate3'
# SEQUENCE='009_karate3';
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_mma4'
# SEQUENCE='016_mma4';
######---------------------------------------------------------------------
# BIG_SEQUENCE='16_mma5'
# SEQUENCE='001_mma5';
########################################################################################


OUTPUT_DIR="$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
mkdir -p ${OUTPUT_DIR}; 


START_TIME=1
END_TIME=-1

CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \



