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

# First, I need to convert the Geo data into Python objects I can use

KMLfile = "JustineandNicoleinStockholm.kml"

def kml2py(file):
	"""
	Converts KML data to usable Python objects.

	file:	A .kml file

	Returns:	A list of Python objects
				[py, py]
	"""
	# I'm not sure what will be useful in the data
	# I don't know what sort of Python object to turn it to
	return

# 


if __name__ == "__main__":
	pass