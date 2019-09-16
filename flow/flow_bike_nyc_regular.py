import csv
import numpy as np
import time
import json


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
    return str(refined_lng_traj) + '-' + str(refined_lat_traj)


def main():
    f = open('station_position.txt', 'r')
    a = f.read()
    station_pos = eval(a)
    station_grid = {}
    H = 16
    W = 8
    num_node = H * W
    for sta, point in station_pos.items():
        lng = float(point[1])
        lat = float(point[0])
        grid_str = transfer_lnglat_to_key(lng, lat)
        w, h = int(grid_str[0]), int(grid_str[2:])
        node_no = w - 1 + W * (16 - h)
        if 0 <= node_no < num_node:
            station_grid[sta] = node_no

    tim_start = int(time.mktime(time.strptime("2017-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
    C = 2
    len_t = 24 * (31 + 31 + 30)
    dataset = np.zeros((C, len_t, num_node), dtype=np.float32)
    path = np.zeros((len_t, num_node, num_node), dtype=np.float32)
    for month in range(7, 10):
        f = open('20170' + str(month) + '-citibike-tripdata.csv')
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if row[3] in station_grid and row[7] in station_grid:
                origin = station_grid[row[3]]
                dest = station_grid[row[7]]
                if origin != dest:
                    start_t = (int(time.mktime(time.strptime(row[1], "%Y-%m-%d %H:%M:%S"))) - tim_start) // 3600
                    end_t = (int(time.mktime(time.strptime(row[2], "%Y-%m-%d %H:%M:%S"))) - tim_start) // 3600
                    if end_t < len_t:
                        dataset[0, end_t, dest] += 1
                        dataset[1, start_t, origin] += 1
                        path[end_t, origin, dest] += 1
                        path[end_t, dest, origin] += 1
    np.save('../path/path_bike_nyc_regular.npy', path)

    out_data = {}
    out_data['inflow'] = {}
    out_data['outflow'] = {}
    for r in range(dataset.shape[2]):
        out_data['inflow'][r] = dataset[0, :, r].tolist()
        out_data['outflow'][r] = dataset[1, :, r].tolist()
    with open("flow_bike_nyc_regular.json", 'w', encoding='utf-8') as json_file:
        json.dump(out_data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
