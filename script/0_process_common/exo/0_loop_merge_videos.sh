DATA_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras
MOVE_DATA_DIR=/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo

# BIG_SEQUENCE="23_ballroom3"
BIG_SEQUENCE="19_sword2"
BIG_SEQUENCE="22_ballroom2"

# BIG_SEQUENCE='31_mma'   
# BIG_SEQUENCE='30_karate3'
# BIG_SEQUENCE='29_karate2'
# BIG_SEQUENCE='28_karate' 

# BIG_SEQUENCE='32_mma2' 
# BIG_SEQUENCE='33_mma3' 
# BIG_SEQUENCE='34_mma4' 
# BIG_SEQUENCE='35_mma5'

# BIG_SEQUENCE='16_grappling3'
CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08' 'cam09' 'cam10' 'cam11' 'cam12' 'cam13' 'cam14' 'cam15' 'cam16' 'cam17' 'cam18' 'cam19' 'cam20')

# BIG_SEQUENCE='36_zen1'
# CAMERAS=('cam01' 'cam02' 'cam03' 'cam04')

# BIG_SEQUENCE='37_zen2' ## capture 1
# BIG_SEQUENCE='38_zen3' ## capture 2
# BIG_SEQUENCE='39_zen4' ## capture 3

# BIG_SEQUENCE='40_zen5' ## capture 4
# BIG_SEQUENCE='41_zen6' ## capture 5
# BIG_SEQUENCE='42_zen7' ## capture 6
# BIG_SEQUENCE='43_zen8' ## capture 7
# BIG_SEQUENCE='44_zen9' ## capture 8
# BIG_SEQUENCE='45_zen10' ## capture 9

# CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')


process_camera() {
    local CAMERA="$1"
    local DIR="$DATA_DIR/$BIG_SEQUENCE/$CAMERA"
    echo "Processing $DIR"
    
    ## if .MP4 files are just one, then make a copy of it as rgb.mp4
    if [ $(ls "$DIR"/*.MP4 2>/dev/null | wc -l) -eq 1 ]; then
        cp "$DIR"/*.MP4 "$DIR"/rgb.mp4  
        echo "Single file copied: $DIR/rgb.mp4"
    else
        ## if .MP4 files are more than one, then merge them into one file as rgb.mp4
        ##---make merge_list.txt---
        echo "$DIR"
        python make_merge_list.py "$DIR"
        
        cd "$DIR" || exit
        ffmpeg -f concat -safe 0 -i merge_list.txt -c copy rgb.mp4
    fi

    local MOVE_DIR="$MOVE_DATA_DIR/$BIG_SEQUENCE"
    mkdir -p "$MOVE_DIR"

    ## move rgb.mp4 to MOVE_DIR as camera.mp4
    mv "$DIR"/rgb.mp4 "$MOVE_DIR/$CAMERA.mp4"
}

export -f process_camera
export DATA_DIR MOVE_DATA_DIR BIG_SEQUENCE

# Parallel processing
for CAMERA in "${CAMERAS[@]}"; do
    process_camera "$CAMERA" &
done

wait

echo "All processing is complete."
