###----------------------------------------------------------------------------
BIG_SEQUENCE='14_grappling' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # # ###-------------for calibration---------------
# # # ## event: rawal in center, ball bounce, first touch
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# # START_TIMESTAMPS="00100--01456--00678--00848--00597--01068--00182--00960--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"

# ## add 500 to all timestamps
# START_TIMESTAMPS="00100--01956--01178--01348--01097--01568--00682--01460--01494--01207--01305--00934--00745--01015--01574--01738--01135--01658--01845--01394--01056"

# SEQUENCE='calibration_grappling'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01100' ## this is also inclusive


# # # # ###-------------for calibration---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="03263--01456--00678--00848--00597--01068--00182--00960--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"
# START_TIMESTAMPS="03263--01456--00678--00848--00597--01068--00182--00937--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"
# START_TIMESTAMPS="03263--01456--00678--00848--00597--01068--00182--00939--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"
# START_TIMESTAMPS="03263--01456--00678--00848--00597--01068--00182--00938--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"
START_TIMESTAMPS="03263--01456--00678--00848--00597--01068--00182--00940--00994--00707--00805--00434--00245--00515--01074--01238--00635--01158--01345--00894--00556"


SEQUENCE='001_grappling'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='03900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04500' ## this is also inclusive
SEQUENCE_END_TIMESTAMP='05100' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
