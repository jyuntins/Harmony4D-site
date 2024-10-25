###----------------------------------------------------------------------------
BIG_SEQUENCE='21_ballroom'

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
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="03101--01124--00997--00234--00732--00916--00961--01302--01537--01446--01259--01488--01031--00590--01605--01692--01355--00809--01221--01080--00630"

SEQUENCE='011_ballroom'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='10104' ## this includes the image name first sequence start at 3360
SEQUENCE_END_TIMESTAMP='10704' ## this is also inclusive first sequence end at 3960

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
