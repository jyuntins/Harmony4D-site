cd ../..

# ###----------------------------------------------------------------
READ_DIR=$1
OUTPUT_DIR=$2
NUM_CAMS=$3

###----------------------------------------------------------------
RUN_FILE='tools/misc/make_collage_exo.py'
python $RUN_FILE \
        --read_dir ${READ_DIR} \
        --output_dir $OUTPUT_DIR \
        --num_cams $NUM_CAMS \

