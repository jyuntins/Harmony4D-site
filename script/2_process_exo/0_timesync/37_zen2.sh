###----------------------------------------------------------------------------
## capture 1
BIG_SEQUENCE='37_zen2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
# START_TIMESTAMPS="00662--00524--00467--00389--00607--00390--00510--00596"

# SEQUENCE='calibration_zen2'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='01500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='02100' ## this is also inclusive

# ###-------------for calibration---------------
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
START_TIMESTAMPS="00662--00524--00467--00389--00607--00390--00510--00596"

SEQUENCE='001_zen2'
SEQUENCE_CAMERA_NAME='cam01'
SEQUENCE_START_TIMESTAMP='01500' ## this includes the image name
SEQUENCE_END_TIMESTAMP='05999' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
