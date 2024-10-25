###----------------------------------------------------------------------------
BIG_SEQUENCE='16_grappling3'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

###-------------for calibration---------------
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="01374--00919--01031--00847--01170--01433--01102--01134--00955--00995--00738--00701--00772--01201--01297--00883--01249--01336--01064--00808"

cd ../../../tools/misc

SEQUENCES=("001_grappling3" "002_grappling3" "003_grappling3" "004_grappling3" "005_grappling3" "006_grappling3" "007_grappling3" "008_grappling3" "009_grappling3" "010_grappling3" "011_grappling3" "012_grappling3")
SEQUENCE_START_TIMESTAMPS=("01540" "02701" "03741" "04761" "05741" "06861" "07821" "09001" "10141" "11291" "11866" "12671")
SEQUENCE_END_TIMESTAMPS=("02710" "03750" "04770" "05750" "06870" "07830" "09010" "10150" "11300" "11875" "12680" "13680")
for (( i=0; i<=11; i++ ))
do
    SEQUENCE_CAMERA_NAME="cam01"
    SEQUENCE=${SEQUENCES[i]}
    SEQUENCE_START_TIMESTAMP=${SEQUENCE_START_TIMESTAMPS[i]} ## this includes the image name
    SEQUENCE_END_TIMESTAMP=${SEQUENCE_END_TIMESTAMPS[i]} ## this is also inclusive
    OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'
    python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                                --start-timestamps $START_TIMESTAMPS \
                                --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                                --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                                --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \

done








# SEQUENCE='012_grappling3'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='12671'
# SEQUENCE_END_TIMESTAMP='13680'
##----------------------------------------------------------------------------
# 001_grappling3 1540-02710
# 002_grappling3 2701-03750
# 003_grappling3 3741-04770
# 004_grappling3 4761-5750
# 005_grappling3 5741-6870
# 006_grappling3 6861-7830
# 007_grappling3 7821-9010
# 008_grappling3 9001-10150
# 009_grappling3 10141-11300
# 010_grappling3 11291-11875
# 011_grappling3 11866-12680
# 012_grappling3 12671-13680


# OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

# cd ../../../tools/misc
# python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                             --start-timestamps $START_TIMESTAMPS \
#                             --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                             --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                             --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
