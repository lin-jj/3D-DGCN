import numpy as np
from sklearn.cluster import KMeans


def main():
    f = open('../flow/irregular_boundary.txt', 'r')
    a = f.read()
    boundary = eval(a)
    V = len(boundary)
    K = 9
    C = 10
    poi_category = {}
    poi_category['Shop & Service'] = 0
    poi_category['Arts & Entertainment'] = 1
    poi_category['Outdoors & Recreation'] = 2
    poi_category['Nightlife Spot'] = 3
    poi_category['Travel & Transport'] = 4
    poi_category['College & University'] = 5
    poi_category['Professional & Other Places'] = 6
    poi_category['Residence'] = 7
    poi_category['Food'] = 8
    poi_category['Event'] = 9
    lng_max = np.zeros(V)
    lng_min = np.zeros(V)
    lng_mean = np.zeros(V)
    lat_max = np.zeros(V)
    lat_min = np.zeros(V)
    lat_mean = np.zeros(V)
    for i in range(V):
        boundary_i = np.array(boundary[i])
        lng_max[i], lng_min[i], lng_mean[i] = np.max(boundary_i[:, 0]), np.min(boundary_i[:, 0]), np.mean(boundary_i[:, 0])
        lat_max[i], lat_min[i], lat_mean[i] = np.max(boundary_i[:, 1]), np.min(boundary_i[:, 1]), np.mean(boundary_i[:, 1])

    f = open('poi_irregular', 'r')
    feature = np.zeros((V, C), dtype=float)
    line = f.readline()
    while line:
        rawid, gid, category_code = line.split("\t")
        c = poi_category[category_code[:-1]]
        node_no = int(gid)
        feature[node_no, c] += 1
        line = f.readline()
    f.close()

    N = np.sum(feature)
    n_i = np.tile(np.sum(feature, axis=0), (V, 1))
    R = np.tile(np.sum(feature, axis=1), (C, 1)).transpose()
    feature = n_i / N * np.log(R / feature)

    feature[np.isinf(feature)] = 0
    feature[np.isnan(feature)] = 0
    cls = KMeans(K).fit(feature)
    label = cls.labels_
    center = cls.cluster_centers_
    np.save('irregular_feature.npy', feature)
    np.save('irregular_label.npy', label)

    dict = {}
    labeled_list = []
    sum = np.zeros(K)
    count = np.zeros(K)
    for k in range(K):
        sum[k] = np.sum(label == k)
    for i in range(V):
        dict[i] = np.linalg.norm(center[label[i], :] - feature[i, :])
    sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=False)
    for v in sorted_dict:
        c = label[v[0]]
        if count[c] < np.ceil(sum[c] * 0.8):
            count[c] += 1
            labeled_list.append(v[0])
    L = np.array(labeled_list)
    weight = np.size(L) / count
    weight[np.isinf(weight)] = 0
    np.save('irregular_idx.npy', L)
    np.save('irregular_weight.npy', weight)


if __name__ == "__main__":
    main()
