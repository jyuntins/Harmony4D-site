###----------------------------------------------------------------------------
BIG_SEQUENCE='31_mma'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # ###-------------for calibration---------------
# # ## second throw of the ball
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="00090--00606--00673--00716--00807--00753--01275--01016--00984--00848--01183--00889--01151--01020--01083--00989--00782--00818--01050--00721--00580"

# SEQUENCE='calibration_mma'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01000' ## this is also inclusive

# ---------------------------------------------------------------------
# # ## second throw of the ball
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="02832--00606--00673--00716--00807--00753--01275--01016--00984--00848--01183--00889--01151--01020--01083--00989--00782--00818--01050--00721--00580"

SEQUENCE='007_mma'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='06750' ## this includes the image name
SEQUENCE_END_TIMESTAMP='07015' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
