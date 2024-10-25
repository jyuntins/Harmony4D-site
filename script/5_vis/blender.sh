cd ../../assets

# SCENE_FILE='./scene.blend'
SCENE_FILE='./original_scene.blend'

RUN_FILE='./pare/pare/utils/blender.py'

# INPUT_DIR='/home/rawalk/Desktop/ego/ego_exo/Outputs/vis'
# INPUT_DIR='/home/rawalk/Desktop/ego/cliff/data/test_samples/temp/'
# INPUT_DIR='/home/rawalk/Desktop/ego/cliff/data/test_samples/temp/meshes/'

# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/ochuman_results_interesting/imgs_/meshes/00315'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/ochuman_results_interesting/imgs_/meshes/00330'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/ochuman_results_interesting/imgs_/meshes/00340'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/ochuman_results_interesting/imgs_/meshes/00420'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/ochuman_results_interesting/imgs_/meshes/00371'

# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/2/images_/meshes/00112'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/2/images_/meshes/00127'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/2/images_/meshes/00139'
# INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/2/images_/meshes/00141'
INPUT_DIR='/home/rawalk/Desktop/ochmr/pare/Outputs/2/images_/meshes/00156'


# COLOR='turkuaz'
# COLOR='purple'
# COLOR='light_purple'
# COLOR='orange'
# COLOR='light_green'
# COLOR='green'
# COLOR='red'
COLOR='blue'
# COLOR='light_orange'
# COLOR='gray'
# COLOR='dark_gray'
# COLOR='light_yellow'
# COLOR='white'
# COLOR='light_pink'


# COLOR='white'
# COLOR='blue'

# colors = {
#     'pink': np.array([197, 27, 125]),
#     'light_pink': np.array([233, 163, 201]),
#     'light_green': np.array([161, 215, 106]),
#     'green': np.array([77, 146, 33]),
#     'red': np.array([215, 48, 39]),
#     'light_red': np.array([252, 146, 114]),
#     'light_orange': np.array([252, 141, 89]),
#     'purple': np.array([118, 42, 131]),
#     'light_purple': np.array([175, 141, 195]),
#     'light_blue': np.array([145, 191, 219]),
#     'blue': np.array([69, 117, 180]),
#     'gray': np.array([130, 130, 130]),
#     'white': np.array([255, 255, 255]),
#     'turkuaz': np.array([50, 134, 204]),
#     'orange': np.array([205, 133, 51]),
#     'light_yellow': np.array([255, 255, 224]),
# }


# IMAGE_SIZE=224
IMAGE_SIZE=512

blender -b ${SCENE_FILE} \
  --python ${RUN_FILE} -- \
  -i ${INPUT_DIR} \
  -o ${INPUT_DIR} \
  -w -t 0.05 --sideview -c ${COLOR} -s ${IMAGE_SIZE} 