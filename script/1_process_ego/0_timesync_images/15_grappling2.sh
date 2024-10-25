###----------------------------------------------------------------------------
BIG_SEQUENCE='15_grappling2' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


# # # ###-------------grappling2---------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00100--00100" ##first throw by rawal

# SEQUENCE='calibration_grappling2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive


# # ##-------------grappling2---------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="02067--02093" ##first throw by rawal

SEQUENCE='019_grappling2'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='14009' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03190' ## this is also inclusive
SEQUENCE_END_TIMESTAMP='14609' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
