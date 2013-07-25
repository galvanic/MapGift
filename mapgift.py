# coding: utf-8
"""
A project based on Nicole's present to me for my departure from Sweden.

Input	A KML file downloaded from internet Google Maps (or its web
		address).
		It is a list of placemarks each representing a special place
		for Nicole and I.

Output	A map image representing these special places, ready to be
		sent off to a printing company to be hung on my wall.
		It must therefore be high resolution and present the note for
		each placemark, all with a good design.

Features	There should be a few map tile styles (not sure what the
			correct vocabulary is) to choose from, as well as different
			placemark icons and also overall presentation of the final
			map image to be printed. 
			I'm toying with the idea of turning this into a semi
			web-app project, which will give me practice in coding
			with web APIs, and doing web mapping.

Future Improvements ?	Support for other type of Geo data such as JSON
						.
		
"""
import re

# First, I need to convert the Geo data into Python objects I can use

KMLfile = "JustineandNicoleinStockholm.kml"


def kml2py(filename):
	"""
	Converts KML data to usable Python objects.

	filename:	A .kml file

	Returns:	A list of Python objects
				[py, py]

				I've chosen to use dictionaries:
				[{'name':name, 'coor': (lat,lon), 'desc': description},
				{'name':name, 'coor': (lat,lon), 'desc': description}]
	"""
	with open(filename, "r") as kmlfile:
		"""
		if kmlfile.info().gettype() == 'text/xml':
			file = kmlfile.read()
		else:
			raise TypeError
		"""
		file = kmlfile.read()

	# find all <Placemark>...</Placemark> tags
	match1 = re.findall(r'<Placemark>.*?</Placemark>', file, re.DOTALL)
	# match1 is a list of code

	# find name, description, lat, lon
	# and organise it into a list of dicts
	placemarks = list()
	for placemark in match1:
		code = placemark.decode('utf-8')
		pldict = dict()

		match = re.search(r'<name>([,\w\s\-]*?)</name>', code, re.UNICODE)
		pldict['name'] = match.group(1)

		match = re.search(r'CDATA\[(<div dir="ltr">)?(.*?)(</div>)?\]\]', code)
		pldict['desc'] = match.group(2)
		
		match = re.search(r'<coordinates>([\d\.]+),([\d\.]+),0', code)
		lat = float(match.group(2))
		lon = float(match.group(1))
		pldict['coor'] = (lat,lon)

		placemarks.append(pldict)

	return placemarks 



import ModestMaps as MM	# I had to manually add the Stamen code
import ImageDraw

def makeMap(provider):
	
	shortcuts = {	'osm': 'OPENSTREETMAP',
					'stamen': 'STAMEN_WATERCOLOR'}
	provider = shortcuts[provider.lower()]

	provider = MM.builtinProviders[provider]()
	zoom 	 = 12
	centre	 = (59.329444, 18.068611)	# lat (north), long (east)
	width	 = 800
	height	 = 600

	m = MM.mapByCenterZoom(	provider,
							MM.Geo.Location(*centre),
							zoom,
							MM.Core.Point(width, height))
	return m


def drawMap(m):
	map_image = m.draw(verbose=False)
	return map_image


def addPlacemark(m, image, coor):
	loc  = MM.Geo.Location(*coor)
	loc  = m.locationPoint(loc)
	# should add code to Core.Point so that I can unpack it like a tuple
	# TypeError: iteration over non-sequence
	x, y = loc.x, loc.y

	w, h = 5, 5
	draw = ImageDraw.Draw(image)
	draw.ellipse((x, y, x+w, y+h), fill="black")
	return


def addAllPlaces(m, image, placemarks, verbose=False):
	for i, pldict in enumerate(placemarks, 1):
		coor = pldict['coor']
		addPlacemark(m, image, coor)
		if verbose:
			print i, "Added -", pldict['name'], "- to the map."
	return


def saveMap(m, filename="map.png"):
	m.save(filename)
	return


if __name__ == "__main__":

	map_inst  = makeMap('stamen')
	map_image = drawMap(map_inst)

	places = kml2py(KMLfile)
	addAllPlaces(map_inst, map_image, places)

	saveMap(map_image)













