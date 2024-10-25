###----------------------------------------------------------------------------
BIG_SEQUENCE='36_zen1'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# CAMERAS="cam01--cam02--cam03--cam04"
# START_TIMESTAMPS="00385--00113--00253--00483"

# SEQUENCE='calibration_zen1'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='00500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='00800' ## this is also inclusive


###-------------for calibration---------------
CAMERAS="cam01--cam02--cam03--cam04"
START_TIMESTAMPS="00385--00113--00253--00483"

SEQUENCE='001_zen1'
SEQUENCE_CAMERA_NAME='cam01'
SEQUENCE_START_TIMESTAMP='01500' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07499' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
