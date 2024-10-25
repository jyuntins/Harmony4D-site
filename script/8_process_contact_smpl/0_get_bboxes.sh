cd ../..
echo "Running 0_get_bboxes.py"
###----------------------------------------------------------------
RUN_FILE='tools/process_smpl/0_get_bboxes.py'
SEQUENCE_ROOT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging' 
# SEQUENCE='002_hugging'; DEVICES=0,

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='016_grappling2'; DEVICES=3,

# ###---------------------------------------------------------------------
# BIG_SEQUENCE="18_sword"
# SEQUENCE="002_sword"; DEVICES=0,

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='003_sword3'; DEVICES=2,

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='011_ballroom'; DEVICES=1,

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='002_ballroom3'; DEVICES=1,

# # ###------------------------------------------------------------------
# ## aria01, blue is the coach. aria02 is the girl
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='002_karate3'; DEVICES=3,

# # ###------------------------------------------------------------------
# # ## aria01 is the white. aria02 is black
BIG_SEQUENCE='31_mma'
SEQUENCE='007_mma'; DEVICES=2,

# # ###------------------------------------------------------------------
# ## aria01 is the blue. aria02 is red guy
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='001_mma2'; DEVICES=2,

# # ###------------------------------------------------------------------
# # aria01 is the black. aria02 is shirtless white guy
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='001_mma3'; DEVICES=1,

###-------------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

# ##----------------------------------------------------------------
NUM_JOBS=4 ## if using fasterrcnn, issues when using odd number of jobs, for eg: 5 is glitchy.
# NUM_JOBS=2 ## if using fasterrcnn, issues when using odd number of jobs, for eg: 5 is glitchy.

# ###----------------------------------------------------------------
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/bbox")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 

# # # ##-----------------------------------------------
SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)

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
    
# #     # ##--------------run-----------------------------
#     LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
#     CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME | tee ${LOG_FILE} &


# done
# wait

# # # ###--------------debug-----------------------------
# TIMESTAMPS=":::"

START_TIME=1
END_TIME=12
TIMESTAMPS="15:16:17:18:19:20:21:22:23:24:25"
TIMESTAMPS="1:2:3:4:5:6:7:8:9:10:11:12:13:14:15"
TIMESTAMPS="1:2:3"
TIMESTAMPS="125"
TIMESTAMPS="126:127:128:129:130:6:7:8:9:10:11:12:13:14:15"
LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                   --sequence_path ${SEQUENCE_PATH} \
                   --output_path $OUTPUT_DIR \
                   --start_time $START_TIME \
                   --end_time $END_TIME \
                   --choosen_time $TIMESTAMPS
