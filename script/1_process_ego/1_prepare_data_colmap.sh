###---------------please hand pick images from the aria data-----------------------------------

###--------------------------copy exo gopro images---------------------------------------------
EXO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
EGO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
TARGET_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging' 
# SEQUENCE='calibration_hugging'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# SEQUENCE='calibration_grappling'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='calibration_grappling2'

# # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='calibration_grappling3'

# # # ###---------------------------------------------------------------------
# BIG_SEQUENCE="18_sword"
# SEQUENCE="calibration_sword"

# # # ###---------------------------------------------------------------------
BIG_SEQUENCE='19_sword2'
SEQUENCE='calibration_sword2'

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='calibration_sword3'

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='calibration_ballroom'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='calibration_ballroom3'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='24_tennis' #
# SEQUENCE='calibration_tennis'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2' #
# SEQUENCE='calibration_karate2'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate' #
# SEQUENCE='calibration_karate'

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3' #
# SEQUENCE='calibration_karate3'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma' #
# SEQUENCE='calibration_mma'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2' #
# SEQUENCE='calibration_mma2'

# # ##---------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3' #
# SEQUENCE='calibration_mma3'

# BIG_SEQUENCE='34_mma4' #
# SEQUENCE='calibration_mma4'

# BIG_SEQUENCE='35_mma5' #
# SEQUENCE='calibration_mma5'

# # ##---------------------------------------------------------------------
# BIG_SEQUENCE='36_zen1' #
# SEQUENCE='calibration_zen1'

# ##---------------------------------------------------------------------
# BIG_SEQUENCE='37_zen2' #
# SEQUENCE='calibration_zen2'

###---------------------------------------------------------------------
# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04' 'aria05' 'aria06')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20' 'cam21' 'cam22')
# EGO_CAMERAS=('aria01')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')

EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20')
# EGO_CAMERAS=('aria01' 'aria02')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20')
# EGO_CAMERAS=('aria01' 'aria02')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04')
EGO_CAMERAS=()

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=()

###--------------------------------------------------------------------------------------
WORK_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/workplace
echo $WORK_DIR
mkdir -p $WORK_DIR

for CAMERA in "${EXO_CAMERAS[@]}"
do

	###--------------------------------------------------------
	SOURCE_IMAGES_DIR=$EXO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/exo/$CAMERA/images
	TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$CAMERA

	mkdir -p $TARGET_IMAGES_DIR
	n=0
	for file in $SOURCE_IMAGES_DIR/*.jpg; 
	do
	   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
	   n=$((n+1))
	#    n=$((n%150)) ## copy every Kth image, 
	#    n=$((n%100)) ## default
	#    n=$((n%200)) 
	   n=$((n%50)) 

	done
	###--------------------------------------------------------

done

###--------------------------copy ego aria images, no aria rotation---------------------------------------------
for CAMERA in "${EGO_CAMERAS[@]}"
do

	###--------------------------------------------------------
	SOURCE_IMAGES_DIR=$EGO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/ego/$CAMERA/images/colmap_rgb

	## if SOURCE_IMAGES_DIR does not exist, then use the original images from images/rgb. 
	if [ ! -d "$SOURCE_IMAGES_DIR" ]; then
		## copy rgb folder as colmap_rgb
		cp -r $EGO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/ego/$CAMERA/images/rgb $EGO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/ego/$CAMERA/images/colmap_rgb
	fi


	TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$CAMERA

	mkdir -p $TARGET_IMAGES_DIR

	###--------------------------------------------------------
	## we assume the aria images are already rotated to match human understanding
	# cp $SOURCE_IMAGES_DIR/*.jpg $TARGET_IMAGES_DIR

	## only copy every Kth image
	n=0
	for file in $SOURCE_IMAGES_DIR/*.jpg;
	do
	   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
	   n=$((n+1))
	#    n=$((n%50)) ## default
	#    n=$((n%20)) ## copy every Kth image,
	   n=$((n%10)) ## copy every Kth image,

	done

done


## copy mobile images straight from the time synced folder

# ###---------------if mobile capture-------------------------
MOBILE_CAMERA='mobile'
SOURCE_IMAGES_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo/mobile"
TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$MOBILE_CAMERA

echo "copying mobile images from: $SOURCE_IMAGES_DIR" to: $TARGET_IMAGES_DIR


mkdir -p $TARGET_IMAGES_DIR
n=0
for file in $SOURCE_IMAGES_DIR/*.jpg; 
do
   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
   n=$((n+1))
#    n=$((n%10)) ## default 
   n=$((n%5)) ## slower but better

done

echo "done!"
# ###--------------------------------------------------------
