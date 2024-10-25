###----------------------------------------------------------------------------
BIG_SEQUENCE='21_ballroom'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


# # # # # ###-------------ballroom---------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00200--00200" ##third throw by rawal

# SEQUENCE='calibration_ballroom'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00200' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive

# # # # ##-------------ballroom---------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="03101--03075" ##third throw by rawal

SEQUENCE='011_ballroom'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='10104' ## this includes the image name First sequence start 3360
SEQUENCE_END_TIMESTAMP='10704' ## this is also inclusive  First sequence end 3960

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
