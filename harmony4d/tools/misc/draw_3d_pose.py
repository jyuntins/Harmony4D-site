import os
import numpy as np
import matplotlib.pyplot as plt

read_file_name = '00120.npy'

# load data
data = np.load(read_file_name, allow_pickle=True).item()

pose3d_A = data['aria01']
pose3d_B = data['aria02']

# define COCO keypoints connections
limbs = [
    [0, 1], [0, 2], [1, 3], [2, 4], [5, 7], [7, 9],
    [6, 8], [8, 10], [5, 6], [5, 11], [6, 12], [11, 12],
    [11, 13], [13, 15], [12, 14], [14, 16]
]

# create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot keypoints and limbs for pose3d_A (blue color)
for i, j in limbs:
    ax.plot([pose3d_A[i, 0], pose3d_A[j, 0]], 
            [pose3d_A[i, 1], pose3d_A[j, 1]], 
            [pose3d_A[i, 2], pose3d_A[j, 2]], 'b-')
ax.scatter(pose3d_A[:, 0], pose3d_A[:, 1], pose3d_A[:, 2], c='b', marker='o')

# plot keypoints and limbs for pose3d_B (green color)
for i, j in limbs:
    ax.plot([pose3d_B[i, 0], pose3d_B[j, 0]], 
            [pose3d_B[i, 1], pose3d_B[j, 1]], 
            [pose3d_B[i, 2], pose3d_B[j, 2]], 'g-')
ax.scatter(pose3d_B[:, 0], pose3d_B[:, 1], pose3d_B[:, 2], c='g', marker='o')

# set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# save plot to disk
plt.savefig('3d_poses.png')
plt.show()

# calculate height of Human A and Human B
height_A = pose3d_A[0, 2] - min(pose3d_A[15, 2], pose3d_A[16, 2])
height_B = pose3d_B[0, 2] - min(pose3d_B[15, 2], pose3d_B[16, 2])

print(f'Height of Human A: {height_A:.2f} units')
print(f'Height of Human B: {height_B:.2f} units')
