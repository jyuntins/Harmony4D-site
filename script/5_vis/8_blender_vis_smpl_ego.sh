cd ../..

###------------note this has to be run inside the mmhuman docker---------------
###--------------------------------------------------------------------------
RUN_FILE='tools/vis/blender_vis_smpl_ego.py'

SEQUENCE_ROOT_DIR='/home/rawalk/Desktop/datasets/ego_exo/main'

SEQUENCE='001_tagging_1'

OUTPUT_DIR="/home/rawalk/Desktop/datasets/ego_exo/main/$SEQUENCE/processed_data/blender_vis_ego"


# ###----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 

# # ###----------------------------------------------------------------
# NUM_JOBS=6
# DEVICES=0,

# # # ##-----------------------------------------------
# SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)
# PER_JOB=$((SEQUENCE_LENGTH/NUM_JOBS))
# LAST_JOB_ITER=$((NUM_JOBS-1))

# for (( i=0; i < $NUM_JOBS; ++i ))
# do
#     START_TIME=$((i*PER_JOB + 1))
#     END_TIME=$((i*PER_JOB + PER_JOB))

#     if [ $i == $LAST_JOB_ITER ]
#     then
#         END_TIME=-1
#     fi

#     # ##--------------run-----------------------------
#     LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
#     CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                     --sequence_path ${SEQUENCE_PATH} \
#                     --output_path $OUTPUT_DIR \
#                     --start_time_stamp $START_TIME \
#                     --end_time_stamp $END_TIME &

# done


# ###----------------debug----------------------
# START_TIME=1
# END_TIME=10

START_TIME=1
END_TIME=1

# ##--------------run-----------------------------
LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                --sequence_path ${SEQUENCE_PATH} \
                --output_path $OUTPUT_DIR \
                --start_time_stamp $START_TIME \
                --end_time_stamp $END_TIME 