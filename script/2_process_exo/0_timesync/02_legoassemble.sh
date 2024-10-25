###----------------------------------------------------------------------------
BIG_SEQUENCE='02_legoassemble' ## assemble

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for lego---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
# START_TIMESTAMPS="00462--05511--05414--05151--05603--05313--05810--04371--05679" 

# # ###--------------------------------
# SEQUENCE='001_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='0700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01900' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='002_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02050' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03250' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='003_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03570' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04370' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='004_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05990' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07030' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='005_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='07480' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08680' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='006_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08830' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09930' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='007_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10010' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11210' ## this is also inclusive

# # ###--------------------------------
# SEQUENCE='008_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='11490' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='12660' ## this is also inclusive


# ###-------------non crouching---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
# START_TIMESTAMPS="00462--05511--05414--05151--05603--05313--05810--04371--05679" 

# SEQUENCE='001_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08920' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09520' ## this is also inclusive

###-------------for lego---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
START_TIMESTAMPS="00462--05511--05414--05151--05603--05313--05810--04371--05679" 

SEQUENCE='002_legoassemble'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='09530' ## this includes the image name
SEQUENCE_END_TIMESTAMP='09980' ## this is also inclusive

# SEQUENCE='003_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10260' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='10860' ## this is also inclusive

# SEQUENCE='004_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10870' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11470' ## this is also inclusive

# SEQUENCE='005_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='11480' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11850' ## this is also inclusive

# SEQUENCE='006_legoassemble'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='12460' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='12700' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \