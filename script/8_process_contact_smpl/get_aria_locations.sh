cd ../..

###----------------------------------------------------------------
RUN_FILE='tools/process_smpl/get_aria_locations.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging' 
# # SEQUENCE='calibration_hugging'
# SEQUENCE='001_hugging'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# # SEQUENCE='calibration_grappling'
# SEQUENCE='001_grappling'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='001_ballroom'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='001_mma'; DEVICES=0,

BIG_SEQUENCE='30_karate3'
SEQUENCE='001_karate3'; DEVICES=0,

###---------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

###----------------------------------------------------------------
CONFIG_FILE='configs/wholebody/2d_kpt_sview_rgb_img/topdown_heatmap/coco-wholebody/hrnet_w48_coco_wholebody_384x288_dark_plus.py'
CHECKPOINT='https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_wholebody_384x288_dark-f5726563_20200918.pth'

###----------------------------------------------------------------
CHOOSEN_TIME=":::" ## default
# CHOOSEN_TIME="150:151:152:153:154:155:156:157:158:159:160:161:162:163:164:165"

CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --choosen_time $CHOOSEN_TIME \
