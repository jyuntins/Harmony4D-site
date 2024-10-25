cd ../..
DEVICES=0
BIG_SEQUENCE="15_grappling2"
SEQUENCE_LIST="001_grappling2 002_grappling2 003_grappling2 004_grappling2 005_grappling2 006_grappling2 007_grappling2 008_grappling2 009_grappling2 010_grappling2 011_grappling2 012_grappling2 013_grappling2 014_grappling2 015_grappling2 016_grappling2 017_grappling2 018_grappling2 019_grappling2"
SEQUENCE_ROOT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"
for SEQUENCE in $SEQUENCE_LIST
do      


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

    wait
done