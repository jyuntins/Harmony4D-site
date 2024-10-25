cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/vis/refine_poses3d.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# ###------------------------------------------------------------------
BIG_SEQUENCE='07_fencing2'
# # SEQUENCE='001_fencing2'; DEVICES=3,
# # SEQUENCE='002_fencing2'; DEVICES=0,
# # SEQUENCE='003_fencing2'; DEVICES=1,
# SEQUENCE='004_fencing2'; DEVICES=2,
# SEQUENCE='005_fencing2'; DEVICES=3,

# SEQUENCE='007_fencing2'; DEVICES=3,
# SEQUENCE='008_fencing2'; DEVICES=3,
# SEQUENCE='009_fencing2'; DEVICES=3,
SEQUENCE='010_fencing2'; DEVICES=3,


OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

##----------------------------------------------------------------
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



