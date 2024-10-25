cd ../..

###------------note this has to be run inside the mmhuman docker---------------
###--------------------------------------------------------------------------
RUN_FILE='tools/process_contact_smpl_no_aria/9_freeze_betas.py'

SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

######---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='001_hugging'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=3,
######---------------------------------------------------------------------
BIG_SEQUENCE='16_grappling3'
SEQUENCE='028_grappling3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='18_sword'
# SEQUENCE='001_sword'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='19_sword2'
# SEQUENCE='002_sword2'; DEVICES=3,
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
# SEQUENCE='001_ballroom3'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='008_karate'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='009_karate2'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='001_karate3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='002_mma'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='003_mma2'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='008_mma3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='34_mma4'
# SEQUENCE='001_mma4'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='35_mma5'
# SEQUENCE='004_mma5'; DEVICES=3,

###----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

###----------------------------------------------------------------
mkdir -p ${OUTPUT_DIR};

# # ###----------------------------------------------------------
# ##----------change permissions of init smpl-----------
START_TIME=148
END_TIME=148

CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME
