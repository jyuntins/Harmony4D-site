import trimesh
import numpy as np
from trimesh.viewer import SceneViewer
import cv2

class CustomViewer(SceneViewer):
    def on_key_press(self, symbol, modifiers):
        self.close()

def visualize_vertices(vertices):   

    for scene_idx in range(vertices.shape[0]):
        scene = trimesh.Scene()
        
        scene_vertices = vertices[scene_idx]

        for human_vertices in scene_vertices:
            human_vertices[:, 1] = human_vertices[:, 1]*-1
            point_cloud = trimesh.points.PointCloud(human_vertices)
            scene.add_geometry(point_cloud)
        print('Visualizing scene {}'.format(scene_idx+1))

        viewer = CustomViewer(scene)

    return

def visualize_keypoints_3d(keypoints_3d):

    for scene_idx in range(keypoints_3d.shape[0]):
        scene = trimesh.Scene()
        
        scene_keypoints_3d = keypoints_3d[scene_idx]
        
        for human_keypoints_3d in scene_keypoints_3d:
            human_keypoints_3d[:, 1] = human_keypoints_3d[:, 1]*-1
            point_cloud = trimesh.points.PointCloud(human_keypoints_3d)
            scene.add_geometry(point_cloud)
        print('Visualizing scene {}'.format(scene_idx+1))

        viewer = CustomViewer(scene)

    return

def draw_skeleton(frame, joints_2d, color=(255, 0, 0)):
    for joint in joints_2d:
        # import pdb; pdb.set_trace()
        x, y = int(joint[0]), int(joint[1])
        cv2.circle(frame, (x, y), 6, color, -1)  # Draw joint
    return frame

def visualize_keypoints_2d(keypoints_2d):

    frame_size = (3840, 2160)
    for scene_idx in range(keypoints_2d.shape[0]):


    # Create an empty frame with white background
        frame = np.ones((frame_size[1], frame_size[0], 3), dtype=np.uint8) * 255

    # Draw the skeleton on the frame
        for human_keypoints_2d in keypoints_2d[scene_idx]:
            frame = draw_skeleton(frame, human_keypoints_2d)

        frame = cv2.resize(frame, (960, 540))
        frame = cv2.putText(frame, 'Frame: '+str(scene_idx+1), (50,50), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (255, 0, 0), 2, cv2.LINE_AA) 
        cv2.imshow('keypoitns_2d', frame)
        if cv2.waitKey(0) == ord('q'):
            break


    # Write the frame to the video