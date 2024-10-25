###----------------------------------------------------------------------------
BIG_SEQUENCE='pro_soccer'
# DATA_DIR="/home/rawalk/Desktop/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
# OUTPUT_DIR="/home/rawalk/Desktop/datasets/ego_exo/main"

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"

###-------------for tagging_2---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10"
START_TIMESTAMPS="05003--04487--01299--01851--02674--02123--03951--02973--01650--03623--02094" 

# ###--------------------------------
SEQUENCE='002_pro_soccer_1'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='05420' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06239' ## this is also inclusive
# SEQUENCE_END_TIMESTAMP='07420' ## this is also inclusive
# SEQUENCE_END_TIMESTAMP='07420' ## this is also inclusive
SEQUENCE_END_TIMESTAMP='10420' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \