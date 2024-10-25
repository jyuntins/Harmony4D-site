###----------------------------------------------------------------------------
BIG_SEQUENCE='07_fencing2' ## assemble

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

###-------------for fencing without masks on---------------
# CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="02491--01483--01558--01374--00692--01526--01075--01680--01642--01036--01324--01170--01720--01415--01597--00879" 

# SEQUENCE='calibration_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03500' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='001_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='02700' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03300' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='002_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03310' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='03910' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='003_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='03920' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04520' ## this is also inclusive


# ##---------------------------------------------------
# SEQUENCE='004_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='04530' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='04840' ## this is also inclusive

# # ##---------------------------------------------------
# ## remove cam08 post the restart
CAMERAS="aria01--cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
START_TIMESTAMPS="02491--01483--01558--01374--00692--01526--01075--01680--01036--01324--01170--01720--01415--01597--00879" 

# SEQUENCE='005_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='08600' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='006_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='08610' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09210' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='007_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='09220' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='09820' ## this is also inclusive


# ##---------------------------------------------------
# SEQUENCE='008_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='09830' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='10430' ## this is also inclusive


# ##---------------------------------------------------
# SEQUENCE='009_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='10500' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='10930' ## this is also inclusive


# ##---------------------------------------------------
SEQUENCE='010_fencing2'
SEQUENCE_CAMERA_NAME='aria01'
SEQUENCE_START_TIMESTAMP='11470' ## this includes the image name
SEQUENCE_END_TIMESTAMP='12020' ## this is also inclusive

##---------------------------------------------------
# # ##---------------------------------------------------
# ## remove cam03 at this point
# CAMERAS="aria01--cam01--cam02--cam04--cam05--cam06--cam07--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="02491--01483--01558--00692--01526--01075--01680--01036--01324--01170--01720--01415--01597--00879" 


# SEQUENCE='011_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='12070' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='12670' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='012_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='12680' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='13150' ## this is also inclusive

# ##---------------------------------------------------
# SEQUENCE='013_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='13610' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='13920' ## this is also inclusive

##---------------------------------------------------
# # ##---------------------------------------------------
# ## remove cam03, 06, 07 ,08 at this point
# CAMERAS="aria01--cam01--cam02--cam04--cam05--cam09--cam10--cam11--cam12--cam13--cam14--cam15"
# START_TIMESTAMPS="02491--01483--01558--00692--01526--01036--01324--01170--01720--01415--01597--00879" 

# SEQUENCE='014_fencing2'
# SEQUENCE_CAMERA_NAME='aria01'
# SEQUENCE_START_TIMESTAMP='14540' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='14870' ## this is also inclusive

###----------------------------------------------------------------------------
OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

###----------------------------------------------------------------------------
cd ../../../tools/misc
python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                            --start-timestamps $START_TIMESTAMPS \
                            --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                            --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                            --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
