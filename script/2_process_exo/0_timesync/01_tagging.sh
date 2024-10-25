###----------------------------------------------------------------------------
BIG_SEQUENCE='01_tagging'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
# OUTPUT_DIR="/home/rawalk/Desktop/datasets/ego_exo/main"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

###-------------for tagging---------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08"

# ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='001_tagging'

# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='01310' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01910' ## this is also inclusive

# # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='002_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02040' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='02259' ## this is also inclusive


# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='003_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02350' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='02660' ## this is also inclusive

# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='004_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02780' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='02900' ## this is also inclusive

# # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='005_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# # SEQUENCE_START_TIMESTAMP='03340' ## this includes the image name
# # SEQUENCE_END_TIMESTAMP='04500' ## this is also inclusive

# SEQUENCE_START_TIMESTAMP='03340' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03780' ## this is also inclusive

# # # # # ###--------------------------------
# SEQUENCE='012_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03805' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03993' ## this is also inclusive


# # # # # # ###--------------------------------
# SEQUENCE='013_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04076' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04243' ## this is also inclusive


# # # # # # ###--------------------------------
# SEQUENCE='014_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04288' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04487' ## this is also inclusive


# # # # # # ###--------------------------------
START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
SEQUENCE='006_tagging'

## pick the sequence start and end times with respect to an ego camera
SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04830' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05400' ## this is also inclusive

SEQUENCE_START_TIMESTAMP='04979' ## this includes the image name, add 4830 + target frame - 1
SEQUENCE_END_TIMESTAMP='05349' ## this is also inclusive


# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='007_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05470' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06185' ## this is also inclusive

# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='008_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06620' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06820' ## this is also inclusive

# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='009_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08880' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09450' ## this is also inclusive

# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='010_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='09550' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09970' ## this is also inclusive

# # # # # ###--------------------------------
# START_TIMESTAMPS="00714--00001--00001--00001--00001--00001--00011--00001--00001" 
# SEQUENCE='011_tagging'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10050' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='10810' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \