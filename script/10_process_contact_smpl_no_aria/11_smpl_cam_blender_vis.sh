cd ../..

## note make sure you have undistored image before running this script, refer 00_undistort_images.sh
### EDIT -> Preferences -> Cycles Render
### also check render -> GPU compute is on

###----------------------------------------------------------------
RUN_FILE='tools/process_contact_smpl_no_aria/smpl_cam_blender.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


RENDER_ARIA=false; NUM_EXO_CAMERAS=9

# # ###-----------------------------------------------------------
BIG_SEQUENCE='33_mma3'
SEQUENCE='001_mma3'; DEVICES=3,

####---------------------------make sure you undistorted images----------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"

# NUM_JOBS=4
NUM_JOBS=6

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

##----------------------------------------------------------------
# START_TIME=1; END_TIME=-1; DEVICES=0,

# CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                         --sequence_path ${SEQUENCE_PATH} \
#                         --output_path $OUTPUT_DIR \
#                         --start_time $START_TIME \
#                         --end_time $END_TIME \
#                         --num_exo_cameras $NUM_EXO_CAMERAS 