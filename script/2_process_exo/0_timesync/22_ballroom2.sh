###----------------------------------------------------------------------------
BIG_SEQUENCE='22_ballroom2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # # # # # ###-------------for calibration---------------
# # # # # # ## event: rawal in center, ball bounce, first touch
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"

# # ## add 500 to all timestamps
# START_TIMESTAMPS="00200--01624--01497--00734--01232--01416--01461--01802--02037--01946--01759--01988--01531--01090--02105--02192--01726--01309--01721--01580--01130"

# SEQUENCE='calibration_ballroom'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00200' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive

# # # # # ###----------------------------
## We don't have camera 6 in this video!
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="03025--02899--02649--02596--02814--03149--03345--03260--03103--03306--02934--02422--03408--03450--03176--02696--03064--02985--02484"

# SEQUENCE='001_ballroom2'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='10104' ## this includes the image name first sequence start at 3360
# SEQUENCE_END_TIMESTAMP='10704' ## this is also inclusive first sequence end at 3960

# 001_ballroom2 03330 04330
# 002_ballroom2 04321 05430
# 003_ballroom2 05421 06450

# 004_ballroom2 07035 08040
# 005_ballroom2 08031 08985
# 006_ballroom2 08976 09645
# 007_ballroom2 09636 10410
cd ../../../tools/misc
SEQUENCES=("001_ballroom2" "002_ballroom2" "003_ballroom2" "004_ballroom2" "005_ballroom2" "006_ballroom2" "007_ballroom2")
SEQUENCE_START_TIMESTAMPS=("03330" "04321" "05421" "07035" "08031" "08976" "09636")
SEQUENCE_END_TIMESTAMPS=("04330" "05430" "06450" "08040" "08985" "09645" "10410")
for (( i=0; i<=6; i++ ))
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

# ###----------------------------------------------------------------------------
# OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

# ###----------------------------------------------------------------------------
# cd ../../../tools/misc
# python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                             --start-timestamps $START_TIMESTAMPS \
#                             --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                             --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                             --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
