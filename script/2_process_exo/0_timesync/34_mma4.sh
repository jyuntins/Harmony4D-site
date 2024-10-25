###----------------------------------------------------------------------------
BIG_SEQUENCE='34_mma4'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

###-------------for calibration---------------
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="01326--01211--01182--01073--01147--01354--00499--00528--00838--01322--00573--01349--00370--01375--00413--00986--00917--00256--01050--01240"

cd ../../../tools/misc

# SEQUENCES=("001_mma4" "002_mma4" "003_mma4" "004_mma4"  "005_mma4" "006_mma4")
# SEQUENCE_START_TIMESTAMPS=("01500" "02551" "03726" "04861" "05806" "06691")
# SEQUENCE_END_TIMESTAMPS=("02560" "03735" "04870" "05815" "06700" "07620")
SEQUENCES=("calibration_mma4")
SEQUENCE_START_TIMESTAMPS=("01500")
SEQUENCE_END_TIMESTAMPS=("02560")

for (( i=0; i<=0; i++ ))
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

# 001_mma4 01500 02560
# 002_mma4 02551 03735
# 003_mma4 03726 04870
# 004_mma4 04861 05815
# 005_mma4 05806 06700
# 006_mma4 06691 07620

###----------------------------------------------------------------------------
# OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

# ###----------------------------------------------------------------------------
# cd ../../../tools/misc
# python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                             --start-timestamps $START_TIMESTAMPS \
#                             --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                             --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                             --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
