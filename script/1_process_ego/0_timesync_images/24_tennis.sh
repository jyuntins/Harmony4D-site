###----------------------------------------------------------------------------
BIG_SEQUENCE='24_tennis'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


###-----------------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00010--00010" ##third throw by rawal

# SEQUENCE='calibration_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00011' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01300' ## this is also inclusive

##----------------------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="02296--02474" ##third throw by rawal

# SEQUENCE='001_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03500' ## this is also inclusive

# SEQUENCE='002_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04700' ## this is also inclusive

# SEQUENCE='003_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04800' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06000' ## this is also inclusive

# SEQUENCE='004_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07300' ## this is also inclusive

# SEQUENCE='005_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='07300' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08500' ## this is also inclusive

# SEQUENCE='006_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08600' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09900' ## this is also inclusive

# SEQUENCE='007_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11550' ## this is also inclusive

# SEQUENCE='008_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='11700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='12900' ## this is also inclusive

# SEQUENCE='009_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='12900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='14100' ## this is also inclusive

# SEQUENCE='010_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='14140' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='15640' ## this is also inclusive

# SEQUENCE='011_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='15760' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='16900' ## this is also inclusive

# SEQUENCE='012_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='16900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='18200' ## this is also inclusive

SEQUENCE='013_tennis'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='18300' ## this includes the image name
SEQUENCE_END_TIMESTAMP='19200' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
