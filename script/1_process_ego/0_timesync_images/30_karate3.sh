###----------------------------------------------------------------------------
BIG_SEQUENCE='30_karate3'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


 ###-------------karate---------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00280--00180" ##third throw by rawal

# SEQUENCE='calibration_karate3'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00300' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01280' ## this is also inclusive

 ###-------------karate---------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="02676--02600" ##third throw by rawal

SEQUENCE='006_karate3'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='06947' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07547' ## this is also inclusive

# 012_karate3 10730 11152
#11800
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
