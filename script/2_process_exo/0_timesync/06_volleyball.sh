###----------------------------------------------------------------------------
BIG_SEQUENCE='06_volleyball'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE"

# ##----------------------------------------------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="02361--03928--03993--03879--05139--04166--03409--04231--03629--05738--03705--03971--04618--04346--03777--04547" 

# # # # # # ###--------------------------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="02361--03928--03993--03879--05139--04166--03409--04231--03629--05738--03705--03971--04595--04346--03777--04524"  ## cam12 dropped around 22 frames, cam15 dropped 23 frames

# SEQUENCE='calibration_volleyball'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03410:7500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05410:9500' ## this is also inclusive

# # # ###--------------------------------
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
START_TIMESTAMPS="02361--03928--03993--03879--05139--04166--03409--04231--03629--05738--03705--03971--04595--04346--03777--04524"  ## cam12 dropped around 22 frames, cam15 dropped 23 frames

# SEQUENCE='001_volleyball'

# ## pick the sequence start and end times with respect to an ego camera
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03410' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04010' ## this is also inclusive

# # ##----------------------------------------------------
# SEQUENCE='002_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04010' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04610' ## this is also inclusive

# # # # ###--------------------------------
# SEQUENCE='003_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04610' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05090' ## this is also inclusive

# # # # ###--------------------------------
# SEQUENCE='004_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05100' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05700' ## this is also inclusive

# # # ##--------------------------------
# SEQUENCE='005_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='05700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='05850' ## this is also inclusive

# # # ##--------------------------------
# SEQUENCE='006_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06050' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='06650' ## this is also inclusive

# # # ##--------------------------------
# SEQUENCE='007_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='06650' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07250' ## this is also inclusive

# # # ##--------------------------------
# SEQUENCE='008_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='07550' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08150' ## this is also inclusive

# # ##--------------------------------
# SEQUENCE='009_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08150' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08750' ## this is also inclusive

# # # # ##--------------------------------
# SEQUENCE='010_volleyball'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08750' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09350' ## this is also inclusive

# # # ##--------------------------------
SEQUENCE='011_volleyball'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='09350' ## this includes the image name
SEQUENCE_END_TIMESTAMP='09950' ## this is also inclusive


###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \