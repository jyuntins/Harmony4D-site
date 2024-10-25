###----------------------------------------------------------------------------
BIG_SEQUENCE='uncego4d'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE"

# # ##----------------------------------------------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04"

# # START_TIMESTAMPS="08570--06809--06609--06405--06231"  ## actual sync

# START_TIMESTAMPS="00001--00001--00001--00001--00001"  ## dummy
# SEQUENCE='calibration_uncego4d'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00010' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01010' ## this is also inclusive

# ##----------------------------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04"

START_TIMESTAMPS="08570--06809--06609--06405--06231"  ## actual sync
SEQUENCE='001_uncego4d'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='08600' ## this includes the image name
SEQUENCE_END_TIMESTAMP='09200' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \