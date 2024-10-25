###----------------------------------------------------------------------------
BIG_SEQUENCE='29_karate2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# ## second throw of the ball
# CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="01575--01087--00937--01230--01515--01186--01433--01487--01457--01007--01092--00971--00700--00795--00833--00653--01047--01266--01243--01542"

# SEQUENCE='calibration_karate2'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='01000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01400' ## this is also inclusive


###-------------for calibration---------------
## second throw of the ball
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="01618--01099--00939--01291--01554--01236--01448--01524--01442--00979--01120--00910--00737--00778--00827--00278--01009--01343--01275--01585"

cd ../../../tools/misc
# SEQUENCES=("001_karate2" "002_karate2" "003_karate2" "004_karate2")
# SEQUENCE_START_TIMESTAMPS=("01880" "02991" "04141" "05101")
# SEQUENCE_END_TIMESTAMPS=("03000" "04150" "05110" "05500")
# for (( i=0; i<=3; i++ ))
# do
#     SEQUENCE_CAMERA_NAME="cam01"
#     SEQUENCE=${SEQUENCES[i]}
#     SEQUENCE_START_TIMESTAMP=${SEQUENCE_START_TIMESTAMPS[i]} ## this includes the image name
#     SEQUENCE_END_TIMESTAMP=${SEQUENCE_END_TIMESTAMPS[i]} ## this is also inclusive
#     OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'
#     python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                                 --start-timestamps $START_TIMESTAMPS \
#                                 --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                                 --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                                 --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \

# done

SEQUENCE='calibration_karate2'
SEQUENCE_CAMERA_NAME='cam01'
SEQUENCE_START_TIMESTAMP='02600' ## this includes the image name
SEQUENCE_END_TIMESTAMP='03800' ## this is also inclusive

# 001_karate2 01880 - 03000
# 002_karate2 02991 - 04150
# 003_karate2 04141 - 05110
# 004_karate2 05101 - 05500
###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
# cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
