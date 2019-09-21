import numpy as np


def normalize(A):
    sum = np.sum(A, 0)
    V = A.shape[0]
    D = np.zeros((V, V))
    for i in range(V):
        if sum[i] > 0:
            D[i, i] = 1.0 / sum[i]
    return np.dot(A, D)

def main():
    H = 16
    W = 8
    V = H * W
    len_t = 24 * (31 + 31 + 30)
    K = 9
    label = np.load('../poi/regular_label_.npy')
    label = np.tile(label, (V, 1)).transpose()
    adj_mat = np.load('path_bike_nyc_regular.npy')

    sum = np.zeros((24 * 2, V, V), dtype=np.float32)
    A = np.zeros((24 * 2, V, V, K + 1), dtype=np.float32)
    eye = np.eye(V)
    neg_eye = 1 - eye
    holiday = [i for i in range(1, 93, 7)] + [i for i in range(2, 93, 7)] + [4, 66]
    for day in holiday:
        sum[24:48, :, :] += adj_mat[(day - 1) * 24: day * 24, :, :]
    for t in range(24):
        sum[t, :, :] = np.sum(adj_mat[t:len_t:24, :, :], axis=0) - sum[24 + t, :, :]
        adjacency = sum[t, :, :]
        normalized_adjacency = normalize(adjacency.transpose() * neg_eye)
        A[t, :, :, 0] = eye
        for k in range(K):
            A[t, :, :, 1 + k][label == k] = normalized_adjacency[label == k]
    for t in range(24, 48):
        adjacency = sum[t, :, :]
        normalized_adjacency = normalize(adjacency.transpose() * neg_eye)
        A[t, :, :, 0] = eye
        for k in range(K):
            A[t, :, :, 1 + k][label == k] = normalized_adjacency[label == k]
    np.save('regular_path.npy', A)


if __name__ == "__main__":
    main()
