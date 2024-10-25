###---------------------------------------------------------------------------
DATA_DIR="/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo"
OUTPUT_DIR='/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo'

# SUPER_SEQUENCE='erwinwalk'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')
# SUPER_SEQUENCE='36_zen1'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04') ## capture 0
# SUPER_SEQUENCE='37_zen2'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 1

# SUPER_SEQUENCE='38_zen3'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 2
# SUPER_SEQUENCE='39_zen4'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 3
# SUPER_SEQUENCE='40_zen5'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 4
# SUPER_SEQUENCE='41_zen6'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 5
# SUPER_SEQUENCE='42_zen7'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 6
# SUPER_SEQUENCE='43_zen8'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 7
# SUPER_SEQUENCE='44_zen9'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 8, 
SUPER_SEQUENCE='45_zen10'; CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08') ## capture 9, 

###---------------------------------------------------------------------------
SEQUENCE_PATH="$(echo "${DATA_DIR}/${SUPER_SEQUENCE}")"
OUTPUT_SEQUENCE_PATH="$(echo "${OUTPUT_DIR}/${SUPER_SEQUENCE}/exo")"

mkdir -p ${OUTPUT_SEQUENCE_PATH}

## everything at the 30
FPS=30

###---------------------------------------------------------------------------
for CAMERA in "${CAMERAS[@]}"
do

  CAM_SEQUENCE_PATH="$(echo "${SEQUENCE_PATH}/${CAMERA}.mp4")" 
  # CAM_SEQUENCE_PATH="$(echo "${SEQUENCE_PATH}/${CAMERA}.MP4")" 

  OUTPUT_CAM_SEQUENCE_PATH="$(echo "${OUTPUT_SEQUENCE_PATH}/${CAMERA}/images")"
  mkdir -p ${OUTPUT_CAM_SEQUENCE_PATH}
  
  ffmpeg -i ${CAM_SEQUENCE_PATH} -vf fps=$FPS ${OUTPUT_CAM_SEQUENCE_PATH}/%05d.jpg & ## run in background

done
###---------------------------------------------------------------------------
echo "Waiting for all background processes to finish..."
wait
echo "All background processes finished for ${SUPER_SEQUENCE}!"

#### for mobile video image extraction, copy the video to the folder and use the command
# ffmpeg -i mobile.MP4 -vf fps=20 %05d.jpg
# ffmpeg -i mobile.MP4 -vf fps=30 %05d.jpg ## for ego4d