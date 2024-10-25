###----------------------------------------------------------------------------
BIG_SEQUENCE='13_hugging' ## 

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# # # # ###-------------for calibration---------------
# # ## event: rawal in center, ball bounce, first touch
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20--cam21--cam22"
# START_TIMESTAMPS="00280--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200--00200"

# ## cam12, cam13 needs fixing
# SEQUENCE='calibration_hugging'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='00281' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01281' ## this is also inclusive


# # # ###-------------for calibration---------------
# Start_timestamps is the frame of the same event in all the cameras. 
# In this case, It's the moment of the ball thrown by Rawal touched the ground. 
# Therefore, in aria01, the frame of 4662 and the frame of 2973 in cam01 are the same event. 
# We use this frame as a signal to sync all the cameras.
# Sequence start timestamp is the timestamp of the start of the event.
# It is based on the specified sequence camera.
# In this case, the sequence camera we use as a reference is aria01.
# The start of the sequence in aria01 is the frame of 5790 and it ends at the frame of 6090.

## event: rawal in center, ball bounce, first touch
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20--cam21--cam22"
START_TIMESTAMPS="04662--02973--02944--02917--02885--02856--02193--02143--02040--01989--01947--01915--01882--01850--01824--01798--01763--01727--01697--01663--01634--01602--1039"

# ## cam12, cam13 needs fixing


SEQUENCE='002_hugging'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='06500' ## this includes the image name
SEQUENCE_END_TIMESTAMP='06800' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
