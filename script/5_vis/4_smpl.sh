cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/vis/smpl.py'
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
BIG_SEQUENCE='13_hugging'
SEQUENCE='001_hugging'; DEVICES=0,

# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='007_grappling2'; DEVICES=0,

# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='002_ballroom'; DEVICES=2,

# # ###------------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball'
# SEQUENCE='001_volleyball'; DEVICES=1,


# # # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=2,

####-------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

##----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl")"
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



