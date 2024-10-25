###----------------------------------------------------------------------------
BIG_SEQUENCE='15_grappling2' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # # # ###-------------for calibration---------------
# # # # ## event: rawal in center, ball bounce, first touch
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# # START_TIMESTAMPS="00100--00753--00375--00466--00306--00584--00788--00529--00550--00412--00440--00200--00142--00238--00612--00697--00340--00660--00718--00501--00273"

# ## add 500 to all timestamps
# START_TIMESTAMPS="00100--01253--00875--00966--00806--01084--01288--01029--01050--00912--00940--00700--00642--00738--01112--01197--00840--01160--01218--01001--00773"

# SEQUENCE='calibration_grappling2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive


# # # # ###-------------for calibration---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="02067--00753--00375--00466--00306--00584--00788--00529--00550--00412--00440--00200--00142--00238--00612--00697--00340--00660--00718--00501--00273"

# SEQUENCE='001_grappling2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02590' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03190' ## this is also inclusive

SEQUENCE='019_grappling2'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='14009' ## this includes the image name
SEQUENCE_END_TIMESTAMP='14609' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
