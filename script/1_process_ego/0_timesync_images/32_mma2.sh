###----------------------------------------------------------------------------
BIG_SEQUENCE='32_mma2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


# #  ###-------------------------------
# CAMERAS="aria01--aria02" ## 2 arias
# START_TIMESTAMPS="00170--00110" 

# SEQUENCE='calibration_mma2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00180' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01000' ## this is also inclusive

# #  ###------------------------------
CAMERAS="aria01--aria02" ## 2 arias
START_TIMESTAMPS="03185--03133"

SEQUENCE='006_mma2'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='07801' ## this includes the image name
SEQUENCE_END_TIMESTAMP='08440' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
