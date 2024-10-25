###----------------------------------------------------------------------------
BIG_SEQUENCE='18_sword'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# # START_TIMESTAMPS="00320--01390--00994--01049--01543--01279--01179--01106--00470--01146--00852--01221--01461--00814--01352--01419--00900--00950--01499--01591--01314"

# # # ## add 500 to all timestamps
# START_TIMESTAMPS="00320--01890--01494--01549--02043--01779--01679--01606--00970--01646--01352--01721--01961--01314--01852--01919--01400--01450--01999--02091--01814"

# SEQUENCE='calibration_sword3'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00320' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01320' ## this is also inclusive

 ###----------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="02694--00771--00381--00429--00912--00646--00546--00473--01008--00512--00253--00588--00841--00208--00730--00809--00297--00336--00883--00971--00687"

SEQUENCE='005_sword'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='05710' ## this includes the image name
SEQUENCE_END_TIMESTAMP='06250' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
echo SEQUENCE: $SEQUENCE
echo SEQUENCE_START_TIMESTAMP: $SEQUENCE_START_TIMESTAMP
echo SEQUENCE_END_TIMESTAMP: $SEQUENCE_END_TIMESTAMP

python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
