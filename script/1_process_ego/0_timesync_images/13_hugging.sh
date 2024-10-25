###----------------------------------------------------------------------------
BIG_SEQUENCE='13_hugging' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"


# ###-------------hugging---------------
# CAMERAS="aria01--aria02" ## 4 arias
# START_TIMESTAMPS="00280--00450" ##second throw from the building side (this is the second attempt to sync), first bounce by rawal

# SEQUENCE='calibration_hugging'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00281' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01281' ## this is also inclusive

# ###-------------hugging---------------
CAMERAS="aria01--aria02" ## 4 arias
START_TIMESTAMPS="04662--04822" ##second throw from the building side (this is the second attempt to sync), first bounce by rawal

SEQUENCE='002_hugging'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='06500' ## this includes the image name 05790
SEQUENCE_END_TIMESTAMP='06800' ## this is also inclusive 06090

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
