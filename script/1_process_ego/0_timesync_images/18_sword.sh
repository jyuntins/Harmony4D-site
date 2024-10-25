###----------------------------------------------------------------------------
BIG_SEQUENCE='18_sword'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###----------------------------------------------------------------------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00320--00370" ##third throw by rawal

# SEQUENCE='calibration_sword3'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00320' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01320' ## this is also inclusive

###----------------------------------------------------------------------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="02694--02430" ##third throw by rawal

SEQUENCE='005_sword'
SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03280' ## this includes the image name 001 starts from 3280
# SEQUENCE_END_TIMESTAMP='03880' ## this is also inclusive  001 ends on 3880
SEQUENCE_START_TIMESTAMP='05710' ## this includes the image name, 001 starts from 3280
SEQUENCE_END_TIMESTAMP='06250' ## this is also inclusive,  001 ends on 3880

# The whole sequence starts at 3280 and ends at 14600
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc

echo SEQUENCE: $SEQUENCE
echo SEQUENCE_START_TIMESTAMP: $SEQUENCE_START_TIMESTAMP
echo SEQUENCE_END_TIMESTAMP: $SEQUENCE_END_TIMESTAMP

python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
