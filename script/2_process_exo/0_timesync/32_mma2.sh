###----------------------------------------------------------------------------
BIG_SEQUENCE='32_mma2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# ## second throw of the ball
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="00170--01742--01666--01614--01522--01585--01772--01209--01261--01276--01808--01245--00882--01093--00985--01123--01395--01358--01023--01497--01653"

# SEQUENCE='calibration_mma2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00180' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01000' ## this is also inclusive

# ##---------------------------------------------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="03185--01742--01666--01614--01522--01585--01772--01209--01261--01276--01808--01245--00882--01093--00985--01123--01395--01358--01023--01497--01653"

SEQUENCE='002_mma2'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='04121' ## this includes the image name
SEQUENCE_END_TIMESTAMP='08440' ## this is also inclusive
# 001_mma2 3343-3943
# 002_mma2 4121-5025
# 003_mma2 5016-6162
# 004_mma2 6152-7115
# 005_mma2 7140-7810
# 006_mma2 7801-8440
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
