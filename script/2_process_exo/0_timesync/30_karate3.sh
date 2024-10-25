###----------------------------------------------------------------------------
BIG_SEQUENCE='30_karate3'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # ###-------------for calibration---------------
# ## second throw of the ball
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="00280--01234--00782--00585--00888--01143--00850--01025--01105--01029--00628--00761--00566--00348--00430--00482--00298--00672--00930--00888--01141"

# SEQUENCE='calibration_karate3'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00300' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01280' ## this is also inclusive

###-------------for karate---------------
## second throw of the ball
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="02676--01234--00782--00585--00888--01143--00850--01025--01105--01029--00628--00761--00566--00348--00430--00482--00298--00672--00930--00888--01141"


# SEQUENCE='001_karate3'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='02500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03700' ## this is also inclusive

SEQUENCE='006_karate3'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='06947' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07547' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
