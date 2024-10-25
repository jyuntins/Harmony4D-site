cd ../..
echo "Running 2_get_poses3d.py"
###----------------------------------------------------------------
RUN_FILE='tools/process_smpl/1_get_poses3d.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='002_hugging'; DEVICES=2,; OVERRIDE_SEGPOSE2D_LOAD=True

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='002_grappling2'; DEVICES=0,; OVERRIDE_SEGPOSE2D_LOAD=True

# ###---------------------------------------------------------------------
# BIG_SEQUENCE="18_sword"
# SEQUENCE="015_sword"; DEVICES=0,; OVERRIDE_SEGPOSE2D_LOAD=True

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; DEVICES=2,; OVERRIDE_SEGPOSE2D_LOAD=True

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='011_ballroom'; DEVICES=1,; OVERRIDE_SEGPOSE2D_LOAD=True

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='002_ballroom3'; DEVICES=2,; OVERRIDE_SEGPOSE2D_LOAD=True

# # ###------------------------------------------------------------------
# ## aria01, blue is the coach. aria02 is the girl
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='002_karate3'; DEVICES=3,; OVERRIDE_SEGPOSE2D_LOAD=True


# # ###------------------------------------------------------------------
# ## aria01 is the white. aria02 is black
BIG_SEQUENCE='31_mma'
SEQUENCE='001_mma'; DEVICES=2,; OVERRIDE_SEGPOSE2D_LOAD=True

# # # ###------------------------------------------------------------------
# # ## aria01 is the blue. aria02 is red guy
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='001_mma2'; DEVICES=2,; OVERRIDE_SEGPOSE2D_LOAD=True


# # ###------------------------------------------------------------------
# # aria01 is the black. aria02 is shirtless white guy
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='001_mma3'; DEVICES=1,; OVERRIDE_SEGPOSE2D_LOAD=True



###----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

# ##----------------------------------------------------------------
#NUM_JOBS=6
NUM_JOBS=8 

# # ##----------------------------------------------------------------
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/poses3d")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 


 # # ##------------------comment to skip parallel run-----------------------
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
    
# #     ##--------------run-----------------------------
#     LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
#     CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME | tee ${LOG_FILE} &



# done
# wait

# # ###--------------------------debug------------------------------
START_TIME=1
END_TIME=2

# TIMESTAMPS=":::"
# TIMESTAMPS="1:2:3:4:5:6:7:8:9:10:11:12:13:14:15"
TIMESTAMPS="57:58:59:60:61:62:63"

# if override_segpose2d_load variable is not defined, set it to False
if [ -z ${OVERRIDE_SEGPOSE2D_LOAD+x} ]; then 
    OVERRIDE_SEGPOSE2D_LOAD=False; 
fi

LOG_FILE="$(echo "${LOG_DIR}/log_pose3d_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                   --sequence_path ${SEQUENCE_PATH} \
                   --output_path $OUTPUT_DIR \
                   --start_time $START_TIME \
                   --end_time $END_TIME \
                   --choosen_time $TIMESTAMPS \
                   --override_segpose2d_load $OVERRIDE_SEGPOSE2D_LOAD \

