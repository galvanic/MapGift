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

	- **osm**: Open Street Map
	- watercolor: Stamen Watercolor *currently unavailable*
	- **toner**: Stamen Toner
	- lines: Stamen Lines *currently unavailable*
	- lite: Stamen Lite *currently unavailable*
	- labels: Stamen Labels *currently unavailable*

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
- Fix other map tile providers and add others
- New design for front-end
- Turn `mapgift.py` into a full module