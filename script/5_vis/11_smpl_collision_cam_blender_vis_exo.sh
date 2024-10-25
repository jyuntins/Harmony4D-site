cd ../..

## note make sure you have undistored image before running this script, refer 00_undistort_images.sh
### EDIT -> Preferences -> Cycles Render
### also check render -> GPU compute is on

###----------------------------------------------------------------
RUN_FILE='tools/vis/smpl_collision_cam_blender_exo.py'
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
# BIG_SEQUENCE='14_grappling'
# SEQUENCE='001_grappling'; 
# DEVICES=0,; 
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # ###-----------------------------------------------------------
#BIG_SEQUENCE='15_grappling2'
#SEQUENCE='001_grappling2'; 
#DEVICES=2,;

#RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # # ###-----------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; 
# DEVICES=1,;
# RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # # # # ###-----------------------------------------------------------
BIG_SEQUENCE='16_grappling3'
SEQUENCE='028_grappling3';
DEVICES=2,;
RENDER_ARIA=false; NUM_EXO_CAMERAS=9

####-------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

NUM_JOBS=4  ## dont increase it too much, blender is slow

##----------------------------------------------------------------
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl_cam_blender")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 


# # # ###------------------------------------------------------
# SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)

# PER_JOB=$((SEQUENCE_LENGTH/NUM_JOBS))
# LAST_JOB_ITER=$((NUM_JOBS-1))

# ## if variable RENDER_ARIA is not define, set it to true
# if [ -z ${RENDER_ARIA+x} ]; then RENDER_ARIA=true; fi


# for (( i=0; i < $NUM_JOBS; ++i ))
# do
#     START_TIME=$((i*PER_JOB + 1))
#     END_TIME=$((i*PER_JOB + PER_JOB))

#     if [ $i == $LAST_JOB_ITER ]
#     then
#         END_TIME=-1
#     fi

#     echo "START_TIME: $START_TIME, END_TIME: $END_TIME"

#     if $RENDER_ARIA; then
#         CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME \
#                         --render_aria \
#                         --num_exo_cameras $NUM_EXO_CAMERAS &
                        

#     else
#         CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME \
#                         --num_exo_cameras $NUM_EXO_CAMERAS &
#     fi


# done



# # # ##----------debug-----------
START_TIME=148
END_TIME=148

CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                        --sequence_path ${SEQUENCE_PATH} \
                        --output_path $OUTPUT_DIR \
                        --start_time $START_TIME \
                        --end_time $END_TIME \
                        --num_exo_cameras $NUM_EXO_CAMERAS 
