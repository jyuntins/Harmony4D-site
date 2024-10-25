cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/vis/init_smpl.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# # ####-------------------------------------------------------------
# BIG_SEQUENCE='01_tagging'

# SEQUENCE='001_tagging'; DEVICES=0, ## next to do
# SEQUENCE='012_tagging'; DEVICES=1,
# SEQUENCE='013_tagging'; DEVICES=2,
# SEQUENCE='014_tagging'; DEVICES=3,

# # ###------------------------------------------------------------------
# BIG_SEQUENCE='08_badminton'
# SEQUENCE='001_badminton'; DEVICES=3,


# # ###------------------------------------------------------------------
# BIG_SEQUENCE='08_badminton'
# SEQUENCE='001_badminton'; DEVICES=3,

# # # ###------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=3,

# # ###------------------------------------------------------------------
BIG_SEQUENCE='23_ballroom3'
SEQUENCE='007_ballroom3'; DEVICES=3,

####-------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

##----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 

##----------change permissions-----------
chmod -R 777 $OUTPUT_DIR/vis_init_smpl
chmod -R 777 $OUTPUT_DIR/init_smpl

# # # ###--------------------------debug------------------------------
START_TIME=1
END_TIME=-1

LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \



