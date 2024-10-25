###----------------------------------------------------------------------------
BIG_SEQUENCE='pro_soccer'

# DATA_DIR="/home/rawalk/Desktop/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"

# OUTPUT_DIR="/home/rawalk/Desktop/datasets/ego_exo/main"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"

###-------------for pro soccer---------------
CAMERAS="aria01--aria02--aria04--aria05--aria06" ## 5 arias
START_TIMESTAMPS="05003--05823--08564--09180--10446" ##this 00001.jpg for the exo cameras

# ###--------------------------------
SEQUENCE='002_pro_soccer_1'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='05420' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06239' ## this is also inclusive
# SEQUENCE_END_TIMESTAMP='07420' ## this is also inclusive
SEQUENCE_END_TIMESTAMP='10420' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'


###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
