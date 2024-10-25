###----------------------------------------------------------------------------
BIG_SEQUENCE='35_mma5'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

###-------------for calibration---------------
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="00949--00854--00821--00709--00785--00976--00395--00431--00500--00937--00457--00962--01079--01007--00291--00619--00579--01044--00726--00866"

cd ../../../tools/misc

SEQUENCES=("001_mma5" "002_mma5" "003_mma5" "004_mma5")
SEQUENCE_START_TIMESTAMPS=("01120" "02210" "03301" "04271")
SEQUENCE_END_TIMESTAMPS=("02130" "03310" "04280" "04880")
for (( i=0; i<=5; i++ ))
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

# 001_mma5 01120 02130
# 002_mma5 02210 03310
# 003_mma5 03301 04280
# 004_mma5 04271 04880
###----------------------------------------------------------------------------
# OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

# ###----------------------------------------------------------------------------
# cd ../../../tools/misc
# python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                             --start-timestamps $START_TIMESTAMPS \
#                             --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                             --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                             --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
