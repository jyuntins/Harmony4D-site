import cv2
import numpy as np
import os
from tqdm import tqdm

# for camera other than the calibration one
def read_qr_code_single(img):
    """get an image and read the QR code.
    """    
    try:
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return int(value)
    except:
        return 0

# just for cam1
def read_qr_code_double(img):
    """
    get an image and read the QR code.
    Erwin's time stamp are all digits with a length of 13
    Kenta's time stamp with period and was 17-digit long
    """    
    ts1=0 #kenta's timestamp
    ts2=0 #erwin's timestamp
    try:
        detect = cv2.QRCodeDetector()
        results = detect.detectAndDecodeMulti(img)
        for value in results[1]:
            #this is a hard code to check kenta's qr code
            if "." in value:
                #remove the period and trim to 13 digit
                ts1 = value.replace('.', '')[:13]
            #this is erwin's code
            elif len(value)==13:
                ts2 = value
        return int(ts1), int(ts2)
    except:
        return 0, 0

# ##--------read aria qr codes--------------------------------------------
data_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/common/raw_from_cameras'
time_synced_data_dir = '/media/rawalk/disk1/rawalk/datasets/ego_exo/common/time_synced_exo'
sequence_name = 'kentawalk'

# ##--------read cam01--------------------------------------------
# cam = 'aria01'; start_idx = 30; end_idx = 100
cam = 'cam01'; start_idx = 30; end_idx = 100
# cam = 'cam02'; start_idx = 30; end_idx = 80
# cam = 'cam03'; start_idx = 30; end_idx = 80
# cam = 'cam04'; start_idx = 30; end_idx = 80
# cam = 'cam05'; start_idx = 30; end_idx = 80
# cam = 'cam06'; start_idx = 30; end_idx = 80
# cam = 'cam07'; start_idx = 30; end_idx = 80
# cam = 'cam08'; start_idx = 30; end_idx = 80


##----------------------------------------------------------------
if cam.startswith('cam'):
    rgb_dir = os.path.join(time_synced_data_dir, sequence_name, 'exo', cam, 'images')

else:
    rgb_dir = os.path.join(data_dir, sequence_name, cam, 'images', 'rgb')

###---------------------------------------------------------------------
rgb_images = sorted(os.listdir(rgb_dir))

valid_rgb_images = []
valid_ts = []


for idx, rgb_image in enumerate(tqdm(rgb_images)):
    
    if idx < start_idx or idx > end_idx:
        continue

    image = cv2.imread(os.path.join(rgb_dir, rgb_image))

    if cam == 'cam01':
        _, ts = read_qr_code_double(image); print('double qr')
    else:
        ts = read_qr_code_single(image)

    if ts != 0:
        valid_rgb_images.append(rgb_image)
        ts = ts - 1675291000000
        valid_ts.append(ts)

        print(ts, rgb_image)

print('------all timestamps------')
print(sequence_name, cam)
for ts, rgb_image in zip(valid_ts, valid_rgb_images):
    print('{} {}'.format(str(ts).zfill(8), rgb_image))