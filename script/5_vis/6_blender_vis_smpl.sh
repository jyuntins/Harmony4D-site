cd ../..

###------------note this has to be run inside the mmhuman docker---------------
###--------------------------------------------------------------------------
RUN_FILE='tools/vis/blender_vis_smpl.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

#### always use the same gpu id in the devices as set in the blender
### EDIT -> Preferences -> Cycles Render
### also check render -> GPU compute is on

# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='01_tagging'
# SEQUENCE='007_tagging'; DEVICES=1,


# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='02_legoassemble'
# SEQUENCE='004_legoassemble'; DEVICES=1,


# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='04_basketball'
# SEQUENCE='001_basketball'; DEVICES=1,


# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball'
# SEQUENCE='001_volleyball'; DEVICES=1,


# # # # ###----------------------------------------------------------------
BIG_SEQUENCE='07_fencing2'
SEQUENCE='001_fencing2'; DEVICES=1,

# # ###----------------------------------------------------------------
# BIG_SEQUENCE='08_badminton'
# SEQUENCE='001_badminton'; DEVICES=1,


# ###----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_blender")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 

# # ###----------------------------------------------------------------
# NUM_JOBS=6

# # # # # # # # # # # # ##-----------------------------------------------
# SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)
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

#     # # ##--------------run-----------------------------
#     CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                     --sequence_path ${SEQUENCE_PATH} \
#                     --output_path $OUTPUT_DIR \
#                     --start_time_stamp $START_TIME \
#                     --end_time_stamp $END_TIME &

# done


# # # # # # # # # # # # # ###----------------debug----------------------
START_TIME=1
END_TIME=100

# ##--------------run-----------------------------
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                --sequence_path ${SEQUENCE_PATH} \
                --output_path $OUTPUT_DIR \
                --start_time_stamp $START_TIME \
                --end_time_stamp $END_TIME 