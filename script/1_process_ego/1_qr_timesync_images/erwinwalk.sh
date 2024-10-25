###----------------------------------------------------------------------------
BIG_SEQUENCE='erwinwalk'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # ###--------------------------------
CAMERAS="aria01" ## 4 arias
FPS=30
QR_TIMESTAMPS="03950:1674651186980" ## this is the first throw, first bounce , cams separate by ---, image id: qr timestamp

# # ###--------------------------------
SEQUENCE='001_erwinwalk'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='13000' ## this includes the image name
SEQUENCE_END_TIMESTAMP='13700' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python qr_ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --frame_rate $FPS \
                            --qr-timestamps $QR_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
