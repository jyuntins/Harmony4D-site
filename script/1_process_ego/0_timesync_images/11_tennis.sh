###----------------------------------------------------------------------------
BIG_SEQUENCE='11_tennis' ## assemble

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # ###-------------for tennis---------------
# CAMERAS="aria01--aria02--aria03--aria04" ## 4 arias
# START_TIMESTAMPS="05566--05521--05341--05046" ##second throw from the building side (this is the second attempt to sync), first bounce by rawal

# SEQUENCE='calibration_tennis'
# SEQUENCE_CAMERA_NAME='aria01'

# # SEQUENCE_START_TIMESTAMP='06000:36000' ## this includes the image name
# # SEQUENCE_END_TIMESTAMP='09200:38000' ## this is also inclusive

# SEQUENCE_START_TIMESTAMP='05600:36000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09600:39000' ## this is also inclusive


# # ###-------------for tennis---------------
CAMERAS="aria01--aria02--aria03--aria04" ## 4 arias
START_TIMESTAMPS="05566--05521--05341--05046"

SEQUENCE='001_tennis'
SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06600' ## this is also inclusive

SEQUENCE_START_TIMESTAMP='06700' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07300' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
