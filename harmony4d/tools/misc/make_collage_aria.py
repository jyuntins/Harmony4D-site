import cv2
import numpy as np
import os
from tqdm import tqdm
import json
import argparse
import shutil

##------------------------------------------------
def parse_args():
  parser = argparse.ArgumentParser(description='Time sync copy')
  parser.add_argument('--read_dir', help='')
  parser.add_argument('--output_dir', help='')
  parser.add_argument('--num_arias', help='')

  args = parser.parse_args()
    
  return args

##------------------------------------------------
def get_image_size(read_dir, camera_name, image_name, is_timesync):
  if is_timesync == False:
    camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'rgb', image_name))
  else:
    camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', 'rgb', image_name))

  image_height = camera_image.shape[0]
  image_width = camera_image.shape[1]

  rgb_width = 960; rgb_height = 960; 
  gray_width = 720; gray_height = 960;

  ## for smpl vis case
  if image_width == 2816:
    rgb_width *= 2
    gray_width *= 2

  return rgb_width, rgb_height, gray_width, gray_height

##------------------------------------------------
def main():
  args = parse_args()
  read_dir = args.read_dir
  output_dir = args.output_dir
  num_arias = int(args.num_arias)

  output_images_dir = os.path.join(output_dir, 'aria_images')

  os.makedirs(output_dir, exist_ok=True)
  os.makedirs(output_images_dir, exist_ok=True)

  is_smpl_cam_blender = False
  if 'vis_smpl_cam_blender' in read_dir.split('/'):
    is_smpl_cam_blender = True

  ## if given parent directory (for timesync)
  is_timesync = False
  if 'ego' in os.listdir(read_dir):
    is_timesync = True
    read_dir = os.path.join(read_dir, 'ego')

  camera_names = [camera_name for camera_name in sorted(os.listdir(read_dir)) if camera_name.startswith('aria')]

  if is_timesync == False:
    image_names = [image_name for image_name in sorted(os.listdir(os.path.join(read_dir, camera_names[0], 'rgb'))) if image_name.endswith('.jpg')]
  else:
    image_names = [image_name for image_name in sorted(os.listdir(os.path.join(read_dir, camera_names[0], 'images', 'rgb'))) if image_name.endswith('.jpg')]

  rgb_width, rgb_height, gray_width, gray_height = get_image_size(read_dir, camera_names[0], image_names[0], is_timesync)

  padding = 5
  fps = 20

  aria_width = rgb_width + 2*gray_width if not is_smpl_cam_blender else rgb_width
  aria_height = rgb_height

  if num_arias == 1:
    total_width = aria_width
    total_height = aria_height
    padding = 0

    total_width_with_padding = aria_width + padding
    total_height_with_padding = aria_height + padding

  elif num_arias <= 4:
    total_width = 2*aria_width
    total_height = 2*aria_height

    total_width_with_padding = 2*aria_width + padding
    total_height_with_padding = 2*aria_height + padding

  elif num_arias == 6:
    total_width = 3*aria_width
    total_height = 2*aria_height

    total_width_with_padding = 3*aria_width + 2*padding
    total_height_with_padding = 2*aria_height + padding

  for t, image_name in enumerate(tqdm(image_names)):
    canvas = 255*np.ones((total_height_with_padding, total_width_with_padding, 3))

    for idx, camera_name in enumerate(camera_names):

      if is_timesync == False and is_smpl_cam_blender == False:
        rgb_image = cv2.imread(os.path.join(read_dir, camera_name, 'rgb', image_name))

        try:
          left_image = cv2.imread(os.path.join(read_dir, camera_name, 'left', image_name))
          right_image = cv2.imread(os.path.join(read_dir, camera_name, 'right', image_name))
        except:
          print('no left/right image')
          left_image = None
          right_image = None

      elif is_smpl_cam_blender == True:
        rgb_image = cv2.imread(os.path.join(read_dir, camera_name, 'rgb', image_name))
        left_image = None
        right_image = None
      else:
        rgb_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', 'rgb', image_name))
        
        try:
          left_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', 'left', image_name))
          right_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', 'right', image_name))
        except:
          print('no left/right image')
          left_image = None
          right_image = None

      assert rgb_image is not None
      rgb_image = cv2.resize(rgb_image, (rgb_width, rgb_height))
      
      if left_image is not None:
        left_image = cv2.resize(left_image, (gray_width, gray_height))
      
      if right_image is not None:
        right_image = cv2.resize(right_image, (gray_width, gray_height))

      camera_image = np.zeros((aria_height, aria_width, 3))

      if left_image is not None:
        origin_x = 0; origin_y = 0; image = left_image
        camera_image[origin_y:origin_y + image.shape[0], origin_x:origin_x + image.shape[1], :] = image[:, :, :]

      if is_smpl_cam_blender == False:
        origin_x = gray_width; origin_y = 0; image = rgb_image
      else:
        origin_x = 0; origin_y = 0; image = rgb_image

      camera_image[origin_y:origin_y + image.shape[0], origin_x:origin_x + image.shape[1], :] = image[:, :, :]

      if right_image is not None:
        origin_x = gray_width + rgb_width; origin_y = 0; image = right_image
        camera_image[origin_y:origin_y + image.shape[0], origin_x:origin_x + image.shape[1], :] = image[:, :, :]

      ##------------paste-----------------
      if num_arias <= 4:
        if idx == 0:
          origin_x = 0; origin_y = 0; image = camera_image
        elif idx == 1:
          origin_x = aria_width + padding; origin_y = 0; image = camera_image
        elif idx == 2:
          origin_x = 0; origin_y = aria_height + padding; image = camera_image
        elif idx == 3:
          origin_x = aria_width + padding; origin_y = aria_height + padding; image = camera_image

      elif num_arias == 6:
        if idx == 0:
          origin_x = 0; origin_y = 0; image = camera_image
        elif idx == 1:
          origin_x = aria_width + padding; origin_y = 0; image = camera_image
        elif idx == 2:
          origin_x = 2*aria_width + 2*padding; origin_y = 0; image = camera_image
        elif idx == 3:
          origin_x = 0; origin_y = aria_height + padding; image = camera_image
        elif idx == 4:
          origin_x = aria_width + padding; origin_y = aria_height + padding; image = camera_image
        elif idx == 5:
          origin_x = 2*aria_width + 2*padding; origin_y = aria_height + padding; image = camera_image

      canvas[origin_y:origin_y + image.shape[0], origin_x:origin_x + image.shape[1], :] = image[:, :, :]

    ##---------resize to target size, ffmpeg does not work with offset image sizes---------
    canvas = cv2.resize(canvas, (total_width, total_height))
    cv2.imwrite(os.path.join(output_images_dir, image_name), canvas)
  
  ##----------make video--------------
  command = 'rm -rf {}/aria.mp4'.format(output_dir)
  os.system(command)

  command = 'ffmpeg -r {} -f image2 -i {}/%05d.jpg -pix_fmt yuv420p {}/aria.mp4'.format(fps, output_images_dir, output_dir)
  os.system(command)
  return


##------------------------------------------------
if __name__ == '__main__':
  main()