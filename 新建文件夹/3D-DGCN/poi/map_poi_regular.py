import numpy as np


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


def read_from_text(file):
    for line in file:
        yield line.strip('\r\n')


def main():
    fin = open('poi_info.txt', 'r', encoding='utf-8')
    f = open('poi_regular', 'w')
    H = 16
    W = 8
    num_node = H * W
    for line in read_from_text(fin):
        if len(line) < 35:
            continue
        rawid, lat, lng, category, name = line.split(',')[0:5]
        lng, lat = float(lng), float(lat)
        grid_str = transfer_lnglat_to_key(lng, lat)
        w, h = grid_str.split(',')
        node_no = int(w) - 1 + W * (16 - int(h))
        if 0 <= node_no < num_node:
            f.write(str('\t'.join([rawid, str(node_no), category])) + '\n')
    f.close()
    fin.close()


if __name__ == "__main__":
    main()
