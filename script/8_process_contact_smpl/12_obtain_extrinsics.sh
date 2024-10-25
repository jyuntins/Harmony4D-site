cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/process_smpl/obtain_extrinsics.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

######---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='001_hugging'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='012_grappling3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='18_sword'
# SEQUENCE='001_sword'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='19_sword2'
# SEQUENCE='001_sword2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='001_ballroom'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='22_ballroom2'
# SEQUENCE='001_ballroom2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='007_ballroom3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='004_karate'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='004_karate2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='008_karate3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='009_mma'; DEVICES=2,
######---------------------------------------------------------------------
BIG_SEQUENCE='32_mma2'
SEQUENCE='024_mma2'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='metric_mma3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='34_mma4'
# SEQUENCE='001_mma4'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='35_mma5'
# SEQUENCE='001_mma5'; DEVICES=3,

##----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

##----------------------------------------------------------------
# LOG_DIR="$(echo "${OUTPUT_DIR}/logs/fit_poses3d_metric")"
mkdir -p ${OUTPUT_DIR}; 
# mkdir -p ${LOG_DIR}; 


# # # ###--------------------------debug------------------------------
START_TIME=1
END_TIME=-1

# LOG_FILE="$(echo "${LOG_DIR}/log_start_${START_TIME}_end_${END_TIME}.txt")"; touch ${LOG_FILE}
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \



