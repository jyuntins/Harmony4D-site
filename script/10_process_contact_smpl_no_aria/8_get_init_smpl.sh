cd ../..

###------------note this has to be run inside the mmhuman docker---------------
###--------------------------------------------------------------------------
RUN_FILE='tools/process_contact_smpl_no_aria/5_get_init_smpl.py'

SEQUENCE_ROOT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/main'
######---------------------------------------------------------------------
# BIG_SEQUENCE='13_hugging'
# SEQUENCE='001_hugging'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='15_grappling2'
# SEQUENCE='001_grappling2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='16_grappling3'
# SEQUENCE='001_grappling3'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='18_sword'
# SEQUENCE='001_sword'; DEVICES=3,
######---------------------------------------------------------------------
BIG_SEQUENCE='19_sword2'
SEQUENCE='002_sword2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='20_sword3'
# SEQUENCE='001_sword3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='21_ballroom'
# SEQUENCE='001_ballroom'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='22_ballroom2'
# SEQUENCE='001_ballroom2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='23_ballroom3'
# SEQUENCE='001_ballroom3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='28_karate'
# SEQUENCE='010_karate'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='29_karate2'
# SEQUENCE='004_karate2'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='30_karate3'
# SEQUENCE='002_karate3'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='31_mma'
# SEQUENCE='002_mma'; DEVICES=2,
######---------------------------------------------------------------------
# BIG_SEQUENCE='32_mma2'
# SEQUENCE='003_mma2'; DEVICES=1,
######---------------------------------------------------------------------
# BIG_SEQUENCE='33_mma3'
# SEQUENCE='008_mma3'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='34_mma4'
# SEQUENCE='001_mma4'; DEVICES=3,
######---------------------------------------------------------------------
# BIG_SEQUENCE='35_mma5'
# SEQUENCE='004_mma5'; DEVICES=3,


# # ##---------------------------------------------------------------------
CHOOSEN_CAMS='cam01:rgb---cam02:rgb---cam03:rgb---cam04:rgb---cam05:rgb---cam06:rgb---cam07:rgb---cam08:rgb---cam09:rgb---cam10:rgb---cam11:rgb---cam12:rgb---cam13:rgb---cam14:rgb---cam15:rgb---cam16:rgb---cam17:rgb---cam18:rgb---cam19:rgb---cam20:rgb'
# CHOOSEN_CAMS='cam18:rgb'
# ###----------------------------------------------------------------
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/$BIG_SEQUENCE/$SEQUENCE/processed_data"
SEQUENCE_PATH=$SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE

NUM_JOBS=4

# # ###----------------------------------------------------------------
mkdir -p ${OUTPUT_DIR};

# #  ##-----------------------------------------------
SEQUENCE_LENGTH=$(find $SEQUENCE_ROOT_DIR/$BIG_SEQUENCE/$SEQUENCE/'exo'/'cam01'/'images' -maxdepth 1 -name '*.jpg' | wc -l)
PER_JOB=$((SEQUENCE_LENGTH/NUM_JOBS))
LAST_JOB_ITER=$((NUM_JOBS-1))

for (( i=0; i < $NUM_JOBS; ++i ))
do
    START_TIME=$((i*PER_JOB + 1))
    END_TIME=$((i*PER_JOB + PER_JOB))

    if [ $i == $LAST_JOB_ITER ]
    then
        END_TIME=-1
    fi
    

    ##--------------run-----------------------------
    CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
                    --sequence_path ${SEQUENCE_PATH} \
                    --output_path $OUTPUT_DIR \
                    --start_time $START_TIME \
                    --end_time $END_TIME \
                    --choosen_cams $CHOOSEN_CAMS &


done


# # ###--------------------------debug------------------------------
# START_TIME=600
# END_TIME=901

# START_TIME=1
# END_TIME=2


# CUDA_VISIBLE_DEVICES=${DEVICES} python $RUN_FILE \
#                     --sequence_path ${SEQUENCE_PATH} \
#                     --output_path $OUTPUT_DIR \
#                     --start_time $START_TIME \
#                     --end_time $END_TIME \
#                     --choosen_cams $CHOOSEN_CAMS \


