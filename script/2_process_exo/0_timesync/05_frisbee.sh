###----------------------------------------------------------------------------
BIG_SEQUENCE='05_frisbee'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/"


CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10"
START_TIMESTAMPS="00805--06512--06784--06108--07844--07583--03741--07395--05027--05289--07161"  ## working correctly
# START_TIMESTAMPS="00805--06512--06784--05922--07844--07583--03741--07395--05027--05289--07161" 

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
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \