###----------------------------------------------------------------------------
BIG_SEQUENCE='06_volleyball'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # ###--------------------------------
CAMERAS="aria01--aria02--aria03--aria04" ## 4 arias
# START_TIMESTAMPS="02537--03062--02435--02845" ## this is the second throw, first bounce 
START_TIMESTAMPS="02361--02886--02258--02669" ## this is the first throw, first bounce 

# # # ###--------------------------------
# SEQUENCE='calibration_volleyball'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03410:7500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05410:9500' ## this is also inclusive

# # # ###--------------------------------
# SEQUENCE='001_volleyball'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03410' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04010' ## this is also inclusive

# # # # ###--------------------------------
# SEQUENCE='002_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04010' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04610' ## this is also inclusive

# # # # # ###--------------------------------
# SEQUENCE='003_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04610' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05090' ## this is also inclusive

# # # # ###--------------------------------
# SEQUENCE='004_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05700' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='005_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05850' ## this is also inclusive

# ##--------------------------------
# SEQUENCE='006_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06050' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06650' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='007_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06650' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07250' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='008_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='07550' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08150' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='009_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08150' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08750' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='010_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08750' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09350' ## this is also inclusive

# # ##--------------------------------
SEQUENCE='011_volleyball'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='09350' ## this includes the image name
SEQUENCE_END_TIMESTAMP='09950' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'ego'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python ego_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
