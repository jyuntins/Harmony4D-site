cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/process_contact_smpl_no_aria/2_get_contact_pose3d.py'
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
# SEQUENCE='001_ballroom3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='011_karate'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='004_karate2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='011_karate3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='002_mma'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='006_mma2'; DEVICES=3,
######---------------------------------------------------------------------
BIG_SEQUENCE='33_mma3'
SEQUENCE='008_mma3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='34_mma4'
# SEQUENCE='001_mma4'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='35_mma5'
# SEQUENCE='004_mma5'; DEVICES=3,

######---------------------------------------------------------------------
START_TIME=1; END_TIME=10;
OVERRIDE_CONTACT_SEGPOSE3D=True;

######---------------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

######---------------------------------------------------------------------
mkdir -p ${OUTPUT_DIR}; 

######---------------------------debug-------------------------------------
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \
                    --override_contact_segpose3d $OVERRIDE_CONTACT_SEGPOSE3D \



