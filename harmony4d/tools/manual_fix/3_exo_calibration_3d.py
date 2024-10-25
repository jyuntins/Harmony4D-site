import cv2 
import glob
import numpy as np
import sys
from scipy import linalg
import yaml
import os
from scipy.spatial.transform import Rotation as R

# https://www.pythonpool.com/opencv-solvepnp/

## returns T x points_3d
def linear_transform(points_3d, T):
    points_3d_homo = np.ones((4, points_3d.shape[0]))
    points_3d_homo[:3, :] = np.copy(points_3d.T)

    points_3d_prime_homo = np.dot(T, points_3d_homo)
    points_3d_prime = points_3d_prime_homo[:3, :]/ points_3d_prime_homo[3, :]
    points_3d_prime = points_3d_prime.T
    return points_3d_prime

###----------------------------------------------------------------------------
# https://yangcha.github.io/iview/iview.html
### you need atleast 6 points!
## in colmap reference
points_3d = np.array([[-9.22852996e+00, -4.09188248e+00, -7.28080869e-01],
       [-9.42410449e+00, -3.82399492e+00,  9.97844734e-01],
       [-9.15531518e+00, -4.53464323e+00, -3.49507781e+00],
       [-9.18691478e+00, -4.24081101e+00, -1.78120788e+00],
       [ 9.96284774e-01,  7.34899972e-01, -1.06575504e-02],
       [ 1.11258206e+00,  7.36567891e-01, -1.25471488e-03],
       [ 1.32860991e+00,  7.38184544e-01,  1.79614553e-02],
       [ 1.16586975e+00,  5.88704931e-01, -9.37039831e-01],
       [ 1.38040937e+00,  5.95184605e-01, -9.18901796e-01]])


## labelled points for target camera
points_2d = np.array([[1560.,  669.],
       [1797.,  666.],
       [1188.,  687.],
       [1419.,  678.],
       [1956., 1695.],
       [1974., 1722.],
       [2010., 1770.],
       [1203., 1758.],
       [1155., 1815.]])

##---projected points (has error) for target camera
projected_points_2d = np.array([[1560.67964342,  670.56284076],
       [1797.09034595,  669.80793632],
       [1188.33873193,  688.33906742],
       [1416.76737419,  678.11590177],
       [1961.29139761, 1687.10234919],
       [1980.39912535, 1711.0412359 ],
       [2022.87895672, 1760.79213897],
       [1208.35640783, 1752.27885391],
       [1169.4177888 , 1811.26786978]])


## extrinsics in colmap, raw_extrinsics in the code
extrinsics = np.array([[ 0.09858315,  0.20329282,  0.97414239, -0.18362307],
       [-0.07645838,  0.97756454, -0.1962694 ,  0.14510389],
       [-0.99218722, -0.0551325 ,  0.11191483,  3.23430395],
       [ 0.        ,  0.        ,  0.        ,  1.        ]])

# target_camera_name = "cam03"
# target_camera_name = "cam06"
# target_camera_name = "cam12"
# target_camera_name = "cam04"
# target_camera_name = "cam01"
# target_camera_name = "cam04"
# target_camera_name = "cam05"
target_camera_name = "cam12"

##--------------------------------------------------------------
# big_sequence = '07_fencing2'
# sequence_name = 'calibration_fencing2'

# big_sequence = '08_badminton'
# sequence_name = 'calibration_badminton'

# big_sequence = '04_basketball'
# sequence_name = '001_basketball'

big_sequence = '06_volleyball'
sequence_name = 'calibration_volleyball'

# colmap_info = "8 OPENCV_FISHEYE 3840 2160 1906.5307312449661 1912.1594474695269 1920 1080 0.027968215637947744 0.079122752537819724 -0.10330772063707933 0.0495460217949747"
# colmap_info = "5 OPENCV_FISHEYE 3840 2160 1915.346061677637 1915.5916704165572 1920 1080 0.011796064531609635 0.14914315583208387 -0.18100627257344351 0.079925659938671886"
# colmap_info = "9 OPENCV_FISHEYE 3840 2160 1936.5793400606167 1932.9311482035462 1920 1080 0.016902164724821603 0.1372130878368841 -0.19691565085513565 0.098310991218227964"
colmap_info = "16 OPENCV_FISHEYE 3840 2160 1754.8638432704706 1753.4486006974907 1920 1080 0.03218214440039683 0.11393967284847671 -0.1897233914101884 0.093804063292024842"

image_path = '/media/rawalk/disk1/rawalk/datasets/ego_exo/main/{}/{}/exo/{}/images/00001.jpg'.format(big_sequence, sequence_name, target_camera_name)
image = cv2.imread(image_path)
image_width = image.shape[1]
image_height = image.shape[0]

###--------------------------------------------------------------------------------
colmap_info = [float(val) for val in colmap_info.split()[4:]]
fx = colmap_info[0]
fy = colmap_info[1]
cx = colmap_info[2]
cy = colmap_info[3]
k1 = colmap_info[4]
k2 = colmap_info[5]
k3 = colmap_info[6]
k4 = colmap_info[7]
K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
D = np.array([k1, k2, 0, 0, k3, k4, 0, 0]) ## distCoeffs1 output vector of distortion coefficients [k1,k2,p1,p2,k3,k4,k5,k6,s1,s2,s3,s4,taux,tauy] of 4, 5, 8, 12 or 14 elements. 
D_fisheye = np.array([k1, k2, k3, k4,])

###-------------------openc fisheye projection-------------------------
def project(point_3d, fx, fy, cx, cy, k1, k2, k3, k4, extrinsics):
    point_3d_cam = (linear_transform(points_3d=point_3d.reshape(1, 3), T=extrinsics))[0] ## RX + T
    x = point_3d_cam[0]
    y = point_3d_cam[1]
    z = point_3d_cam[2]

    # https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
    a = x/z; b = y/z
    r = np.sqrt(a*a + b*b)
    theta = np.arctan(r)
    theta_d = theta * (1 + k1*theta**2 + k2*theta**4 + k3*theta**6 + k4*theta**8)
    x_prime = (theta_d/r)*a
    y_prime = (theta_d/r)*b

    u = fx*(x_prime + 0) + cx
    v = fy*y_prime + cy

    return np.array([u, v])

##----------verify--------------
num_points = len(points_3d)
points_3d_opencv = np.expand_dims(np.asarray(points_3d), -2)
rotvec = R.from_matrix(extrinsics[:3, :3]).as_rotvec()
tvec = extrinsics[:3, 3]
opencv_projected_points_2d, jacobian = cv2.fisheye.projectPoints(points_3d_opencv, rotvec.reshape(1, 1, -1), tvec.reshape(1, 1, -1), K, D_fisheye)
opencv_projected_points_2d = opencv_projected_points_2d.reshape(-1, 2)

print('custom_fisheye, expected_colmap, opencv')
for idx in range(num_points):
    custom_projected_point_2d = project(points_3d[idx], fx, fy, cx, cy, k1, k2, k3, k4, extrinsics)
    print(custom_projected_point_2d, projected_points_2d[idx], opencv_projected_points_2d[idx])

###------------------------undistort points--------------------------------------------------------
# https://stackoverflow.com/questions/61147903/what-is-the-correct-way-to-undistort-points-captured-using-fisheye-camera-in-ope
K_undistorted = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D_fisheye, (image_width, image_height), np.eye(3), balance=1.0)
points_2d_opencv = np.expand_dims(np.asarray(points_2d), -2)
undistorted_points_2d_normalized = np.squeeze(cv2.fisheye.undistortPoints(points_2d_opencv, K, D_fisheye))
undistorted_points_2d = np.zeros_like(undistorted_points_2d_normalized)

fx_ = K_undistorted[0, 0]
fy_ = K_undistorted[1, 1]
cx_ = K_undistorted[0, 2]
cy_ = K_undistorted[1, 2]

for idx, undistorted_point_2d_normalized in enumerate(undistorted_points_2d_normalized):
    x = undistorted_point_2d_normalized[0]
    y = undistorted_point_2d_normalized[1]
    undistorted_points_2d[idx, 0] = x*fx_ + cx_
    undistorted_points_2d[idx, 1] = y*fy_ + cy_

###-------------------------------------------------------------------------------------------------
success, rotation_vector, translation_vector = cv2.solvePnP(points_3d, undistorted_points_2d, K_undistorted, None, flags=0)
new_opencv_projected_points_2d, jacobian = cv2.fisheye.projectPoints(points_3d_opencv, rotation_vector.reshape(1, 1, -1), translation_vector.reshape(1, 1, -1), K, D_fisheye)
new_opencv_projected_points_2d = new_opencv_projected_points_2d.reshape(-1, 2)

print()
print('calibrated points using opencv')
print(new_opencv_projected_points_2d)
print()

for idx in range(len(new_opencv_projected_points_2d)):
    image = cv2.circle(image, (round(new_opencv_projected_points_2d[idx, 0]), round(new_opencv_projected_points_2d[idx, 1])), 10, (0, 0, 2550), -1)
    image = cv2.putText(image, 'id:{}'.format(idx + 1), (round(new_opencv_projected_points_2d[idx, 0]), round(new_opencv_projected_points_2d[idx, 1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

factor = 3.0
cv2.namedWindow('reprojected points using calibration')
image_resized = cv2.resize(image, (int(image_width/factor), int(image_height/factor)), interpolation=cv2.INTER_AREA)

while True:
    cv2.imshow('reprojected points using calibration', image_resized)
    key = cv2.waitKey(5) & 0xFF

    if key == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()

rotation_matrix = R.from_rotvec(rotation_vector.reshape(-1)).as_matrix()
new_extrinsics = np.eye(4)
new_extrinsics[:3, :3] = rotation_matrix[:, :]
new_extrinsics[:3, 3] = (translation_vector.reshape(-1))[:]

print('old camera extrinsics')
print(repr(extrinsics))
print()


print('new camera extrinsics in colmap referenece')
print(repr(new_extrinsics))
print()

np.save('{}.npy'.format(target_camera_name), new_extrinsics)