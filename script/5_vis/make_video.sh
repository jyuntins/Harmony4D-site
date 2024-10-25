#!/bin/bash

# Define the function to make high-quality videos
make_video_high() {
    /usr/bin/ffmpeg -r "$2" -f image2 -i "$3" -c:v libx264 -preset veryslow -crf 0 -pix_fmt yuv420p "$1".mp4
}

# # Define the base directory
# # BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/001_tennis/processed_data/vis_smpl_cam_blender"
# # BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/002_tennis/processed_data/vis_smpl_cam_blender"
# # BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/003_tennis/processed_data/vis_smpl_cam_blender"
# BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/004_tennis/processed_data/vis_smpl_cam_blender"

# # Create the videos folder if it doesn't exist
# OUTPUT_DIR="${BASE_DIR}/../videos"
# mkdir -p $OUTPUT_DIR

# # Loop through each camera directory and generate the videos
# for dir in $BASE_DIR/cam*/rgb; do
#     cam_name=$(basename $(dirname $dir))

#     # Use the function to create videos with high quality and save them to the videos folder
#     cd "$dir"
    
#     # Regular video from the default images
#     make_video_high "$OUTPUT_DIR/${cam_name}" 20 "./%05d.jpg"
    
#     # Mask video from the _white.jpg images
#     make_video_high "$OUTPUT_DIR/${cam_name}_mask" 20 "./%05d_white.jpg"
# done

# ##---------------------------------------------------------------------------------------------------------
# Define the base directory
# BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/001_tennis/exo"
BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/002_tennis/exo"
# BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/003_tennis/exo"
# BASE_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/main/24_tennis/004_tennis/exo"

# Create the videos folder if it doesn't exist
OUTPUT_DIR="${BASE_DIR}/../processed_data/videos"
mkdir -p $OUTPUT_DIR

# Loop through each camera directory and generate the videos
for dir in $BASE_DIR/cam*/undistorted_images; do
    cam_name=$(basename $(dirname $dir))

    # Use the function to create videos with high quality and save them to the videos folder
    cd "$dir"
    
    # Regular video from the default images
    make_video_high "$OUTPUT_DIR/${cam_name}_rgb" 20 "./%05d.jpg" &
    
done
