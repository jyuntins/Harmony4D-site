import numpy as np
from itertools import product
import quaternion
import cv2

def with_zeros(data):
    """
    Appends a [0, 0, 0, 1] vector to all the 3 X 4 matrices in the batch
    Args:
        data: matrix shape Batch X 3 X 4
    Returns: matrix shape Batch X 4 X 4

    """
    batch_size = data.shape[0]
    padding = np.array([0.0, 0.0, 0.0, 1.0])

    # This creates a list of data and a padding array with size Batch X 1 X 4

    concat_list = [data, np.tile(np.resize(padding, (1, 1, 4)), (batch_size, 1, 1))]
    cat_res = np.concatenate(concat_list, axis=1)
    return cat_res

def pack(data):
    """
    changes a matrix of size B x 4 x 1 to matrix of size B x 4 x 4 where all the additional values are zero
    This is useful for multiplying the global transform with the inverse of the pose transform
    Args:
        data: BATCH x 4 x 1
    Returns:

    """
    batch_size = data.shape[0]
    padding = np.zeros((batch_size, 4, 3))
    pack_list = [padding, data]
    pack_res = np.concatenate(pack_list, 2)
    return pack_res


def subtract_flat_id(rot_mats):
    """
    does R(\theta) - R(\theta*)
    R(\theta*) is a contatenation of identity matrices
    Args:
        rot_mats: shape: BATCH X 207
    Returns:

    """
    # Subtracts identity as a flattened tensor
    id_flat = np.eye(3, dtype=rot_mats.dtype)
    id_flat = np.resize(id_flat, (1, 9))
    id_flat = np.tile(id_flat, (rot_mats.shape[0], 23))
    results = rot_mats - id_flat
    return results


def rot_matrix_to_axan(data):
    """
    Converts rotation matrices to axis angles
    :param data: Rotation matrices. Shape: (Persons, Seq, 24, 3, 3)
    :return: Axis angle representation of inpute matrices. Shape: (Persons, Seq, 24, 3)
    """
    aa = quaternion.as_rotation_vector(quaternion.from_rotation_matrix(data))
    return aa


def axan_to_rot_matrix(data):
    """
    Converts the axis angle representation to a rotation matrix.
    :param data: Axis angle. Shape (batch,  24*3).
    :return: an array of shape (num_people, seq_length, 24, 3, 3).
    """
    # reshape to have sensor values explicit
    data_c = np.array(data, copy=True)
    # n = 24
    batch, n = data_c.shape[0], int(data_c.shape[1] / 3)
    data_r = np.reshape(data_c, [batch, n, 3])

    qs = quaternion.from_rotation_vector(data_r)
    rot = np.array(quaternion.as_rotation_matrix(qs))
    # size Batch x 24 x 3 x 3

    # check this
    rot = np.resize(rot, (batch, 24 * 3 * 3))
    # finally we get Batch X 24*3*3
    return rot

def compute_similarity_transform(S1, S2):
    '''
    Computes a similarity transform (sR, t) that takes
    a set of 3D points S1 (3 x N) closest to a set of 3D points S2,
    where R is an 3x3 rotation matrix, t 3x1 translation, s scale.
    i.e. solves the orthogonal Procrutes problem.
    Ensure that the first argument is the prediction

    Source: https://en.wikipedia.org/wiki/Kabsch_algorithm

    :param S1 predicted joint positions array 24 x 3
    :param S2 ground truth joint positions array 24 x 3
    :return S1_hat: the predicted joint positions after apply similarity transform
            R : the rotation matrix computed in procrustes analysis
    '''
    # If all the values in pred3d are zero then procrustes analysis produces nan values
    # Instead we assume the mean of the GT joint positions is the transformed joint value

    if not (np.sum(np.abs(S1)) == 0):
        transposed = False
        if S1.shape[0] != 3 and S1.shape[0] != 2:
            S1 = S1.T
            S2 = S2.T
            transposed = True
        assert (S2.shape[1] == S1.shape[1])

        # 1. Remove mean.
        mu1 = S1.mean(axis=1, keepdims=True)
        mu2 = S2.mean(axis=1, keepdims=True)
        X1 = S1 - mu1
        X2 = S2 - mu2

        # 2. Compute variance of X1 used for scale.
        var1 = np.sum(X1 ** 2)

        # 3. The outer product of X1 and X2.
        K = X1.dot(X2.T)

        # 4. Solution that Maximizes trace(R'K) is R=U*V', where U, V are
        # singular vectors of K.
        U, s, Vh = np.linalg.svd(K)
        V = Vh.T
        # Construct Z that fixes the orientation of R to get det(R)=1.
        Z = np.eye(U.shape[0])
        Z[-1, -1] *= np.sign(np.linalg.det(U.dot(V.T)))
        # Construct R.
        R = V.dot(Z.dot(U.T))

        # 5. Recover scale.
        scale = np.trace(R.dot(K)) / var1

        # 6. Recover translation.
        t = mu2 - scale * (R.dot(mu1))

        # 7. Error:
        S1_hat = scale * R.dot(S1) + t

        if transposed:
            S1_hat = S1_hat.T

        return S1_hat, R, scale, t
    else:
        S1_hat = np.tile(np.mean(S2, axis=0), (SMPL_NR_JOINTS, 1))
        R = np.identity(3)

        return S1_hat, R


def match_2d_greedy(
        pred_kps,
        gtkp,
        imgPath=None,
        iou_thresh=0.6,
        valid=None,
        ind=-1):
    '''
    matches groundtruth keypoints to the detection by considering all possible matchings.
    :return: best possible matching, a list of tuples, where each tuple corresponds to one match of pred_person.to gt_person.
            the order within one tuple is as follows (idx_pred_kps, idx_gt_kps)
    '''
    predList = np.arange(len(pred_kps))
    gtList = np.arange(len(gtkp))
    # get all pairs of elements in pred_kps, gtkp
    # all combinations of 2 elements from l1 and l2
    combs = list(product(predList, gtList))

    errors_per_pair = {}
    errors_per_pair_list = []
    for comb in combs:
        # vmask = valid_mask[comb[1]]
        # assert vmask.sum()>0, print('no valid points')
        errors_per_pair[str(comb)] = l2_error(
            pred_kps[comb[0]][:, :2], gtkp[comb[1]][:, :2])
        errors_per_pair_list.append(errors_per_pair[str(comb)])

    gtAssigned = np.zeros((len(gtkp),), dtype=bool)
    opAssigned = np.zeros((len(pred_kps),), dtype=bool)
    errors_per_pair_list = np.array(errors_per_pair_list)

    bestMatch = []
    excludedGtBecauseInvalid = []
    falsePositiveCounter = 0
    while np.sum(gtAssigned) < len(gtAssigned) and np.sum(
            opAssigned) + falsePositiveCounter < len(pred_kps):
        found = False
        falsePositive = False
        while not(found):
            if sum(np.inf == errors_per_pair_list) == len(
                    errors_per_pair_list):
                print('something went wrong here')

            minIdx = np.argmin(errors_per_pair_list)
            minComb = combs[minIdx]
            # compute IOU
            iou = get_bbx_overlap(
                pred_kps[minComb[0]], gtkp[minComb[1]])
            # if neither prediction nor ground truth has been matched before and iou
            # is larger than threshold
            if not(opAssigned[minComb[0]]) and not(
                    gtAssigned[minComb[1]]) and iou >= iou_thresh:
                #print(imgPath + ': found matching')
                found = True
                errors_per_pair_list[minIdx] = np.inf
            else:
                errors_per_pair_list[minIdx] = np.inf
                # if errors_per_pair_list[minIdx] >
                # matching_threshold*headBboxs[combs[minIdx][1]]:
                if iou < iou_thresh:
                    #print(
                    #   imgPath + ': false positive detected using threshold')
                    found = True
                    falsePositive = True
                    falsePositiveCounter += 1

        # if ground truth of combination is valid keep the match, else exclude
        # gt from matching
        if not(valid is None):
            if valid[minComb[1]]:
                if not falsePositive:
                    bestMatch.append(minComb)
                    opAssigned[minComb[0]] = True
                    gtAssigned[minComb[1]] = True
            else:
                gtAssigned[minComb[1]] = True
                excludedGtBecauseInvalid.append(minComb[1])

        elif not falsePositive:
            # same as above but without checking for valid
            bestMatch.append(minComb)
            opAssigned[minComb[0]] = True
            gtAssigned[minComb[1]] = True

    bestMatch = np.array(bestMatch)
    # add false positives and false negatives to the matching
    # find which elements have been successfully assigned
    opAssigned = []
    gtAssigned = []
    for pair in bestMatch:
        opAssigned.append(pair[0])
        gtAssigned.append(pair[1])
    opAssigned.sort()
    gtAssigned.sort()

    falsePositives = []
    misses = []

    # handle false positives
    opIds = np.arange(len(pred_kps))
    # returns values of oIds that are not in opAssigned
    notAssignedIds = np.setdiff1d(opIds, opAssigned)
    for notAssignedId in notAssignedIds:
        falsePositives.append(notAssignedId)
    gtIds = np.arange(len(gtList))
    # returns values of gtIds that are not in gtAssigned
    notAssignedIdsGt = np.setdiff1d(gtIds, gtAssigned)

    # handle false negatives/misses
    for notAssignedIdGt in notAssignedIdsGt:
        if not(valid is None):  # if using the new matching
            if valid[notAssignedIdGt]:
                #print(imgPath + ': miss')
                misses.append(notAssignedIdGt)
            else:
                excludedGtBecauseInvalid.append(notAssignedIdGt)
        else:
            #print(imgPath + ': miss')
            misses.append(notAssignedIdGt)

    return bestMatch, falsePositives, misses  # tuples are (idx_pred_kps, idx_gt_kps)


def get_bbx_overlap(p1, p2):
    min_p1 = np.min(p1, axis=0)
    min_p2 = np.min(p2, axis=0)
    max_p1 = np.max(p1, axis=0)
    max_p2 = np.max(p2, axis=0)

    bb1 = {}
    bb2 = {}

    bb1['x1'] = min_p1[0]
    bb1['x2'] = max_p1[0]
    bb1['y1'] = min_p1[1]
    bb1['y2'] = max_p1[1]
    bb2['x1'] = min_p2[0]
    bb2['x2'] = max_p2[0]
    bb2['y1'] = min_p2[1]
    bb2['y2'] = max_p2[1]

    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']
    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = max(0, x_right - x_left + 1) * \
        max(0, y_bottom - y_top + 1)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1'] + 1) * (bb1['y2'] - bb1['y1'] + 1)
    bb2_area = (bb2['x2'] - bb2['x1'] + 1) * (bb2['y2'] - bb2['y1'] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)

    return iou

def l2_error(j1, j2):
    return np.linalg.norm(j1 - j2, 2)


def joint_angle_error(pred_mat, gt_mat):
    """
    Compute the geodesic distance between the two input matrices.
    :param pred_mat: predicted rotation matrices. Shape: ( Seq, 9g, 3, 3)
    :param gt_mat: ground truth rotation matrices. Shape: ( Seq, 24, 3, 3)
    :return: Mean geodesic distance between input matrices.
    """
    SMPL_OR_JOINTS = np.array([0, 1, 2, 4, 5, 16, 17, 18, 19])

    gt_mat = gt_mat[:, SMPL_OR_JOINTS, :, :]

    # Reshape the matrices into B x 3 x 3 arrays
    r1 = np.reshape(pred_mat, [-1, 3, 3])
    r2 = np.reshape(gt_mat, [-1, 3, 3])

    # Transpose gt matrices
    r2t = np.transpose(r2, [0, 2, 1])

    # compute R1 * R2.T, if prediction and target match, this will be the identity matrix
    r = np.matmul(r1, r2t)

    angles = []
    # Convert rotation matrix to axis angle representation and find the angle
    for i in range(r1.shape[0]):
        aa, _ = cv2.Rodrigues(r[i])
        angles.append(np.linalg.norm(aa))

    return np.mean(np.array(angles))


def compute_auc(xpts, ypts):
    """
    Calculates the AUC.
    :param xpts: Points on the X axis - the threshold values
    :param ypts: Points on the Y axis - the pck value for that threshold
    :return: The AUC value computed by integrating over pck values for all thresholds
    """
    a = np.min(xpts)
    b = np.max(xpts)
    from scipy import integrate
    myfun = lambda x: np.interp(x, xpts, ypts)
    auc = integrate.quad(myfun, a, b)[0]
    return auc


def compute_pck(errors, THRESHOLD):
    """
    Computes Percentage-Correct Keypoints
    :param errors: N x 12 x 1
    :param THRESHOLD: Threshold value used for PCK
    :return: the final PCK value
    """
    errors_pck = errors <= THRESHOLD
    errors_pck = np.mean(errors_pck, axis=1)
    return np.mean(errors_pck)

def align_by_root(joints):
    """
    Assumes joints is 24 x 3 in SMPL order.
    Subtracts the location of the root joint from all the other joints
    """
    root = joints[0, :]

    return joints - root

def compute_prf1(count, miss, num_fp):
    if count == 0:
        return 0, 0, 0
    all_tp = count - miss
    all_fp = num_fp
    all_fn = miss
    all_f1_score = round(all_tp / (all_tp + 0.5 * (all_fp + all_fn)), 2)
    all_recall = round(all_tp / (all_tp + all_fn), 2)
    all_precision = round(all_tp / (all_tp + all_fp), 2)
    return all_precision, all_recall, all_f1_score

def compute_errors(preds3d, gt3ds, predsvertices, gtvertices):
    """
    Gets MPJPE after root alignment + MPJPE after Procrustes.
    Evaluates on all the 24 joints joints.
    Inputs:
    :param gt3ds: N x 24 x 3
    :param preds: N x 24 x 3
    :returns
        MPJPE : scalar - mean of all MPJPE errors
        MPJPE_PA : scalar- mean of all MPJPE_PA errors
        errors_pck : N x 24 - stores the error b/w GT and prediction for each joint separate
        proc_mats : N x 3 x 3 - for each frame, stores the 3 x 3 rotation matrix that best aligns the prediction and GT
    """
    SMPL_MAJOR_JOINTS = np.array([1, 2, 4, 5, 7, 8, 16, 17, 18, 19, 20, 21])
    PCK_THRESH = 150.0
    AUC_MIN = 0.0
    AUC_MAX = 200.0
    errors, errors_pa, errors_pck, auc = [], [], [], []
    vertex_errors, pa_vertex_errors = [], []

    for i, (gt3d, pred3d, gtvertex, predvertex) in enumerate(zip(gt3ds, preds3d, gtvertices, predsvertices)):
        # Root align.
        gt3d = align_by_root(gt3d)*1000
        pred3d = align_by_root(pred3d)*1000
        gtvertex = align_by_root(gtvertex)*1000
        predvertex = align_by_root(predvertex)*1000

        # Compute MPJPE
        joint_error = np.sqrt(np.sum((gt3d - pred3d) ** 2, axis=1))
        errors.append(np.mean(joint_error))

        # Joint errors for PCK Calculation
        joint_error_maj = joint_error[SMPL_MAJOR_JOINTS]
        errors_pck.append(joint_error_maj)
        errors_pck = np.stack(errors_pck, 0)
        pck_final = compute_pck(errors_pck, PCK_THRESH) * 100

        # Compute AUC
        auc_range = np.arange(AUC_MIN, AUC_MAX)
        pck_aucs = []
        for pck_thresh_ in auc_range:
            err_pck_tem = compute_pck(errors_pck, pck_thresh_)
            pck_aucs.append(err_pck_tem)

        auc_final = compute_auc(auc_range / auc_range.max(), pck_aucs) * 100       

        # MPVPE
        vertex_error = np.sqrt(np.sum((gtvertex - predvertex) ** 2, axis=1))
        vertex_errors.append(np.mean(vertex_error))

        # Compute MPJPE_PA and also store similiarity matrices to apply them later to rotation matrices for MPJAE_PA
        pred3d_sym, R, scale, t = compute_similarity_transform(pred3d, gt3d)
        pa_error = np.sqrt(np.sum((gt3d - pred3d_sym) ** 2, axis=1))
        errors_pa.append(np.mean(pa_error))

        predvertex_sym, R, scale, t = compute_similarity_transform(predvertex, gtvertex)

        pa_vertex_error = np.sqrt(np.sum((gtvertex - predvertex_sym) ** 2, axis=1))
        pa_vertex_errors.append(np.mean(pa_vertex_error))

    return np.mean(np.array(errors)), np.mean(np.array(errors_pa)), np.mean(np.array(vertex_errors)), np.mean(np.array(pa_vertex_errors)), pck_final, auc_final

def with_ones(data):
    """
    Converts an array in 3d coordinates to 4d homogenous coordiantes
    :param data: array of shape A x B x 3
    :return return ret_arr: array of shape A x B x 4 where the extra dimension is filled with ones
    """
    ext_arr = np.ones((data.shape[0], data.shape[1], 1))
    ret_arr = np.concatenate((data, ext_arr), axis=2)
    return ret_arr

def homogeneous(coordinate):
    homogeneous = np.vstack((coordinate.T, np.ones((1, coordinate.shape[0])))).T
    return homogeneous

def apply_camera_transforms(joints, rotations, camera):
    """
    Applies camera transformations to joint locations and rotations matrices
    :param joints: B x 24 x 3
    :param rotations: B x 24 x 3 x 3
    :param camera: B x 4 x 4 - already transposed
    :return: joints B x 24 x 3 joints after applying camera transformations
             rotations B x 24 x 3 x 3 - rotations matrices after applying camera transformations
    """
    joints = with_ones(joints)  # B x 4 x 4
    joints = np.matmul(joints, camera)

    # multiply all rotation matrices with the camera rotation matrix
    # transpose camera coordinates back
    cam_new = np.transpose(camera[:, :3, :3], (0, 2, 1))
    cam_new = np.expand_dims(cam_new, 1)
    cam_new = np.tile(cam_new, (1, 24, 1, 1))
    # B x 24 x 3 x 3
    rotations = np.matmul(cam_new, rotations)

    return joints[:, :, :3], rotations


def check_valid_inds(poses2d, camposes_valid):
    """
    Computes the indices where further computations are required
    :param poses2d: N x 18 x 3 array of 2d Poses
    :param camposes_valid: N x 1 array of indices where camera poses are valid
    :return: array of indices indicating frame ids in the sequence which are to be evaluated
    """

    # find all indices in the N sequences where the sum of the 18x3 array is not zero
    # N, numpy array
    poses2d_mean = np.mean(np.mean(np.abs(poses2d), axis=2), axis=1)
    poses2d_bool = poses2d_mean == 0
    poses2d_bool_inv = np.logical_not(poses2d_bool)

    # find all the indices where the camposes are valid
    camposes_valid = np.array(camposes_valid).astype('bool')

    final = np.logical_and(poses2d_bool_inv, camposes_valid)
    indices = np.array(np.where(final == True)[0])

    return indices