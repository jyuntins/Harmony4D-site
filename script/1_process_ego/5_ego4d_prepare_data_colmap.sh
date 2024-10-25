###---------------please hand pick images from the aria data-----------------------------------

###--------------------------copy exo gopro images---------------------------------------------
EXO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
EGO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
TARGET_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball' 
# SEQUENCE='calibration_volleyball'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='07_fencing2' ## assemble
# SEQUENCE='calibration_fencing2'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='08_badminton' ## assemble
# SEQUENCE='calibration_badminton'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='11_tennis' #
# SEQUENCE='calibration_tennis'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='uncego4d' 
# SEQUENCE='calibration_uncego4d'


# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='erwinwalk' 
# SEQUENCE='calibration_erwinwalk'


# ###---------------------------------------------------------------------
# BIG_SEQUENCE='erwinwalk2' 
# SEQUENCE='calibration_erwinwalk2'


# # # ###---------------------------------------------------------------------
BIG_SEQUENCE='13_hugging' 
SEQUENCE='calibration_hugging'

###---------------------------------------------------------------------
# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')


# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04')
# EGO_CAMERAS=('aria01')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04' 'aria05' 'aria06')

# EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# EGO_CAMERAS=('aria01' 'aria02' 'aria03')

EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20' 'cam21' 'cam22')
EGO_CAMERAS=('aria01' 'aria02')

###--------------------------------------------------------------------------------------
WORK_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/workplace
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
	   # n=$((n%500)) ## copy every Kth image, 
	   n=$((n%300)) ## copy every Kth image, 
	   # n=$((n%150)) ## copy every Kth image, 
	   # n=$((n%100)) ## copy every Kth image, 

	done
	###--------------------------------------------------------

done


###--------------------------make colmap_rotated_rgb---------------------------------
for CAMERA in "${EGO_CAMERAS[@]}"
do
	SOURCE_IMAGES_DIR=$EGO_SOURCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/ego/$CAMERA/images/colmap_rgb
	TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$CAMERA

	mkdir -p $TARGET_IMAGES_DIR

	# ###--------------------------------------------------------
	# ## we assume the aria images are already rotated to match human understanding
	# cp $SOURCE_IMAGES_DIR/*.jpg $TARGET_IMAGES_DIR

	# for szFile in $TARGET_IMAGES_DIR/*.jpg
	# do 
	#     convert "$szFile" -rotate -90 $TARGET_IMAGES_DIR/"$(basename "$szFile")" ; 
	# done

	n=0
	for file in $SOURCE_IMAGES_DIR/*.jpg; 
	do
	   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
	   n=$((n+1))
	   n=$((n%10)) ## copy every Kth image, 

	done


done


