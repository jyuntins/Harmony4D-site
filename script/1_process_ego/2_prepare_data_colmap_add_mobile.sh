###---------------please hand pick images from the aria data-----------------------------------

###--------------------------copy exo gopro images---------------------------------------------
EXO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
EGO_SOURCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
TARGET_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# BIG_SEQUENCE='07_fencing2' ## assemble
# SEQUENCE='calibration_fencing2'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='08_badminton' ## assemble
# SEQUENCE='calibration_badminton'

# ##---------------------------------------------------------------------
# BIG_SEQUENCE='11_tennis' #
# SEQUENCE='calibration_tennis'

###---------------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball' #
# SEQUENCE='calibration_volleyball'

###---------------------------------------------------------------------
# BIG_SEQUENCE='kentawalk' 
# SEQUENCE='001_kentawalk'

###---------------------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# SEQUENCE='calibration_grappling'

###---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='calibration_grappling2'

###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='calibration_ballroom'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='calibration_sword3'

# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='24_tennis' #
# SEQUENCE='calibration_tennis'

# ##---------------------------------------------------------------------
BIG_SEQUENCE='37_zen2' #
SEQUENCE='calibration_zen2'


# ###---------------if mobile capture-------------------------
MOBILE_CAMERA='mobile'
SOURCE_IMAGES_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
TARGET_IMAGES_DIR=$TARGET_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/colmap/images/$MOBILE_CAMERA

mkdir -p $TARGET_IMAGES_DIR
n=0
for file in $SOURCE_IMAGES_DIR/*.jpg; 
do
   test $n -eq 0 && cp "$file" $TARGET_IMAGES_DIR
   n=$((n+1))
   n=$((n%10)) ## default 
   # n=$((n%5)) ## slower but better

done
# ###--------------------------------------------------------
