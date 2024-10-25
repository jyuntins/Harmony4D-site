cd ../..

## note make sure you have undistored image before running this script, refer 00_undistort_images.sh
### EDIT -> Preferences -> Cycles Render
### also check render -> GPU compute is on

###----------------------------------------------------------------
RUN_FILE='tools/vis/smpl_cam_blender_exo.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'

# # # # ####-------------------------------------------------------------
# BIG_SEQUENCE='01_tagging'
# SEQUENCE='001_tagging'; DEVICES=1,

# # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='07_fencing2'
# SEQUENCE='003_fencing2'; DEVICES=0,1,2,3, 

# # # # # ###------------------------------------------------------------------
# BIG_SEQUENCE='02_legoassemble'
# SEQUENCE='004_legoassemble'; DEVICES=0,1,2,3, 

# # # # # # # # # ###---------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball'
# SEQUENCE='001_volleyball'; DEVICES=0,1,2,3,

# # # # # # ###-------------------------------------------------------------
# BIG_SEQUENCE='08_badminton'
# SEQUENCE='001_badminton'; DEVICES=0,1,2,3, 

###-----------------------------------------------------------
# BIG_SEQUENCE='04_basketball'
# SEQUENCE='001_basketball'; DEVICES=0,1,2,3,

# # ###-----------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='001_hugging'; 
# DEVICES=0,; 
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # ###-----------------------------------------------------------
#BIG_SEQUENCE='24_tennis'
# SEQUENCE='001_tennis'; DEVICES=0,; 
#SEQUENCE='002_tennis'; DEVICES=1,; 
# SEQUENCE='003_tennis'; DEVICES=2,; 
# SEQUENCE='004_tennis'; DEVICES=3,; 

#RENDER_ARIA=false; NUM_EXO_CAMERAS=9


# # ###-----------------------------------------------------------
# BIG_SEQUENCE='14_grappling'
# SEQUENCE='001_grappling'; 
# DEVICES=0,; 
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # ###-----------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; 
# DEVICES=1,;
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # ###-----------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='028_grappling3'; 
# DEVICES=3,;
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # # ###-----------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; 
# DEVICES=1,;
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # # # ###-----------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='011_karate3';
# DEVICES=3,;
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # ###------------------------------------------------------------------
# # # ## aria01, blue is the coach. aria02 is the girl
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='002_karate2'; DEVICES=3,
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # ###------------------------------------------------------------------
# # # # ## aria01 is the white. aria02 is black
# BIG_SEQUENCE='31_mma'
# SEQUENCE='001_mma'; DEVICES=0,
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # ###------------------------------------------------------------------
# # ## aria01 is the blue. aria02 is red guy
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='001_mma2'; DEVICES=2,
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # # ###------------------------------------------------------------------
# # # # aria01 is the black. aria02 is shirtless white guy
BIG_SEQUENCE='33_mma3'
SEQUENCE='008_mma3'; DEVICES=3,
RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# BIG_SEQUENCE='34_mma4'
# SEQUENCE='001_mma4'; DEVICES=1,
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

####---------------------------make sure you undistorted images----------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"


NUM_JOBS=4
# NUM_JOBS=6
# NUM_JOBS=8

##----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl_cam_blender")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 


# # # ###------------------------------------------------------
SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)

PER_JOB=$((SEQUENCE_LENGTH/NUM_JOBS))
LAST_JOB_ITER=$((NUM_JOBS-1))


echo "SEQUENCE_LENGTH: $SEQUENCE_LENGTH"

## if variable RENDER_ARIA is not define, set it to true
if [ -z ${RENDER_ARIA+x} ]; then RENDER_ARIA=true; fi


for (( i=0; i < $NUM_JOBS; ++i ))
do
    START_TIME=$((i*PER_JOB + 1))
    END_TIME=$((i*PER_JOB + PER_JOB))

    if [ $i == $LAST_JOB_ITER ]
    then
        END_TIME=-1
    fi

    echo "START_TIME: $START_TIME"
    echo "END_TIME: $END_TIME"

    if $RENDER_ARIA; then
        CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                        --sequence_path ${SEQUENCE_PATH} \
                        --output_path $OUTPUT_DIR \
                        --start_time $START_TIME \
                        --end_time $END_TIME \
                        --render_aria \
                        --num_exo_cameras $NUM_EXO_CAMERAS &
                        

    else
        CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                        --sequence_path ${SEQUENCE_PATH} \
                        --output_path $OUTPUT_DIR \
                        --start_time $START_TIME \
                        --end_time $END_TIME \
                        --num_exo_cameras $NUM_EXO_CAMERAS &
    fi


done

# # ##----------------------------------------------------------------
# START_TIME=1; END_TIME=-1; DEVICES=1,
# START_TIME=148; END_TIME=148; DEVICES=1,

# CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME \
#                         --num_exo_cameras $NUM_EXO_CAMERAS 
