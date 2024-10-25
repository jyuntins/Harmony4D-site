###----------------------------------------------------------------------------
BIG_SEQUENCE='11_tennis' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # ###-------------for calibration tennis---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="05566--01631--01470--01556--01743--01233--01787--01145--01561--01086--01376--01916--01206--01441--01335--01307"

# SEQUENCE='calibration_tennis'
# SEQUENCE_CAMERA_NAME='aria01'

# # SEQUENCE_START_TIMESTAMP='06000:36000' ## this includes the image name
# # SEQUENCE_END_TIMESTAMP='09200:38000' ## this is also inclusive

# SEQUENCE_START_TIMESTAMP='05600:36000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09600:39000' ## this is also inclusive


# ###-------------for tennis---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
START_TIMESTAMPS="05566--01631--01470--01556--01743--01233--01787--01145--01561--01086--01376--01916--01206--01441--01335--01307"


SEQUENCE='001_tennis'
SEQUENCE_CAMERA_NAME='aria01'

SEQUENCE_START_TIMESTAMP='06700' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07300' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
