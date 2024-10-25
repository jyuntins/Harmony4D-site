###----------------------------------------------------------------------------
BIG_SEQUENCE='tennispilot'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"

###---------------------------
CAMERAS="aria04" ## 2 arias
START_TIMESTAMPS="01480" 


# ###--------------------------------
SEQUENCE='tennispilot_calibration'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria04'
SEQUENCE_START_TIMESTAMP='01950' ## this includes the image name
SEQUENCE_END_TIMESTAMP='03950' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
