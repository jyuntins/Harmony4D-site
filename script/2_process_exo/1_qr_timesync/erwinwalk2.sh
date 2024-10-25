###----------------------------------------------------------------------------
BIG_SEQUENCE='erwinwalk2'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE"

# # ##----------------------------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
QR_TIMESTAMPS="00005:1675290012520--00070:1675290129168--00025:1675290156170--00020:1675290165426--00060:1675290175415--00026:1675290183173--00059:1675290191180--00078:1675290201169--00110:1675290208927"  ## real
# QR_TIMESTAMPS="00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520--00005:1675290012520"  ## dummy

# FPS=30
FPS=20

# ###-----------------------------------------------------------------
# SEQUENCE='calibration_erwinwalk2'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00250' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01200' ## this is also inclusive

# # # ###--------------------------------
# SEQUENCE='001_erwinwalk2'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06875' ## this is also inclusive


# # # ###--------------------------------
# SEQUENCE='002_erwinwalk2'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08410' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08780' ## this is also inclusive


# # # ###--------------------------------
# SEQUENCE='003_erwinwalk2'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='11000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='11800' ## this is also inclusive

# # ###--------------------------------
SEQUENCE='004_erwinwalk2'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='14500' ## this includes the image name
SEQUENCE_END_TIMESTAMP='15200' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python qr_exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --frame_rate $FPS \
                            --qr-timestamps $QR_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \