import os
from tqdm import tqdm

data_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/'
big_sequences = ['01_tagging', '02_legoassemble', '04_basketball', '06_volleyball', '07_fencing2', '08_badminton']


ego_total_images = 0
exo_total_images = 0

for big_sequence in big_sequences:

  big_sequence_dir = os.path.join(data_dir, big_sequence)
  sub_sequences = [sequence_name for sequence_name in sorted(os.listdir(big_sequence_dir)) if not sequence_name.startswith('calibration_') and '.' not in sequence_name]

  for sub_sequence in sub_sequences:

    if sub_sequence in ['031_badminton', '032_badminton', '033_badminton', '034_badminton', '035_badminton', '036_badminton', '037_badminton', '038_badminton', '039_badminton', '040_badminton' '041_badminton', '042_badminton', '043_badminton', '044_badminton', '045_badminton', '046_badminton', '047_badminton', '048_badminton', '049_badminton', '050_badminton', '051_badminton', '052_badminton', '053_badminton', '054_badminton', '055_badminton', '056_badminton', '057_badminton', '058_badminton', '059_badminton', '060_badminton', '061_badminton', '062_badminton']:
      continue

    sequence_dir = os.path.join(data_dir, big_sequence, sub_sequence)

    ego_total_sequence_images = 0
    ego_dir = os.path.join(sequence_dir, 'ego')
    arias = [aria for aria in sorted(os.listdir(ego_dir)) if aria.startswith('aria')]

    for aria in arias:
      aria_dir = os.path.join(ego_dir, aria, 'images', 'rgb')
      images = [image for image in sorted(os.listdir(aria_dir)) if image.endswith('.jpg')]
      ego_total_sequence_images += len(images)

    exo_total_sequence_images = 0
    exo_dir = os.path.join(sequence_dir, 'exo')
    cams = [cam for cam in sorted(os.listdir(exo_dir)) if cam.startswith('cam')]

    for cam in cams:
      cam_dir = os.path.join(exo_dir, cam, 'images')
      images = [image for image in sorted(os.listdir(cam_dir)) if image.endswith('.jpg')]
      exo_total_sequence_images += len(images)

    ego_total_images += ego_total_sequence_images
    exo_total_images += exo_total_sequence_images

    print('Sequence: {}, Ego images: {}, Exo images: {}'.format(sub_sequence, ego_total_sequence_images, exo_total_sequence_images))

print('Total ego images: {}, Total exo images: {}'.format(ego_total_images, exo_total_images))