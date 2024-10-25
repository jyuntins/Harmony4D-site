###----------------------------------------------------------------------------
BIG_SEQUENCE='33_mma3'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


# #  ###-------------------------------
# CAMERAS="aria01--aria02" ## 2 arias
# START_TIMESTAMPS="00200--00200" 

# SEQUENCE='calibration_mma3'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00220' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive

# #  ###------------------------------
CAMERAS="aria01--aria02" ## 2 arias
START_TIMESTAMPS="03030--03000"

SEQUENCE='002_mma3'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='03901' ## this includes the image name
SEQUENCE_END_TIMESTAMP='04430' ## this is also inclusive
# 001_mma3 3458-3868
# 002_mma3 3901-4430
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
