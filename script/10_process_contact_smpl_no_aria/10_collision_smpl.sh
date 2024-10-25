cd ../..

RUN_FILE='tools/process_contact_smpl_no_aria/7_get_smpl_trajectory_collision.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

###--------------------------------------------------------------------------
#BIG_SEQUENCE='13_hugging'
#SEQUENCE='001_hugging'; DEVICES=1,

###--------------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='002_grappling2'; DEVICES=2,

###--------------------------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='008_grappling3'; DEVICES=1,

###--------------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; DEVICES=1,

###--------------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='001_ballroom3'; DEVICES=2,

###--------------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='004_karate2'; DEVICES=3,

###--------------------------------------------------------------------------
BIG_SEQUENCE='34_mma4'
SEQUENCE='001_mma4'; DEVICES=2,

###--------------------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

mkdir -p ${OUTPUT_DIR}; 

START_TIME=1
END_TIME=-1

CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME

# # # ###-------------------debug-------------------------
#START_TIME=1
#END_TIME=15

#CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                    --sequence_path ${SEQUENCE_PATH} \
#                    --output_path $OUTPUT_DIR \
#                    --start_time $START_TIME \
#                    --end_time $END_TIME 
