###----------------------------------------------------------------------------
BIG_SEQUENCE='33_mma3'

DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo/${BIG_SEQUENCE}/exo"
OUTPUT_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/${BIG_SEQUENCE}"

# ###-------------for calibration---------------
# ## second throw of the ball
# CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="01575--01087--00937--01230--01515--01186--01433--01487--01457--01007--01092--00971--00700--00795--00833--00653--01047--01266--01243--01542"

# SEQUENCE='calibration_karate'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='01000' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='01400' ## this is also inclusive


###-------------for calibration---------------
## second throw of the ball
CAMERAS="cam01--cam02--cam03--cam04--cam05--cam06--cam07--cam08--cam09--cam10--cam11--cam12--cam13--cam14--cam15--cam16--cam17--cam18--cam19--cam20"
# START_TIMESTAMPS="01575--01087--00937--01230--01515--01186--01433--01487--01457--01007--01092--00971--00700--00795--00833--00653--01047--01266--01243--01542"
START_TIMESTAMPS="01612--01525--01489--01386--01459--01639--00937--01052--01171--01599--00324--00597--00808--00652--00850--01283--01235--00726--01363--01526"

cd ../../../tools/misc

# SEQUENCES=("002_mma3" "003_mma3" "004_mma3" "005_mma3" "006_mma3" "007_mma3" "008_mma3")
# SEQUENCE_START_TIMESTAMPS=("02250" "02760" "03670" "04670" "05716" "06650" "07580")
# SEQUENCE_END_TIMESTAMPS=("02770" "03680" "04680" "05725" "06185" "07590" "07940")
SEQUENCES=('metric_mma3')
SEQUENCE_START_TIMESTAMPS=("01390")
SEQUENCE_END_TIMESTAMPS=("01445")
for (( i=0; i<=0; i++ ))
do
    SEQUENCE_CAMERA_NAME="cam01"
    SEQUENCE=${SEQUENCES[i]}
    SEQUENCE_START_TIMESTAMP=${SEQUENCE_START_TIMESTAMPS[i]} ## this includes the image name
    SEQUENCE_END_TIMESTAMP=${SEQUENCE_END_TIMESTAMPS[i]} ## this is also inclusive
    OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'
    python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
                                --start-timestamps $START_TIMESTAMPS \
                                --sequence-camera-name $SEQUENCE_CAMERA_NAME \
                                --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
                                --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \

    # echo $SEQUENCE
    # echo $SEQUENCE_START_TIMESTAMP
    # echo $SEQUENCE_END_TIMESTAMP
    # echo "pass"
done


# SEQUENCE='002_mma3'
# SEQUENCE_CAMERA_NAME='cam01'
# SEQUENCE_START_TIMESTAMP='07580' ## this includes the image name
# SEQUENCE_END_TIMESTAMP='07940' ## this is also inclusive
#001_mma3 1800 - 2210
#002_mma3 2250 - 2770  V
# 003_mma3 2760 - 3680
# 004_mma3 3670 - 4680 V 
# 005_mma3 4670 - 5725
# 006_mma3 5716 - 6185 
# 007_mma3 6650 - 7590 V
# 008_mma3 7580 - 7940

#metric 1645
###----------------------------------------------------------------------------
# OUTPUT_IMAGE_DIR=$OUTPUT_DIR/$SEQUENCE/'exo'

# ###----------------------------------------------------------------------------
# cd ../../../tools/misc
# python exo_time_sync_restructure.py --sequence $SEQUENCE --cameras $CAMERAS \
#                             --start-timestamps $START_TIMESTAMPS \
#                             --sequence-camera-name $SEQUENCE_CAMERA_NAME \
#                             --sequence-start-timestamp $SEQUENCE_START_TIMESTAMP --sequence-end-timestamp $SEQUENCE_END_TIMESTAMP \
#                             --data-dir $DATA_DIR --output-dir $OUTPUT_IMAGE_DIR \
