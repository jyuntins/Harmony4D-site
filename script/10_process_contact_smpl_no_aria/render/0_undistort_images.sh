cd ../../..

###----------------------------------------------------------------
RUN_FILE='tools/process_contact_smpl_no_aria/undistort_images.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='001_karate'; DEVICES=3,; MODE='exo'

# # # ###---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='001_karate3'; DEVICES=3,; MODE='exo'

# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='001_mma'; DEVICES=3,; MODE='exo'


# # ###---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='001_mma2'; DEVICES=3,; MODE='exo'


# # ###---------------------------------------------------------------------
BIG_SEQUENCE='33_mma3'
SEQUENCE='001_mma3'; DEVICES=3,; MODE='exo'



# ###------------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

# ###----------------------------------------------------------------
mkdir -p ${OUTPUT_DIR}; 

## if MODE variable is not set, then set it to 'all'
if [ -z ${MODE+x} ]; then MODE='all'; fi

# # # # # # # # ##-----------------------------------------------
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --mode $MODE \
