cd ../../..

###----------------------------------------------------------------
RUN_FILE='tools/vis/fit_poses3d_no_aria.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# # ###------------------------------------------------------------------
# BIG_SEQUENCE='11_tennis'
# SEQUENCE='001_tennis'; DEVICES=1,

# # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging' 
# SEQUENCE='001_hugging'; DEVICES=0,

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='001_mma'; DEVICES=3,

# # # ###---------------------------------------------------------------------
BIG_SEQUENCE='37_zen2'
SEQUENCE='001_zen2'; DEVICES=3,

OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

##----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/refine_poses3d")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 


# # # ###--------------------------debug------------------------------
START_TIME=1
END_TIME=-1

LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \



