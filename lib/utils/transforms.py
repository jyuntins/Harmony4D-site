import numpy as np
import cv2

def linear_transform(points_3d, T):
    assert(points_3d.shape[1] == 3)

    points_3d_homo = np.ones((4, points_3d.shape[0]))
    points_3d_homo[:3, :] = np.copy(points_3d.T)

    points_3d_prime_homo = np.dot(T, points_3d_homo)
    points_3d_prime = points_3d_prime_homo[:3, :]/ points_3d_prime_homo[3, :]
    points_3d_prime = points_3d_prime.T

    return points_3d_prime

def fast_circle(image, overlay, points_2d, radius, color):
    for idx in range(len(points_2d)):
        image = cv2.circle(image, (round(points_2d[idx, 0]), round(points_2d[idx, 1])), radius, color, -1)

        if overlay is not None:
            overlay = cv2.circle(overlay, (round(points_2d[idx, 0]), round(points_2d[idx, 1])), radius, color, -1)

    if overlay is None:
        return image

    return image, overlay
