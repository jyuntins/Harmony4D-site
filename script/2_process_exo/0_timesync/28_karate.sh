###----------------------------------------------------------------------------
BIG_SEQUENCE='28_karate'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# ## second throw of the ball
# CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="01575--01087--00937--01230--01515--01186--01433--01487--01457--01007--01092--00971--00700--00795--00833--00653--01047--01266--01243--01542"

# SEQUENCE='calibration_karate'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='01000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01400' ## this is also inclusive


###-------------for calibration---------------
## second throw of the ball
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="01575--01087--00937--01230--01515--01186--01433--01487--01457--01007--01092--00971--00700--00795--00833--00653--01047--01266--01243--01542"

SEQUENCE='006_karate'
SEQUENCE_CAMERA_NAME='cam01'
SEQUENCE_START_TIMESTAMP='09386' ## this includes the image name
SEQUENCE_END_TIMESTAMP='09685' ## this is also inclusive

# 001_karate 2600-3800
# 002_karate 3790-4990
# 003_karate 4981-6100
# 004_karate 07330-08410
# 005_karate 08401-09430
# 006_karate 09386-09685
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
