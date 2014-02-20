#OpenData @ TEC

As you may know, the TEC are opening up their data. Sadly, they are providing it [here](http://geoportail.wallonie.be/geocatalogue?search-theme=theme_30&search-subtheme=soustheme_3040) in a ESRI Shapefile format.
To allow developpers and open data enthusiasts to play with it, I wrote a simple python script that read the files and generate
json and GTFS files.

You need two dependencies in order to run the extract.py script (one to read shapefiles and the other to translate Lambert to 
WGS84).

You can install them with pip : 

```
pip install pyshp
pip install pyproj
```

#JSON files

### stops.json
Contains all the TEC stops in this format 
```
[
{
"id" : 3724,
"name" : 'RECOGNE Big Mat'
"lat" : 3.173342,
"lon" : 51.282530
},
...
]
```

### lines.json
Contains all the lines provided by the TEC in this format
```
[
	{
		"xid": "1", 
		"id": "BE.TEC.B1",
		"name": "Jodoigne - Louvain-la-Neuve - Ottignies"	
		"type" : "B",	
		"points" : [
			{"lat": 4.876579285263261, "lon": 50.72327969107735, "seq": 0},
			...
		]	
	},
	...
]
```

#GTFS feed

You can find information about GTFS [here](https://developers.google.com/transit/gtfs/). The extract.py script create these files : 
* [agency.txt](https://github.com/QKaiser/tec-opendata/blob/master/agency.txt) (information about the TEC)
* [stops.txt](https://github.com/QKaiser/tec-opendata/blob/master/stops.txt)  (information about the stops)
* [routes.txt](https://github.com/QKaiser/tec-opendata/blob/master/routes.txt) (information about the lines)
* [shapes.txt](https://github.com/QKaiser/tec-opendata/blob/master/shapes.txt) (shape containing all points related to a specific line)

#TODO

The stops names provided by the TEC contains the locality AND the street name. Could be nice to find the ultimate regex to separate these in
two different attributes for enhanced filtering.

Feel free to comment or file an issue.


