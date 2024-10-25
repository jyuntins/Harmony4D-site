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
  parser.add_argument('--num_cams', help='')

  args = parser.parse_args()
    
  return args

##------------------------------------------------
def get_image_size(read_dir, camera_name, image_name, is_timesync, base_width=960, base_height=540, scale=1.0):
  if is_timesync == False:
    camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'rgb', image_name))
  else:
    camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', image_name))

  image_height = camera_image.shape[0]
  image_width = camera_image.shape[1]

  ## for smpl vis case
  if image_width == 7680:
    width = round(2*scale*base_width); height = round(scale*base_height)

  else:
    width = round(scale*base_width); height = round(scale*base_height)

  return width, height

##------------------------------------------------
def main():
  args = parse_args()
  read_dir = args.read_dir
  output_dir = args.output_dir
  num_cams = int(args.num_cams)

  output_images_dir = os.path.join(output_dir, 'exo_images')

  os.makedirs(output_dir, exist_ok=True)
  os.makedirs(output_images_dir, exist_ok=True)

  ## if given parent directory (for timesync)
  is_timesync = False
  if 'exo' in os.listdir(read_dir):
    is_timesync = True
    read_dir = os.path.join(read_dir, 'exo')

  camera_names = [camera_name for camera_name in sorted(os.listdir(read_dir)) if camera_name.startswith('cam')]

  if len(camera_names) > num_cams:
    print('Warning: num_cams is smaller than the number of cameras')
    camera_names = camera_names[:num_cams]

  if is_timesync == False:
    image_names = [image_name for image_name in sorted(os.listdir(os.path.join(read_dir, camera_names[0], 'rgb'))) if image_name.endswith('.jpg')]
  else:
    image_names = [image_name for image_name in sorted(os.listdir(os.path.join(read_dir, camera_names[0], 'images'))) if image_name.endswith('.jpg')]

  ###--------------------------------------------
  width, height = get_image_size(read_dir, camera_names[0], image_names[0], is_timesync)
  padding = 5
  divide_val = 3

  write_image_width = 3840
  write_image_height = 2160

  fps = 20
  if num_cams == 4:
    total_width_with_padding = 2*width + padding
    total_height_with_padding = 2*height + padding

    total_width = 2*width
    total_height = 2*height

    divide_val = 2

  elif num_cams == 8:
    total_width_with_padding = 3*width + 2*padding
    total_height_with_padding = 3*height + 2*padding

    total_width = 3*width
    total_height = 3*height

  elif num_cams == 9:
    total_width_with_padding = 3*width + 2*padding
    total_height_with_padding = 3*height + 2*padding

    total_width = 3*width
    total_height = 3*height

  elif num_cams >= 10 and num_cams < 16: ## we drop the last camera

    camera_names = camera_names[:9]

    total_width_with_padding = 3*width + 2*padding
    total_height_with_padding = 3*height + 2*padding

    total_width = 3*width
    total_height = 3*height

  elif num_cams >= 16 and num_cams <= 20 : ## we drop the last camera
    total_width_with_padding = 5*width + 4*padding
    total_height_with_padding = 4*height + 3*padding

    total_width = 5*width
    total_height = 4*height

    divide_val = 5 ## number of columns

  elif num_cams > 20: ## we drop the last camera
    total_width_with_padding = 5*width + 4*padding
    total_height_with_padding = 5*height + 4*padding

    total_width = 5*width
    total_height = 5*height

    divide_val = 5

  ###--------------------------------------------
  for t, image_name in enumerate(tqdm(image_names)):
    canvas = 255*np.ones((total_height_with_padding, total_width_with_padding, 3))

    for idx, camera_name in enumerate(camera_names):
      if is_timesync == False:
        camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'rgb', image_name))
      else:
        camera_image = cv2.imread(os.path.join(read_dir, camera_name, 'images', image_name))

      camera_image = cv2.resize(camera_image, (width, height))

      ##------------paste-----------------
      col_idx = idx % divide_val
      row_idx = idx // divide_val

      origin_x = width*col_idx + col_idx*padding; 
      origin_y = height*row_idx + row_idx*padding
      image = camera_image

      canvas[origin_y:origin_y + image.shape[0], origin_x:origin_x + image.shape[1], :] = image[:, :, :]

      # ## tempporary save canvas for debugging with camera names
      # cv2.imwrite(os.path.join(output_images_dir, '{}_{}.jpg'.format(camera_name, image_name)), canvas)

    ##---------resize to target size, ffmpeg does not work with offset image sizes---------
    canvas = cv2.resize(canvas, (total_width, total_height))
    canvas = cv2.resize(canvas, (write_image_width, write_image_height))
    cv2.imwrite(os.path.join(output_images_dir, image_name), canvas)
  
  ##----------make video--------------
  command = 'rm -rf {}/exo.mp4'.format(output_dir)
  os.system(command)

  command = 'ffmpeg -r {} -f image2 -i {}/%05d.jpg -pix_fmt yuv420p {}/exo.mp4'.format(fps, output_images_dir, output_dir)
  os.system(command)

  return


##------------------------------------------------
if __name__ == '__main__':
  main()