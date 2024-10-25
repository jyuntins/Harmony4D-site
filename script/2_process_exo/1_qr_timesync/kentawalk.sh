###----------------------------------------------------------------------------
BIG_SEQUENCE='kentawalk'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE"

# # ##----------------------------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
QR_TIMESTAMPS="01433:1675291110192--00065:1675291057135--00045:1675291066392--00049:1675291075631--00067:1675291085138--00044:1675291093129--00057:1675291103133--00057:1675291113888--00053:1675291125142"  ## real

# FPS=30
FPS=20

# # ###-----------------------------------------------------------------
# SEQUENCE='001_kentawalk'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03600' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04200' ## this is also inclusive

# # # ###-----------------------------------------------------------------
# SEQUENCE='002_kentawalk'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05050' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05550' ## this is also inclusive

# # # ###-----------------------------------------------------------------
# SEQUENCE='003_kentawalk'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07000' ## this is also inclusive

# # ###-----------------------------------------------------------------
SEQUENCE='004_kentawalk'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='07900' ## this includes the image name
SEQUENCE_END_TIMESTAMP='08400' ## this is also inclusive


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