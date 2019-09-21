import numpy as np


def read_from_text(file):
    for line in file:
        yield line.strip('\r\n')


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
    f = open('../flow/irregular_boundary.txt', 'r')
    a = f.read()
    boundary = eval(a)
    region_num = len(boundary)
    lng_max = np.zeros(region_num)
    lng_min = np.zeros(region_num)
    lat_max = np.zeros(region_num)
    lat_min = np.zeros(region_num)
    for r in range(region_num):
        boundary_r = np.array(boundary[r])
        lng_max[r], lng_min[r] = np.max(boundary_r[:, 0]), np.min(boundary_r[:, 0])
        lat_max[r], lat_min[r] = np.max(boundary_r[:, 1]), np.min(boundary_r[:, 1])
    fin = open('poi_info.txt', 'r', encoding='utf-8')
    f = open('poi_irregular', 'w')
    for line in read_from_text(fin):
        if len(line) < 35:
            continue
        rawid, lat, lng, category, name = line.split(',')[0:5]
        lng, lat = float(lng), float(lat)
        for r in range(region_num):
            if lng_min[r] <= lng <= lng_max[r] and lat_min[r] <= lat <= lat_max[r]:
                if isPoiWithinPoly((lng, lat), boundary[r]):
                    f.write(str('\t'.join([rawid, str(r), category])) + '\n')
                    break
    f.close()
    fin.close()


if __name__ == "__main__":
    main()
