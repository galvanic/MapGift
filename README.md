Mapgift
=======

Overview
--------
Make a customized map with placemarks from a KML file.

Installation
------------
The modules necessary to run this program are in `requirements.txt`. If you are only interested in the command line interface to make the custom maps, you will need only the [python port](https://github.com/stamen/modestmaps-py) of [Modest Maps](https://modestmaps.com) and [Pillow](https://pypi.python.org/pypi/), a fork of the [Python Image Library](https://effbot.org/imagingbook/pil-index.htm).

The <folder to clone to> is the folder in which all scripts of the program will be put.

```shell
git clone https://github.com/Galvanic/MapGift.git <path of folder to clone to>
cd <folder path cloned to>
sudo pip install pillow
sudo pip install modestmaps
./mapgift.py
```

Getting Started
---------------

**mapgift.py** takes the following flags:

- **-p** map tile provider; choose from:

	- **osm**: [OpenStreetMap](http://www.openstreetmap.org/about)
	- **aerial**: [Microsoft Bing Aerial Maps](http://www.microsoft.com/maps/product/features.aspx)
	- the beautiful map tiles made by [Stamen Design](http://stamen.com/) (see [Attribution](#attribution) below):

		- **watercolor**: [Stamen Watercolor](http://maps.stamen.com/watercolor/)
		- **toner**: [Stamen Toner](http://maps.stamen.com/toner/)
		- **lines**: [Stamen Toner Lines](http://maps.stamen.com/toner-lines/)
		- **lite**: [Stamen Toner Lite](http://maps.stamen.com/toner-lite/)
		- **labels**: [Stamen Toner Labels](http://maps.stamen.com/toner-labels/)
		- **hybrid**: [Stamen Toner Hybrid](http://maps.stamen.com/toner-hybrid/)
		- **background**: [Stamen Toner Background](http://maps.stamen.com/toner-background/)

	- Add your own by implementing a `Provider` class in the `providers.py` and adding it to the `PROVIDER` dictionary inside `mapgift.py`

- **-a** area name or coordinates
- **-z** zoom level (from 1 to 18 technically but here limited from 4 to 15)
- **-c** whether to interpret area coordinates as centre or not
- **-k** filepath of kmlfile to use, if at all
- **-o** output filepath, without the extension
- **-v** verbosity
- **-s** shows the map with your system's default preview application
- **-i** opens an interactive shell in the local environment

For example:

```shell
mapapp/mapgift.py -vsi -a london -p toner -z 12
```

Future improvements
-------------------
- make an admin page to delete maps
	- or learn how to do it so that it sends right away (eg. deleting on pocket)
- preview of map tile style on mouseover of 'design' form options
- change javascript map provider
- refactor `mapgift.py` module
- implement a lot more control over placemarks, more fine tuning
- responsive design (esp for showing archive page on phone)


Attribution
-----------
Some of the map designs provided by this program are © Stamen Design, under a Creative Commons Attribution (CC BY 3.0) license:
Map tiles by [Stamen Design](http://stamen.com), under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0).
Data by [OpenStreetMap](http://openstreetmap.org), under [CC BY SA](http://creativecommons.org/licenses/by-sa/3.0).