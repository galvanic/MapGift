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
For the moment, I haven't implemented a proper CLI for the mapgift.py script, so you will have to manually change the options for your desired map in the file itself, by changing the values in the `test_param` tuple.

```shell
./mapgift.py
```

Future improvements
-------------------
- Fix other map tile providers and add others
- Implement CLI for mapgift.py
- New design for front-end