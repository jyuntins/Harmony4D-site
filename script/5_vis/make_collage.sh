# BIG_SEQUENCE='01_tagging'

# SEQUENCE='001_tagging'; NUM_ARIAS=4; NUM_CAMS=8;
# # SEQUENCE='007_tagging'; NUM_ARIAS=4; NUM_CAMS=8;
# # SEQUENCE='008_tagging'; NUM_ARIAS=4; NUM_CAMS=8;
# # SEQUENCE='009_tagging'; NUM_ARIAS=4; NUM_CAMS=8;
# # SEQUENCE='010_tagging'; NUM_ARIAS=4; NUM_CAMS=8;
# # SEQUENCE='011_tagging'; NUM_ARIAS=4; NUM_CAMS=8;


# # # # # # ###----------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball'
# # # SEQUENCE='001_volleyball'; NUM_ARIAS=4; NUM_CAMS=15;
# # SEQUENCE='001_volleyball'; NUM_ARIAS=4; NUM_CAMS=9;
# SEQUENCE='002_volleyball'; NUM_ARIAS=4; NUM_CAMS=15;

# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='07_fencing2'
# SEQUENCE='003_fencing2'; NUM_ARIAS=3; NUM_CAMS=15;

# # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='08_badminton'
# SEQUENCE='001_badminton'; NUM_ARIAS=4; NUM_CAMS=15;

# # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='24_tennis'
# SEQUENCE='001_tennis'; NUM_ARIAS=2; NUM_CAMS=20;

# # # # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# # SEQUENCE='001_hugging'; NUM_ARIAS=2; NUM_CAMS=22;
# SEQUENCE='001_hugging'; NUM_ARIAS=2; NUM_CAMS=9

# # ###------------------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# # SEQUENCE='001_grappling'; NUM_ARIAS=4; NUM_CAMS=20
# SEQUENCE='001_grappling'; NUM_ARIAS=4; NUM_CAMS=9

# # # ###------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# # SEQUENCE='001_grappling2'; NUM_ARIAS=4; NUM_CAMS=20
# SEQUENCE='001_grappling2'; NUM_ARIAS=4; NUM_CAMS=9

# # # # # # ###------------------------------------------------------------------
BIG_SEQUENCE='21_ballroom'
# # # SEQUENCE='001_ballroom'; NUM_ARIAS=4; NUM_CAMS=20
SEQUENCE='002_ballroom'; NUM_ARIAS=4; NUM_CAMS=9

# # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# # SEQUENCE='001_sword3'; NUM_ARIAS=4; NUM_CAMS=20
# SEQUENCE='001_sword3'; NUM_ARIAS=4; NUM_CAMS=9


# # # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='001_karate'; NUM_ARIAS=2; NUM_CAMS=20

# # # # # ###------------------------------------------------------------------
#BIG_SEQUENCE='30_karate3'
# SEQUENCE='001_karate3'; NUM_ARIAS=2; NUM_CAMS=20
#SEQUENCE='001_karate3'; NUM_ARIAS=2; NUM_CAMS=9


# # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='001_mma'; NUM_ARIAS=2; NUM_CAMS=20
# SEQUENCE='001_mma'; NUM_ARIAS=2; NUM_CAMS=9

# # # # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# # # SEQUENCE='001_mma2'; NUM_ARIAS=2; NUM_CAMS=20
# SEQUENCE='001_mma2'; NUM_ARIAS=2; NUM_CAMS=9

# # # # # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3'
# # SEQUENCE='001_mma3'; NUM_ARIAS=2; NUM_CAMS=20
# SEQUENCE='001_mma3'; NUM_ARIAS=2; NUM_CAMS=9


##-------------------------------------------
# MODE='time_sync'
# MODE='vis_aria_locations'
# MODE='vis_bboxes'
# MODE='vis_poses2d'
# MODE='vis_segposes2d'
# MODE='vis_poses3d'
# MODE='vis_contact_poses3d'
# MODE='vis_refine_poses3d'
# MODE='vis_fit_poses3d'
# MODE='vis_smpl'
# MODE='vis_smpl_cam_blender'
MODE='vis_smpl_collision_cam_blender'

# MODE='vis_kf_poses3d'
# MODE='vis_segmentation'
# MODE='vis_segposes2d'

##-------------------------------------------

if [ $MODE == 'time_sync' ]
then
	READ_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/"

else
	READ_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data/$MODE/"
fi

OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data/vis_collage/$MODE/"

# # # # ###----------------------------------------------------------------
./make_collage_aria.sh ${READ_DIR} ${OUTPUT_DIR} ${NUM_ARIAS} &


# # ###----------------------------------------------------------------
./make_collage_exo.sh ${READ_DIR} ${OUTPUT_DIR} ${NUM_CAMS} 


