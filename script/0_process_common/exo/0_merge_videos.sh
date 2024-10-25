# DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/11_tennis/cam01

DATA_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras
MOVE_DATA_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo


# ##----------------------------------------------------------------
# BIG_SEQUENCE='24_tennis'

# # CAMERA='cam01'
# # CAMERA='cam02'
# # CAMERA='cam03'
# # CAMERA='cam04'
# # CAMERA='cam05'
# # CAMERA='cam06'
# # CAMERA='cam07'
# # CAMERA='cam08'
# # CAMERA='cam09'
# # CAMERA='cam10'
# # CAMERA='cam11'
# # CAMERA='cam12'
# # CAMERA='cam13'
# # CAMERA='cam14'
# # CAMERA='cam15'
# # CAMERA='cam16'
# # CAMERA='cam17'
# # CAMERA='cam18'
# CAMERA='cam19'
# # CAMERA='cam20'

##----------------------------------------------------------------
BIG_SEQUENCE='26_tennis'

# CAMERA='cam01'
# CAMERA='cam02'
# CAMERA='cam03'
# CAMERA='cam04'
# CAMERA='cam05'
# CAMERA='cam06'
# CAMERA='cam07'
# CAMERA='cam08'
# CAMERA='cam09'
# CAMERA='cam10'
# CAMERA='cam11'
# CAMERA='cam12'
# CAMERA='cam13'
# CAMERA='cam14'
# CAMERA='cam15'
# CAMERA='cam16'
# CAMERA='cam17'
# CAMERA='cam18'
# CAMERA='cam19'
CAMERA='cam20'

##----------------------------------------------------------------
DIR=$DATA_DIR/$BIG_SEQUENCE/$CAMERA

##---make merge_list.txt---
echo $DIR
python make_merge_list.py $DIR

cd $DIR
ffmpeg -f concat -safe 0 -i merge_list.txt -c copy rgb.mp4


MOVE_DIR=$MOVE_DATA_DIR/$BIG_SEQUENCE
mkdir -p $MOVE_DIR


## move rgb.mp4 to MOVE_DIR as camera.mp4
mv rgb.mp4 $MOVE_DIR/$CAMERA.mp4