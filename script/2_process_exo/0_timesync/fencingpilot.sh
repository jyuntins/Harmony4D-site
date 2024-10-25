###----------------------------------------------------------------------------
BIG_SEQUENCE='fencingpilot' ## actually soccer1, parent folder for gopros

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/"

CAMERAS="aria01--cam01--cam02--cam03--cam04"
START_TIMESTAMPS="03231--01279--01484--01246--01069" 


# # ###--------------------------------
SEQUENCE='fencingpilot_calibration'

## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='02900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04100' ## this is also inclusive

SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='03800' ## this includes the image name
SEQUENCE_END_TIMESTAMP='05000' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \