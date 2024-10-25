###----------------------------------------------------------------------------
BIG_SEQUENCE='24_tennis'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # # # # # # ###-------------for calibration---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="00010--06133--06979--07082--07050--06309--06470--04352--04439--04588--04661--04849--05118--05240--05296--05418--05531--05651--05778--05886--06012"

# SEQUENCE='calibration_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00011' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01300' ## this is also inclusive

# # # # # # ###----------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
START_TIMESTAMPS="02296--06133--06979--07082--07050--06309--06470--04352--04439--04588--04661--04849--05118--05240--05296--05418--05531--05651--05778--05886--06012"


# SEQUENCE='001_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03500' ## this is also inclusive

# SEQUENCE='002_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04700' ## this is also inclusive

# SEQUENCE='003_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04800' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06000' ## this is also inclusive

# SEQUENCE='004_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07300' ## this is also inclusive


# SEQUENCE='005_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='07300' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08500' ## this is also inclusive


# SEQUENCE='006_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08600' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09900' ## this is also inclusive


# SEQUENCE='007_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11550' ## this is also inclusive


# SEQUENCE='008_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='11700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='12900' ## this is also inclusive

# SEQUENCE='009_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='12900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='14100' ## this is also inclusive

# SEQUENCE='010_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='14140' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='15640' ## this is also inclusive

# SEQUENCE='011_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='15760' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='16900' ## this is also inclusive


# SEQUENCE='012_tennis'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='16900' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='18200' ## this is also inclusive

SEQUENCE='013_tennis'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='18300' ## this includes the image name
SEQUENCE_END_TIMESTAMP='19200' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
