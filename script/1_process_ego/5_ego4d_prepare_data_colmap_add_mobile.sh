###---------------please hand pick images from the aria data-----------------------------------

###--------------------------copy exo gopro images---------------------------------------------
EXO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
EGO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
TARGET_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='uncego4d' 
# SEQUENCE='calibration_uncego4d'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='erwinwalk' 
# SEQUENCE='calibration_erwinwalk'

BIG_SEQUENCE='erwinwalk2' 
SEQUENCE='calibration_erwinwalk2'

# ###---------------if mobile capture-------------------------
MOBILE_CAMERA='mobile'
SOURCE_IMAGES_DIR=$EXO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/exo/$MOBILE_CAMERA
TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$MOBILE_CAMERA

mkdir -p $TARGET_IMAGES_DIR
n=0
for file in $SOURCE_IMAGES_DIR/*.jpg; 
do
   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
   n=$((n+1))
   # n=$((n%30)) ## copy every Kth image, 
   n=$((n%5)) ## copy every Kth image, 

done
# ###--------------------------------------------------------
