cd ../..

###------------------------------------------------------------------
SEQUENCE='001_tagging_1'


# SEQUENCE='002_tagging_leg'
# SEQUENCE='003_tagging_game'
# SEQUENCE='004_tagging_walk'
# SEQUENCE='005_tagging_circle'
# SEQUENCE='006_dodgeball_1'
# SEQUENCE='007_dodgeball_2'
# SEQUENCE='008_basketball_1'
# SEQUENCE='009_basketball_2'
# SEQUENCE='010_basketball_3'
# SEQUENCE='011_passing'

COLMAP_ROOT_DIR=/home/rawalk/Desktop/datasets/ego_exo/main/$SEQUENCE/colmap
ARIA_WORKPLACE_DIR=/home/rawalk/Desktop/datasets/ego_exo/main/$SEQUENCE/ego

###------------------------------------------------------------------
COLMAP_WORKPLACE_DIR=$COLMAP_ROOT_DIR/"workplace"
RUN_FILE='tools/icp/run_icp.py'
# RUN_FILE='tools/icp/vis_camera_centers.py'

###------------------------------------------------------------------
python $RUN_FILE --colmap-workplace-dir ${COLMAP_WORKPLACE_DIR} --aria-workplace-dir $ARIA_WORKPLACE_DIR