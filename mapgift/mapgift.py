#!/usr/bin/env python
# coding: utf-8

"""
Attribution
-----------
Some of the map designs provided by this program are © Stamen Design, under a Creative Commons Attribution (CC BY 3.0) license:
Map tiles by [Stamen Design](http://stamen.com), under [CC BY 3.0](http://creativecommons.org/licenses/by/3.0).
Data by [OpenStreetMap](http://openstreetmap.org), under [CC BY SA](http://creativecommons.org/licenses/by-sa/3.0).


Input
-----
A KML file downloaded from internet Google Maps (or its web
address). => changed to accept the data *from* the KML file


Output
------
A map image representing these special places, ready to be
sent off to a printing company to be hung on my wall.
It must therefore be high resolution and present the note for
each placemark, all with a good design.


Features
--------
There should be a few map tile styles (basemap providers)
to choose from, as well as different placemark icons and
also overall presentation of the final map image to be
printed. 
I'm toying with the idea of turning this into a semi
web-app project, which will give me practice in coding
with web APIs, and doing web mapping.


How this works
--------------        
It's important to make the distinction between the map instance, and the map image.


Improvements
------------
- Support for other types of geographic data such as in JSON format
    (although I want to keep it limited to placemarks)
- easier & straightforward customisability:
    - map type
    - map provider
    - map colour / inverted colours
    - placemark image / icon
    - placemark colour
    - placemark size
    - map size
    - map area
    - map centre
    - map zoom
    - placemark uniqueness
        - numbering
        - labeling with name ?
    - layout of poster
        eg. map + smaller map w/ viewport + descriptions
- ability to customise this in a logical way
    ie.     "I want to be able to make a 1m*2m poster"
            "I want to see all placemarks"
- add "styles" which offer pre-made selections of above customisation options
    - find "hipster" colours & fonts
    - "glamour" / contrast
    - "handmade": watercolor + handwriting
    etc
- add placemark shadow implementation
- properly organise the MM changes:
    - fork and modify it
    - add a lot of my comments to understand how it works
- implement viewports & details
- implement placemark description
- implement a sort of cache feature to save map backgrounds already done
    so that they can be reused (less "waste" & faster)
- more ways to control script from terminal with sys.argv
- turn it into Object Oriented Program
    - map instance
    - map layers
    - places / placemarks
- put in safety controls based on geographic area covered relatively to zoom level
- predict time it will take to make map image
- figure out why some map styles just won't fetch tiles at certain levels
- more verbose of what's going on
- if the map background in going to be opaque, or you use 2 different map backgrounds,
    it might be better to generate the round placemarks first and then paste them,
    so that a lot of unecessary background isn't made
- implement a grid preview of incrementing changes in 2 customisation options
    ie. like what I did for the images at work


More ideas for map design
-------------------------    
- give it a different style by using circle shapes
    eg. - make a grid of circles of the places
        - show circled placemarks in different map type than map background
            eg. a black map with placemarks "punched through"


Idea for how to organise code
-----------------------------
1.  Draw a few map examples like the ones detailed above.
    Make some very different and very similar ones.
2.  Write step by step code of how to make that map, for each map.
3.  See overlap in functions / objects used.

"""
import re
import os
import sys
import click
import time # to put date in saved images' filename

from helper import makeSwedishDate as sw
from helper import makeSmaller
import providers

import ModestMaps as MM # I had to manually add the Stamen code
from PIL import Image, ImageDraw, ImageFont, ImageOps


MAP_BOX = {
    'central':      ((59.356, 18.000),  (59.303, 18.137)),
    'suburb':       ((59.382, 17.931),  (59.277, 18.206)),
    'wkista':       ((59.434, 17.794),  (59.224, 18.343)),
    'wtyresta':     ((59.539, 17.519),  (59.119, 18.618)),
    'southsweden':  ((62.533, 9.272),   (55.801, 26.851)),
    'sweden':       ((65.422, 0.483),   (51.917, 35.640)),
    'northeurope':  ((70.348, -17.051), (43.005, 53.262)),
    'europe':       ((77.542, -52.207), (20.961, 88.418)),
    'world':        ((85.021, -122.695),(-29.841, 158.555)),

    'stockholm':    ((59.382, 17.931),  (59.277, 18.206)),
    'london':       ((51.535, -0.239),  (51.45,  -0.046)),
    'paris':        ((48.902, 2.241),   (48.810, 2.429)),

    'france':       ((50.345, -8.0454), (41.705, 7.9286)),

}   # 'area_name':  (lat lon of top left corner, lat lon bottom right corner)

CENTRE = {
    'stockholm':    (59.329444, 18.068611),
    'london':       (51.507222, -0.1275),
    'paris':        (48.8567,   2.3508),
    'bath':         (51.3800,   -2.3600),

    'france':       (46.164614, -0.860367),
}

PROVIDERS = {   'osm':        'OPENSTREETMAP',
                # 'watercolor': 'STAMEN_WATERCOLOR', # Stamen changed it to jpg ?? in place of the png in ModestMaps
                'toner':      'STAMEN_TONER',
                'watercolor': providers.StamenWatercolorProvider,
                'lines':      providers.StamenTonerLinesProvider,
                'lite':       providers.StamenTonerLiteProvider,
                'labels':     providers.StamenTonerLabelsProvider,
                'hybrid':     providers.StamenTonerHybridProvider,
                'background': providers.StamenTonerBackgroundProvider,
                'aerial':     'MICROSOFT_AERIAL',
}


def openkml(filename):
    with open(filename, 'r') as kmlfile:
        """
        if kmlfile.info().gettype() == 'text/xml':
            file = kmlfile.read()
        else:
            raise TypeError
        """
        kmldata = kmlfile.read()
    return kmldata


def kml2py(kmldata):
    """
    Converts KML data to usable Python objects.

    kmldata:    An open and read .kml file

    Returns:    A list of Python objects
                [py, py]

                I've chosen to use dictionaries:
                [{'name':name, 'coor': (lat,lon), 'desc': description},
                 {'name':name, 'coor': (lat,lon), 'desc': description}]
    """
    # find all <Placemark>...</Placemark> tags
    match1 = re.findall(r'<Placemark>.*?</Placemark>', kmldata, re.DOTALL)
    # match1 is a list of code

    # find name, description, lat, lon
    # and organise it into a list of dicts
    placemarks = list()
    linestrings = list()
    for i, placemark in enumerate(match1):
        code = placemark.decode('utf-8')
        pldict = dict()

        match = re.search(r'<name>([,\w\s\-]*?)</name>', code, re.UNICODE)
        if match:
            pldict['name'] = match.group(1)
        else:
            pldict['name'] = 'Placemark %d' % i

        match = re.search(r'CDATA\[(<div dir="ltr">)?(.*?)(</div>)?\]\]', code)
        if match:
            pldict['desc'] = match.group(2)
        else:
            pldict['desc'] = ''
    
        # 2 possibilities, either a Point, or a Line
        match = re.search(r'<Point>', code)
        if match:

            match = re.search(r'<coordinates>([-\d\.]+),([-\d\.]+),0', code)
            if match:
                lat = float(match.group(2))
                lon = float(match.group(1))
                pldict['coor'] = (lat,lon)
            else:
                pldict['coor'] = (0.0, 0.0)
        else:
            match = re.search(r'<LineString>', code)
            if match:

                match = re.findall(r'([-\d\.]+),([-\d\.]+),0', code)
                if match:
                    pldict['coor'] = [(float(lat),float(lon)) for lon, lat in match]
                else:
                    pldict['coor'] = [(0.0, 0.0)]

        placemarks.append(pldict)

    return placemarks 


def make_map(provider, area, zoom, by_centre, map_size=(1200,800), verbose=False):
    """
    zoom:   integer, the zoom level (altitude)
            min 12; max 15 in this case

    Returns a map instance (not image!)
    """
    if type(area) in (str, unicode):
        area = area.lower()
    zoom = int(zoom)

    provider = PROVIDERS[provider.lower()]

    if verbose:
        title = 'Making map with the following characteristics:'
        print '\n%s' % title
        print '-' * len(title)
        if type(area) in (str, unicode):
            print 'Area:     %s' % area.title()
        else:
            print 'Area:     %s' % area
        print 'Zoom:     %d' % zoom
        if type(provider) == str:
            print 'Provider: %s' % provider.title().replace('_', ' ')
        else:
            print 'Provider: %s' % provider.__name__
        print 'Height:   %dpx' % map_size[1]
        print 'Width:    %dpx' % map_size[0]
        print

    if type(provider) == str:
        provider = MM.builtinProviders[provider]()
    else: # it must be a custom provider
        provider = provider()

    if by_centre:
        if type(area) in (str, unicode):
            centre = CENTRE[area]
        elif type(area) == tuple:
            centre = area
        width  = map_size[0]
        height = map_size[1]

        m = MM.mapByCenterZoom( provider,
                                MM.Geo.Location(*centre),
                                zoom,
                                MM.Core.Point(width, height))
        if verbose:
            print m.pointLocation(MM.Core.Point(0,0))           # to get the upper left corner geo coordinates
            print m.pointLocation(MM.Core.Point(width,height))  # to get the lower right corner geo coordinates
    
    else: # by box
        if type(area) in (str, unicode):
            map_box = MAP_BOX[area]
        elif type(area) == tuple:
            map_box = area
        left_upper_corner  = MM.Geo.Location(*map_box[0])
        right_lower_corner = MM.Geo.Location(*map_box[1])

        m = MM.mapByExtentZoom( provider,
                                left_upper_corner,
                                right_lower_corner,
                                zoom)
    return m


def draw_map(m, verbose=False):
    """Takes a map instance and 'draws' it by calling all the map tiles and stitching them together."""
    map_image = m.draw(verbose)
    return map_image


def makeLayer(map_image, colour=None):
    """"""
    params = ('RGBA', map_image.size)
    if colour or colour != 'transparent':
        params += (colour,)
    layer = Image.new(*params)
    return layer

###

def nothing(a, x):
    return a

def invert(image, x):
    image = ImageOps.invert(image)
    return image

def grayscale(image, x):
    image = image.convert('L').convert('RGBA')
    return image

def grainyBW(image, x):
    image = image.convert('1').convert('RGBA')
    return image

def brightness(image, x=1.0):
    return image.point(lambda i: i * x)

###

def addNum(image, number, size_param=0.5, colour='black', location=(0,0)):
    """"""
    w, h = image.size
    text_size = int(h*size_param)

    fontpath = '/Library/Fonts/Georgia.ttf'
    font = ImageFont.truetype(fontpath, text_size)

    draw = ImageDraw.Draw(image)
    draw.text(location, str(number), fill=colour, font=font)
    return


def addLabel(image, label, size, loc):
    """"""
    addNum(image, num, 0.02, location=loc)
    return


def addLine(m, image, coordinates, num, placemark_params):
    """"""
    thickness, colour = placemark_params[1:]
    if not colour or colour == 'transparent':
        colour = (255, 0, 0, 0)

    points = list()
    for coor in coordinates:
        loc  = MM.Geo.Location(*coor)
        loc  = m.locationPoint(loc)
        x, y = loc.x, loc.y
        points.append((x,y))

    draw = ImageDraw.Draw(image)
    draw.line(points, fill=colour, width=thickness)
    return


def addCircle(image, loc, placemark_params, num):
    """
    d:  integer, the diametre of the placemark circle to draw
    """
    d, colour = placemark_params[1:]
    if not colour or colour == 'transparent':
        colour = (255, 0, 0, 0)

    x, y = loc

    r = d/2
    w, h = d, d

    draw = ImageDraw.Draw(image)
    circle_box = (x-r, y-r, x-r+w, y-r+h)
    draw.ellipse(circle_box, fill=colour)
    return


def addPlacemarkImage(map_image, placemark_image, loc, placemark_params):
    """"""
    size, colour = placemark_params[1:]
    mask = Image.open(placemark_image)
    mask = makeSmaller(mask, size)
    w, h = mask.size
    x, y = loc
    loc = (int(x-w/2), int(y-h))
    background = Image.new('RGBA', (w, h), colour)
    map_image.paste(background, loc, mask)
    return


def addPlacemarkXY(image, loc, num, placemark_params):
    """"""
    placemark_type = placemark_params[0]
    # should have a function for size of placemark relative to size of map images
    if placemark_type == 'circle':
        addCircle(image, loc, placemark_params, num)
    elif placemark_type == 'image':
        addPlacemarkImage(image, 'heart.png', loc, placemark_params)
    return

def addPlacemark(m, image, coor, num, placemark_params):
    """"""
    loc  = MM.Geo.Location(*coor)
    loc  = m.locationPoint(loc)
    # should add code to Core.Point so that I can unpack it like a tuple
    # TypeError: iteration over non-sequence
    x, y = loc.x, loc.y

    addPlacemarkXY(image, (x,y), num, placemark_params)
    return


def addPlacemarks(m, image, placemarks, placemark_params, verbose=False):
    """"""
    for i, pldict in enumerate(placemarks, 1):
        coordinates = pldict['coor']
        if type(coordinates) == tuple:
            addPlacemark(m, image, coordinates, i, placemark_params)
        elif type(coordinates) == list:
            # could implement this recursively ?
            for i, p in enumerate(coordinates):
                addPlacemark(m, image, p, i, placemark_params)
            if len(coordinates) < 30:
                addLine(m, image, coordinates, i, placemark_params)
        else:
            pass # problem
        if verbose:
            print '%d Added - %s - to the map.' % (i, pldict['name'])
    return


def addLayer(image, layer, mask=None):
    """"""
    if not mask:
        mask = layer
    image.paste(layer, (0,0), mask)
    return image


def save_map(m, filename='map', inc_date=True, verbose=False):
    """"""
    if inc_date:
        filename += str(sw(time.localtime()))
    filename += '.png'
    m.save(filename)
    if verbose:
        print 'Image saved to %s' % filename
    return


def assembleMap(map_type, area, zoom, by_centre, placemark_params, kmlfile, verbose=False):
    """"""
    map1, map2 = map_type

    map_inst  = make_map(map1, area, int(zoom), by_centre=by_centre)
    map_image = draw_map(map_inst, verbose)
    """
    if map_type in ['lines', 'labels', 'lite']:
        map_image = invert(map_image)
    """

    # map for the placemark circles
    if map1 != map2:
        map2_inst  = make_map(map2, area, int(zoom), by_centre=by_centre)
        map2_image = draw_map(map2_inst, verbose)
    elif map1 == map2:
        map2_image = map_image.copy()

    # makes a black background with holes in it for the placemark locations
    placemark_layer = makeLayer(map_image, 'black')
    if kmlfile[-3:] == 'kml':
        kmlfile = os.path.join('kml_files', kmlfile)
        kmldata = openkml(kmlfile)
    else:
        kmldata = kmlfile
    places = kml2py(kmldata)
    addPlacemarks(map_inst, placemark_layer, places, placemark_params)

    # makes a placemark mask
    placemark_mask = makeLayer(map_image, None)
    addPlacemarks(map_inst, placemark_mask, places, placemark_params[:-1]+('black',))

    # add placemark layer to the second map which will be the layer to the first map
    layer = addLayer(map2_image, placemark_layer)

    # add effects to map layers
    effect1 = brightness, 0.6
    effect2 = nothing, None

    def applyFilter(image, filter, x):
        return filter(image, x)

    # add layer to the background map
    map_image = addLayer(applyFilter(map_image, *effect1), applyFilter(layer, *effect2), placemark_mask)

    return map_image


def addViewport(map1, map_image, map2, thickness=1, colour='black', params=None):
    """
    map1:   instance of Map, the higher altitude map on which the viewport is pasted
    map2:   instance of Map, the lower altitude map
            or
            2-value tuple,  the viewport coordinates
                            it contains 2 2-value tuples:
                            (left_upper_corner, right_lower_corner)
                            eg. ((lat1, lon1), (lat2, lon2))

    Improvements
    ------------
    Ugh, really don't like the global viewport variable thing
    What if I want to have 2 viewports ? Ok, it works.
    Still, it feels meh, maybe reduce and/or map would have been cleaner.
    """
    if type(map2) != tuple:
        pass
        # find the geographical coordinates of the map2 (ie the viewport)

    left_upper, right_lower = map2
    right_upper = left_upper[0], + right_lower[1],
    left_lower  = right_lower[0], + left_upper[1],

    box = [left_upper, right_upper, right_lower, left_lower]

    # find the equivalent x,y coordinates of the viewport on the map image of map1
    global viewport
    viewport = [map1.locationPoint(MM.Geo.Location(*coor)) for coor in box]
    viewport = [tuple(map(int, (point.x, point.y))) for point in viewport]
    viewport += viewport[0],

    def bigger(rectangle, recursion):
        if recursion == 1:
            return rectangle
        left_upper, right_upper, right_lower, left_lower = rectangle[:-1]
        left_upper  = ( left_upper[0]-1,  left_upper[1]-1)
        right_upper = (right_upper[0]+1, right_upper[1]-1)
        right_lower = (right_lower[0]+1, right_lower[1]+1)
        left_lower  = ( left_lower[0]-1,  left_lower[1]+1)

        new = (left_upper, right_upper, right_lower, left_lower, left_upper)
        global viewport
        viewport += new
        return bigger(new, recursion-1)

    bigger(viewport, thickness)

    # draw the viewport
    draw = ImageDraw.Draw(map_image)
    draw.line(viewport, fill=colour)

    return map_image


def main(map_provider, area, zoom, by_centre, kmlfile,
         ofilepath=None, verbose=False, show=False, interactive=False):
    """"""
    placemark_params = ('circle', 20, 'transparent')

    ## m is a map instance
    m = make_map(map_provider, area, zoom, by_centre, verbose=verbose)

    if not kmlfile:
        img = draw_map(m)
    else:
        img = assembleMap((map_provider, map_provider), area, zoom, by_centre, placemark_params, kmlfile)

    if ofilepath:
        save_map(img, filename=ofilepath, inc_date=True, verbose=verbose)

    if show:
        img.show()

    if interactive:
        from code import interact; interact(local=dict( globals(), **locals() ))

    # img = addViewport(m, img, MAP_BOX['central'], 5)
    # img = addViewport(m, img, MAP_BOX['wKista'], 10)
    return img


@click.command()
@click.option('map_provider',  '-p', '--provider',    default='osm',
                                                        # type=click.Choice(['osm', 'watercolor', 'toner', 'lines', 'lite', 'labels']),
                                                        help='Name of map tile provider.')
@click.option('area',          '-a', '--area',        prompt='Area',
                                                        help='Name of area.')
@click.option('zoom',          '-z', '--zoom',        default=10,
                                                        type=click.IntRange(7, 16, clamp=True),
                                                        help='Zoom level.')
@click.option('by_centre',     '-c', '--by-centre',   default=False,
                                                        help='Whether area coordinates are interpreted as the centre.')
@click.option('kmlfile',       '-k', '--kmlfile',     default=None,
                                                        type=click.Path(exists=False),
                                                        help='Output filepath.')
@click.option('ofilepath',     '-o', '--ofilepath',   default=None,
                                                        type=click.Path(exists=False),
                                                        help='Output filepath.')
@click.option('verbose',       '-v', '--verbose',     default=False, is_flag=True,
                                                        help='Verbosity.')
@click.option('show',          '-s', '--show',        default=False, is_flag=True,
                                                        help='Show map.')
@click.option('interactive',   '-i', '--interactive', default=False, is_flag=True,
                                                        help='Opens interactive console at end of script to play with map.')
def cli(*args, **kwargs):
    return main(*args, **kwargs)


if __name__ == '__main__':

    # for quick access
    paris_params     = ('toner',      'Paris',  14, False, 'SummerinParis.kml')
    stockholm_params = ('watercolor', 'suburb', 14, False, 'JustineandNicoleinStockholm.kml')
    london_params    = ('lite',       'London', 15, False, 'Imperialyears.kml')

    test_params      = ('osm',        'London', 15, False, 'Imperialyears.kml')

    sys.exit(cli())











