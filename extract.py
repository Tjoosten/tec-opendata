#!/bin/python
# Convert TEC shapefile to json files 

import shapefile
import pyproj
import json
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 

wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
lambert = pyproj.Proj('+proj=lcc +lat_1=51.16666723333333 +lat_2=49.8333339 +lat_0=90 +lon_0=4.367486666666666 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.8686,52.2978,-103.7329,-0.3366,0.457,-1.8422,-1.2747 +units=m +no_defs')

shp_stops = shapefile.Reader('Poteaux_2013_12')
shp_lines = shapefile.Reader('LGN_2013_12')
stops = []
lines = []
i=0

for s, name in zip(shp_stops.shapes(), shp_stops.records()):
	name = [x.decode('iso-8859-15').encode('utf-8') for x in name]
	x, y = pyproj.transform(lambert, wgs84, s.points[0][1], s.points[0][0])
	stops.append({'id' : i, 'name' : name[0], 'lon' : y, 'lat' : x})
	i+=1

for name, line in zip(shp_lines.records(), shp_lines.shapes()):
	points = []
	name = [x.decode('iso-8859-15').encode('utf-8') for x in name]
	i = 0
	for point in line.points:
		x, y = pyproj.transform(lambert, wgs84, point[0], point[1])
		points.append({"seq" : i, "lat" : x, "lon" : y})
		i+=1
	lines.append({"id" : "BE.TEC.%s"%(name[0]), "name" : name[1], "xid" : name[2], "type" : name[3], "points" : points})

	print json.dumps(lines)
	break

with open('stops.json', 'w') as f:
	f.write(json.dumps(stops, ensure_ascii=False))

with open('lines.json', 'w') as f:
	f.write(json.dumps(lines, ensure_ascii=False))

with open('agency.txt', 'w') as f:
	f.write('agency_id,agency_name,agency_url,agency_timezone\nTEC,Transport En Commun,http://www.infotec.be,Europe/Brussels\n')

with open('stops.txt', 'w') as f:
	f.write('stop_id,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url\n')
	for stop in stops:
		f.write('%s,%s,,%f,%f,,\n'%(stop['id'], stop['name'], stop['lat'], stop['lon']))

with open('routes.txt', 'w') as f:
	f.write('route_id,route_short_name,route_long_name,route_desc,route_type\n')
	for line in lines:
		f.write('BE.TEC.%s, %s, %s,, %s\n'%(line['id'], line['xid'], line['name'],line['type']))

with open('shapes.txt', 'w') as f:
	f.write('shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled\n')
	for line in lines:
		distance = 0
		ppoint = line['points'][0]		
		for point in line['points']:
			distance += haversine(ppoint['lon'], ppoint['lat'], point['lon'], point['lat'])		
			f.write('BE.TEC.%s,%f,%f,%d,%f\n'%(line['id'], point['lat'], point['lon'], point['seq'], distance))
			ppoint = point


