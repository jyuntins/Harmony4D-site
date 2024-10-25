cd ../..

###------------note this has to be run inside the mmhuman docker---------------
###--------------------------------------------------------------------------
RUN_FILE='tools/vis/overlay_render.py'
SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'


# # # # ###----------------------------------------------------------------
# BIG_SEQUENCE='01_tagging'
# SEQUENCE='007_tagging'; DEVICES=1,

# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='02_legoassemble'
# SEQUENCE='004_legoassemble'; DEVICES=1,

# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='04_basketball'
# SEQUENCE='001_basketball'; DEVICES=1,

# # # ###----------------------------------------------------------------
# BIG_SEQUENCE='06_volleyball'
# SEQUENCE='001_volleyball'; DEVICES=1,

# # # # ###----------------------------------------------------------------
BIG_SEQUENCE='07_fencing2'
SEQUENCE='001_fencing2'; DEVICES=1,


# ###----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE
LOG_DIR="$(echo "${OUTPUT_DIR}/logs/vis_smpl")"
mkdir -p ${OUTPUT_DIR}; mkdir -p ${LOG_DIR}; 

# ##--------------run-----------------------------
CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                --sequence_path ${SEQUENCE_PATH} \
                --output_path $OUTPUT_DIR \
