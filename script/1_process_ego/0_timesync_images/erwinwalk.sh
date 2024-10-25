###----------------------------------------------------------------------------
BIG_SEQUENCE='erwinwalk'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # ###--------------------------------
# CAMERAS="aria01" ## 4 arias
# START_TIMESTAMPS="00001" ## this is the first throw, first bounce 

# # # # ###--------------------------------
# SEQUENCE='calibration_erwinwalk'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00010' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01010' ## this is also inclusive

# # # ###--------------------------------
CAMERAS="aria01" 
START_TIMESTAMPS="11623"

# # # ###--------------------------------
SEQUENCE='001_erwinwalk'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='11650' ## this includes the image name
SEQUENCE_END_TIMESTAMP='12250' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
