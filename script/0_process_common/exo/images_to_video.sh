
DATA_DIR='/home/rawalk/Desktop/ego/mmpose/Outputs/vis/ego_exo'

# SEQUENCE='001_tagging'
SEQUENCE='002_tagging_leg'
# SEQUENCE='003_tagging_game'
# SEQUENCE='004_tagging_walk'
# SEQUENCE='005_tagging_circle'
# SEQUENCE='006_dodgeball_1'
# SEQUENCE='007_dodgeball_2'
# SEQUENCE='008_basketball_1'
# SEQUENCE='009_basketball_2'
# SEQUENCE='010_basketball_3'
# SEQUENCE='011_passing'

FPS=30

OUTPUT_SEQUENCE_PATH="$(echo "${DATA_DIR}/${SEQUENCE}/videos")"
mkdir -p ${OUTPUT_SEQUENCE_PATH}

# ###--------------------single inference------------------------
# CAMERA='cam01'
# CAMERA='cam02'
# CAMERA='cam03'
# CAMERA='cam04'
# CAMERA='cam05'
# CAMERA='cam06'
# CAMERA='cam07'
# CAMERA='cam08' 


# CAMERA_SEQUENCE_PATH="$(echo "${DATA_DIR}/${SEQUENCE}/${CAMERA}/images")"

# cd ${CAMERA_SEQUENCE_PATH}
# ffmpeg -r ${FPS} -f image2 -i %*.jpg -pix_fmt yuv420p ${OUTPUT_SEQUENCE_PATH}/${CAMERA}.mp4

# ###--------------------for loop------------------------
CAMERAS=('cam01' 'cam02' 'cam03' 'cam04' 'cam05' 'cam06' 'cam07' 'cam08')

for CAMERA in "${CAMERAS[@]}"
do
  CAMERA_SEQUENCE_PATH="$(echo "${DATA_DIR}/${SEQUENCE}/${CAMERA}/images")"
  cd ${CAMERA_SEQUENCE_PATH}
  ffmpeg -r ${FPS} -f image2 -i %*.jpg -pix_fmt yuv420p ${OUTPUT_SEQUENCE_PATH}/${CAMERA}.mp4

done