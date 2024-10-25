###----------------------------------------------------------------------------
BIG_SEQUENCE='05_frisbee'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main"

###-------------for frisbee_1---------------
CAMERAS="aria01--aria02--aria03--aria04--aria05--aria06" ## 6 arias
START_TIMESTAMPS="00805--01061--00695--01406--00851--02043" ##this 00001.jpg for the exo cameras

# # ###--------------------------------
SEQUENCE='calibration_frisbee'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='02000:04000:05500' ## this includes the image name
SEQUENCE_END_TIMESTAMP='03000:05000:06500' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='001_frisbee'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='01900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='02180' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$BIG_SEQUENCE/$SEQUENCE/'ego'


###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
