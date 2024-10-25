###---------------please hand pick images from the aria data-----------------------------------


###--------------------------copy exo gopro images---------------------------------------------
EXO_SOURCE_ROOT_DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/main'
EGO_SOURCE_ROOT_DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/main'
TARGET_ROOT_DIR='/home/rawalk/Desktop/datasets/ego_exo/current_dev/basketball/main'

# SEQUENCE='001_tagging'
# SEQUENCE='002_tagging_leg'
# SEQUENCE='003_tagging_game'
# SEQUENCE='004_tagging_walk'
# SEQUENCE='005_tagging_circle'
SEQUENCE='006_dodgeball_1'
# SEQUENCE='007_dodgeball_2'
# SEQUENCE='008_basketball_1'
# SEQUENCE='009_basketball_2'
# SEQUENCE='010_basketball_3'
# SEQUENCE='011_passing'

EXO_CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
EGO_CAMERAS=('aria01' 'aria02' 'aria03' 'aria04')

###----------------------------copy exo cameras--------------------------------------------
for CAMERA in "${EXO_CAMERAS[@]}"
do

	###--------------------------------------------------------
	SOURCE_IMAGES_DIR=$EXO_SOURCE_ROOT_DIR/$SEQUENCE/exo/$CAMERA/images
	TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$SEQUENCE/metashape/images/$CAMERA

	mkdir -p $TARGET_IMAGES_DIR
	n=0
	for file in $SOURCE_IMAGES_DIR/*.jpg; 
	do
	   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
	   n=$((n+1))
	   n=$((n%300)) ## copy every Kth image
	done
	###--------------------------------------------------------

done


###--------------------------make colmap_rotated_rgb---------------------------------
for CAMERA in "${EGO_CAMERAS[@]}"
do
	SOURCE_IMAGES_DIR=$EGO_SOURCE_ROOT_DIR/$SEQUENCE/ego/$CAMERA/images/colmap_rgb
	TARGET_IMAGES_DIR=$EGO_SOURCE_ROOT_DIR/$SEQUENCE/ego/$CAMERA/images/colmap_rotated_rgb

	mkdir -p $TARGET_IMAGES_DIR

	###--------------------------------------------------------
	## we assume the aria images are already rotated to match human understanding
	cp $SOURCE_IMAGES_DIR/*.jpg $TARGET_IMAGES_DIR

	for szFile in $TARGET_IMAGES_DIR/*.jpg
	do 
	    convert "$szFile" -rotate -90 $TARGET_IMAGES_DIR/"$(basename "$szFile")" ; 
	done


done



###--------------------------copy ego aria images to colmap folder---------------------------------------------
for CAMERA in "${EGO_CAMERAS[@]}"
do

	###--------------------------------------------------------
	SOURCE_IMAGES_DIR=$EGO_SOURCE_ROOT_DIR/$SEQUENCE/ego/$CAMERA/images/colmap_rotated_rgb
	TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$SEQUENCE/metashape/images/$CAMERA

	mkdir -p $TARGET_IMAGES_DIR

	###--------------------------------------------------------
	## we assume the aria images are already rotated to match human understanding
	cp $SOURCE_IMAGES_DIR/*.jpg $TARGET_IMAGES_DIR

done


##---------------merage all folders into one-----
cd "$TARGET_ROOT_DIR/$SEQUENCE/metashape"

find 'images' -type f -print0 | 
    while IFS= read -r -d '' f; do 
        dd=$(dirname "$f")
        new="${f/main\/}"
        new="${new//\//_}"
        new=${new:7}
        mv "$f" "$dd"/"$new"
    done

mv './images' './temp_images'
mkdir -p 'images'
mv temp_images/**/* images/
rm -rf temp_images