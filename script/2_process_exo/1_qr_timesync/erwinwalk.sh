###----------------------------------------------------------------------------
BIG_SEQUENCE='erwinwalk'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE"

# # ##----------------------------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"
FPS=30
QR_TIMESTAMPS="03950:1674651186980--00473:1674651115236--00068:1674651130735--00095:1674651136984--00079:1674651143984--00132:1674651151734--00065:1674651157731--00237:1674651167484--00189:1674651172982"  ## dummy

SEQUENCE='001_erwinwalk'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='13000' ## this includes the image name
SEQUENCE_END_TIMESTAMP='13700' ## this is also inclusive

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