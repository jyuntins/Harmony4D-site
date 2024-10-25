cd ../..

# ###----------------------------------------------------------------
READ_DIR=$1
OUTPUT_DIR=$2
NUM_ARIAS=$3

# ###----------------------------------------------------------------
RUN_FILE='tools/misc/make_collage_aria.py'
python $RUN_FILE \
        --read_dir ${READ_DIR} \
        --output_dir $OUTPUT_DIR \
        --num_arias $NUM_ARIAS \


