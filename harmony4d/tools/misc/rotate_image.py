import cv2
import numpy as np
import os
from tqdm import tqdm
import json

###-------------------
# DATA_DIR = '/home/rawalk/Desktop/datasets/dummy/basketball/rawal/'
# DATA_DIR = '/home/rawalk/Desktop/datasets/dummy/basketball/minh/'
# DATA_DIR = '/home/rawalk/Desktop/datasets/dummy/basketball/akash/'
DATA_DIR = '/home/rawalk/Desktop/datasets/dummy/basketball/christian/'

##-------------------
SOURCE_RGB_DIR = os.path.join(DATA_DIR, '214-1')
SOURCE_LEFT_STEREO_DIR = os.path.join(DATA_DIR, '1201-1')
SOURCE_RIGHT_STEREO_DIR = os.path.join(DATA_DIR, '1201-2')

RGB_FPS = 20
STEREO_FPS = 20

##-------------------
TARGET_RGB_DIR = os.path.join(DATA_DIR, 'rgb')
TARGET_LEFT_STEREO_DIR = os.path.join(DATA_DIR, 'left')
TARGET_RIGHT_STEREO_DIR = os.path.join(DATA_DIR, 'right')

if not os.path.exists(TARGET_RGB_DIR): os.makedirs(TARGET_RGB_DIR)
if not os.path.exists(TARGET_LEFT_STEREO_DIR): os.makedirs(TARGET_LEFT_STEREO_DIR)
if not os.path.exists(TARGET_RIGHT_STEREO_DIR): os.makedirs(TARGET_RIGHT_STEREO_DIR)

##--------------------------------------------
def rotate_and_save(source_images_dir, target_images_dir, fps=20):
  images_path = [os.path.join(source_images_dir, x) for x in sorted(os.listdir(source_images_dir)) if x.endswith('.jpg') or
                 x.endswith('.jpeg') or
                 x.endswith('.png')]

  for image_path in tqdm(images_path):
    image = cv2.imread(image_path)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    image_name = image_path.split('/')[-1]
    save_image_path = os.path.join(target_images_dir,  image_name)
    cv2.imwrite(save_image_path, image)

  return

##--------------------------------------------
### convert rgb images
source_images_dir = SOURCE_RGB_DIR
target_images_dir = TARGET_RGB_DIR
fps = RGB_FPS

rotate_and_save(source_images_dir, target_images_dir, fps)

# ##--------------------------------------------
### convert left stereo images
source_images_dir = SOURCE_LEFT_STEREO_DIR
target_images_dir = TARGET_LEFT_STEREO_DIR
fps = STEREO_FPS

rotate_and_save(source_images_dir, target_images_dir, fps)

##--------------------------------------------
### convert rgb images
source_images_dir = SOURCE_RIGHT_STEREO_DIR
target_images_dir = TARGET_RIGHT_STEREO_DIR
fps = STEREO_FPS

rotate_and_save(source_images_dir, target_images_dir, fps)


