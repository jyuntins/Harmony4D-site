from thirdparty.libmesh.inside_mesh import check_mesh_contains
from scipy.spatial.distance import cdist
import trimesh
import numpy as np


def penetration(obj_verts, obj_faces, hand_verts, mode="max"):
    from thirdparty.libmesh.inside_mesh import check_mesh_contains
    # import pdb; pdb.set_trace()
    obj_trimesh = trimesh.Trimesh(vertices=np.asarray(obj_verts), faces=np.asarray(obj_faces))
    inside = check_mesh_contains(obj_trimesh, hand_verts)

    valid_vals = inside.sum()
    if valid_vals > 0:
        selected_hand_verts = hand_verts[inside, :]

        mins_sel_hand_to_obj = np.min(cdist(selected_hand_verts, obj_verts), axis=1)

        collision_vals = mins_sel_hand_to_obj
        if mode == "max":
            penetr_val = np.max(collision_vals)  # max
        elif mode == "mean":
            penetr_val = np.mean(collision_vals)
        elif mode == "sum":
            penetr_val = np.sum(collision_vals)
        else:
            raise KeyError("unexpected penetration mode")
    else:
        penetr_val = 0
    return penetr_val, valid_vals

def solid_intersection_volume(hand_verts, hand_faces, obj_vox_points, obj_vox_el_vol, return_kin=False):
    # create hand trimesh
    hand_trimesh = trimesh.Trimesh(vertices=np.asarray(hand_verts), faces=np.asarray(hand_faces))

    inside = check_mesh_contains(hand_trimesh, obj_vox_points)
    volume = inside.sum() * obj_vox_el_vol
    if return_kin:
        return volume, inside
    else:
        return volume