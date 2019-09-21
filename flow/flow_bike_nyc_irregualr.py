import csv
import numpy as np
import time
import json


def isRayIntersectsSegment(poi, s_poi, e_poi):  # https://www.jianshu.com/p/ba03c600a557
    if s_poi == e_poi:
        return False
    if s_poi[1] == e_poi[1]:
        return False
    if s_poi[1] > poi[1] and e_poi[1] > poi[1]:
        return False
    if s_poi[1] < poi[1] and e_poi[1] < poi[1]:
        return False
    if s_poi[1] == poi[1] and e_poi[1] > poi[1]:
        return False
    if e_poi[1] == poi[1] and s_poi[1] > poi[1]:
        return False
    if s_poi[0] < poi[0] and e_poi[0] < poi[0]:
        return False
    xseg = e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1])
    return xseg >= poi[0]


def isPoiWithinPoly(poi, boundary):
    count = 0
    poly = boundary
    for i in range(len(poly)-1):
        s_poi = poly[i]
        e_poi = poly[i+1]
        if isRayIntersectsSegment(poi, s_poi, e_poi):
            count += 1
    return count % 2 == 1


def main():
    f = open('station_position.txt', 'r')
    a = f.read()
    station_pos = eval(a)
    f = open('irregular_boundary.txt', 'r')
    a = f.read()
    boundary = eval(a)
    station_region = {}
    num_node = len(boundary)
    lng_max = np.zeros(num_node)
    lng_min = np.zeros(num_node)
    lat_max = np.zeros(num_node)
    lat_min = np.zeros(num_node)
    for i in range(num_node):
        boundary_r = np.array(boundary[i])
        lng_max[i], lng_min[i] = np.max(boundary_r[:, 0]), np.min(boundary_r[:, 0])
        lat_max[i], lat_min[i] = np.max(boundary_r[:, 1]), np.min(boundary_r[:, 1])
    for sta, point in station_pos.items():
        lng = float(point[1])
        lat = float(point[0])
        for r in range(num_node):
            if lng_min[r] <= lng <= lng_max[r] and lat_min[r] <= lat <= lat_max[r]:
                if isPoiWithinPoly((lng, lat), boundary[r]):
                    station_region[sta] = r
                    break

    tim_start = int(time.mktime(time.strptime("2017-07-01 00:00:00", "%Y-%m-%d %H:%M:%S")))
    C = 2
    len_t = 24 * (31 + 31 + 30)
    num_node = len(boundary)
    dataset = np.zeros((C, len_t, num_node), dtype=np.float32)
    path = np.zeros((len_t, num_node, num_node), dtype=np.float32)
    for month in range(7, 10):
        f = open('20170' + str(month) + '-citibike-tripdata.csv')
        reader = csv.reader(f)
        header_row = next(reader)
        for row in reader:
            if row[3] in station_region and row[7] in station_region:
                origin = station_region[row[3]]
                dest = station_region[row[7]]
                if origin != dest:
                    start_t = (int(time.mktime(time.strptime(row[1], "%Y-%m-%d %H:%M:%S"))) - tim_start) // 3600
                    end_t = (int(time.mktime(time.strptime(row[2], "%Y-%m-%d %H:%M:%S"))) - tim_start) // 3600
                    if end_t < len_t:
                        dataset[0, end_t, dest] += 1
                        dataset[1, start_t, origin] += 1
                        path[end_t, origin, dest] += 1
                        path[end_t, dest, origin] += 1
    np.save('../path/path_bike_nyc_irregular.npy', path)

    out_data = {}
    out_data['inflow'] = {}
    out_data['outflow'] = {}
    for r in range(dataset.shape[2]):
        out_data['inflow'][r] = dataset[0, :, r].tolist()
        out_data['outflow'][r] = dataset[1, :, r].tolist()
    with open("flow_bike_nyc_irregular.json", 'w', encoding='utf-8') as json_file:
        json.dump(out_data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    main()
