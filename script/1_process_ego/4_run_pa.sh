cd ../..


# # # ###---------------------------------------------------
# BIG_SEQUENCE='24_tennis'
# SEQUENCE='calibration_tennis'


# # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging' 
# SEQUENCE='calibration_hugging'

# ###---------------------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# SEQUENCE='calibration_grappling'

# # ###---------------------------------------------------------------------
BIG_SEQUENCE='15_grappling2'
SEQUENCE='calibration_grappling2'

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='calibration_ballroom'

# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='calibration_sword3'

#BIG_SEQUENCE="23_ballroom3"
#SEQUENCE="calibration_ballroom3"
# # # # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3' #
# SEQUENCE='calibration_karate3'

# BIG_SEQUENCE='31_mma' #
# SEQUENCE='calibration_mma'

# BIG_SEQUENCE='32_mma2' #
# SEQUENCE='calibration_mma2'

#BIG_SEQUENCE='33_mma3' #
#SEQUENCE='calibration_mma3'

#BIG_SEQUENCE="18_sword"
#SEQUENCE="calibration_sword"

COLMAP_ROOT_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/colmap
ARIA_WORKPLACE_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/ego

###------------------------------------------------------------------
COLMAP_WORKPLACE_DIR=$COLMAP_ROOT_DIR/"workplace"
RUN_FILE='tools/calibration/run_procrustes_alignment.py'

###------------------------------------------------------------------
python $RUN_FILE --colmap-workplace-dir ${COLMAP_WORKPLACE_DIR} --aria-workplace-dir $ARIA_WORKPLACE_DIR
