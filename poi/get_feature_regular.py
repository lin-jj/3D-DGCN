import numpy as np
from sklearn.cluster import KMeans


earth_radius = 6378137.0
pi = 3.1415926535897932384626
meter_per_degree = earth_radius * pi / 180.0
GRID_SIZE = 1000.0  # The length of the grid (meter)
lng_l, lng_r = -74.03, -73.92  # Boundary of the city
lat_b, lat_u = 40.656, 40.80
lat_step = GRID_SIZE / 111000
ratio = np.cos((lat_b + lat_u) * np.pi / 360)
lng_step = lat_step / ratio


def transfer_lnglat_to_key(lng, lat):
    refined_lng_traj = np.floor((lng - lng_l) / lng_step).astype(np.int32)
    refined_lat_traj = np.floor((lat - lat_b) / lat_step).astype(np.int32)
    return str(refined_lng_traj) + ',' + str(refined_lat_traj)


def main():
    H = 16
    W = 8
    V = H * W
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

    f = open('poi_regular', 'r')
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
    n_i = np.tile(np.sum(feature[:, 0:C], axis=0), (V, 1))
    R = np.tile(np.sum(feature[:, 0:C], axis=1), (C, 1)).transpose()
    feature = n_i / N * np.log(R / feature)

    feature[np.isinf(feature)] = 0
    feature[np.isnan(feature)] = 0
    cls = KMeans(K).fit(feature)
    label = cls.labels_
    center = cls.cluster_centers_
    np.save('regular_feature.npy', feature)
    np.save('regular_label.npy', label)

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
        k = label[v[0]]
        if count[k] < np.ceil(sum[k] * 0.8):
            count[k] += 1
            labeled_list.append(v[0])
    L = np.array(labeled_list)
    weight = np.size(L) / count
    weight[np.isinf(weight)] = 0
    np.save('regular_idx.npy', L)
    np.save('regular_weight.npy', weight)


if __name__ == "__main__":
    main()
