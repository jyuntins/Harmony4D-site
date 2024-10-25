###----------------------------------------------------------------------------
BIG_SEQUENCE='19_sword2'

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
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="01141--00703--00758--01290--01007--00897--00811--01384--00854--00560--00943--01216--00516--01095--01177--00606--00655--01248--01328--01052"

SEQUENCE='010_sword2'
SEQUENCE_CAMERA_NAME="cam01"
SEQUENCE_START_TIMESTAMP='10721' ## this includes the image name
SEQUENCE_END_TIMESTAMP='11920' ## this is also inclusive

# 001_sword2 01350 - 02400
# 002_sword2 02390 - 03300
# 003_sword2 03291 - 04410
# 004_sword2 04401 - 05360
# 005_sword2 05351 - 06525
# 006_sword2 06516 - 07670
# 007_sword2 07661 - 08790
# 008_sword2 08781 - 09700
# 009_sword2 09691 - 10730
# 010_sword2 10721 - 11920
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
