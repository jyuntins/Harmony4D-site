cd ../..

###------------------------------------------------------------------
# SEQUENCE='001_tagging'
# SEQUENCE='002_tagging'
# SEQUENCE='003_tagging'
# SEQUENCE='004_tagging'
# SEQUENCE='005_tagging'
# SEQUENCE='006_tagging'
# SEQUENCE='007_tagging'
# SEQUENCE='008_tagging'
# SEQUENCE='009_tagging'
# SEQUENCE='010_tagging'
# SEQUENCE='011_tagging'

# SEQUENCE='012_frisbee'
# SEQUENCE='013_lego'
# SEQUENCE='014_basketball'

SEQUENCE='frisbee_calibration'

COLMAP_ROOT_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$SEQUENCE/colmap
ARIA_WORKPLACE_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$SEQUENCE/ego
EXO_WORKPLACE_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$SEQUENCE/exo

###------------------------------------------------------------------
COLMAP_WORKPLACE_DIR=$COLMAP_ROOT_DIR/"workplace"
RUN_FILE='tools/calibration/generate_exo_calibration.py'

###------------------------------------------------------------------
python $RUN_FILE --colmap-workplace-dir ${COLMAP_WORKPLACE_DIR} \
				--aria-workplace-dir $ARIA_WORKPLACE_DIR \
				--exo-workplace-dir $EXO_WORKPLACE_DIR \
