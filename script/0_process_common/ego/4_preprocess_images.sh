###----------------------------------------------------------------------------
# BIG_SEQUENCE='07_fencing2'
# BIG_SEQUENCE='08_badminton'
# BIG_SEQUENCE='11_tennis'
BIG_SEQUENCE='13_frisbee'


DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras/${BIG_SEQUENCE}"

# RECORDING=aria01
# RECORDING=aria02
RECORDING=aria03
# RECORDING=aria04
# RECORDING=aria05
# RECORDING=aria06

###----------------------------------------------------------------------------
IMAGE_DIR=$DATA_DIR/$RECORDING/'images'
RGB_IMAGE_DIR=$IMAGE_DIR/'rotated_rgb'
LEFT_IMAGE_DIR=$IMAGE_DIR/'rotated_left'
RIGHT_IMAGE_DIR=$IMAGE_DIR/'rotated_right'

mkdir -p $RGB_IMAGE_DIR $LEFT_IMAGE_DIR $RIGHT_IMAGE_DIR

# ###----------------------------------------------------------------------------
CURRENT_DIR=$PWD

cd $IMAGE_DIR
for IMAGE_NAME in *;
do
    CAMERA_STRING=${IMAGE_NAME:(-5)}
    echo $IMAGE_DIR/$IMAGE_NAME

    if [[ "${CAMERA_STRING}" == "0.jpg" ]] ;
    then
        SAVE_IMAGE_NAME=${IMAGE_NAME//"_0_0.jpg"/".jpg"}
        mv $IMAGE_NAME $RGB_IMAGE_DIR/$SAVE_IMAGE_NAME

    elif [[ "${CAMERA_STRING}" == "1.jpg" ]] ;
    then
        SAVE_IMAGE_NAME=${IMAGE_NAME//"_0_1.jpg"/".jpg"}
        mv $IMAGE_NAME $LEFT_IMAGE_DIR//$SAVE_IMAGE_NAME

    elif [[ "${CAMERA_STRING}" == "2.jpg" ]] ;
    then
        SAVE_IMAGE_NAME=${IMAGE_NAME//"_0_2.jpg"/".jpg"}
        mv $IMAGE_NAME $RIGHT_IMAGE_DIR//$SAVE_IMAGE_NAME
    fi
done

# ###----------------------------------------------------------------------------
RGB_ROTATED_IMAGE_DIR=$IMAGE_DIR/'rgb'
LEFT_ROTATED_IMAGE_DIR=$IMAGE_DIR/'left'
RIGHT_ROTATED_IMAGE_DIR=$IMAGE_DIR/'right'

echo "copying " $RGB_IMAGE_DIR
cp -r $RGB_IMAGE_DIR $RGB_ROTATED_IMAGE_DIR

echo "copying " $LEFT_IMAGE_DIR
cp -r $LEFT_IMAGE_DIR $LEFT_ROTATED_IMAGE_DIR

echo "copying " $RIGHT_IMAGE_DIR
cp -r $RIGHT_IMAGE_DIR $RIGHT_ROTATED_IMAGE_DIR

###---------------------------------------------------------------------------
cd $CURRENT_DIR

echo "rotating " $RGB_ROTATED_IMAGE_DIR
./rotate_images.sh $RGB_ROTATED_IMAGE_DIR &

echo "rotating " $LEFT_ROTATED_IMAGE_DIR 
./rotate_images.sh $LEFT_ROTATED_IMAGE_DIR & 

echo "rotating " $RIGHT_ROTATED_IMAGE_DIR
./rotate_images.sh $RIGHT_ROTATED_IMAGE_DIR &

echo "Rotation minions are live! They will work hard in the background. Be patient and do not kill them!"
# ###---------------------------------------------------------------------------
