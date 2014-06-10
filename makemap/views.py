from django.shortcuts          import render, get_object_or_404
from django.http               import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers  import reverse
from django.utils              import timezone

from django.core.files.storage import default_storage
from django.core.files.base    import ContentFile

from makemap.models import Map, KMLfile
import mapgift

import cStringIO

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import boto
from boto.s3.key        import Key
from boto.s3.connection import S3Connection

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


def send_image_s3(img_file, image_filename):
    conn   = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket("map-images-jc")
    k      = Key(bucket)
    k.key  = image_filename
    k.set_contents_from_string(img_file.getvalue())
    k.make_public()
    return


def update_map_list():
    map_list = Map.objects.order_by('-pub_date')
    context = { 'map_list': map_list,
                'next_map_id': len(map_list)+1,
                'providers': mapgift.PROVIDERS,
                }
    return context


# Create your views here.


def index(request):
    return render(request, 'makemap/index.html', update_map_list())


def archive(request):
    return render(request, 'makemap/archive.html', update_map_list())


def assemble(request, map_id):

    ## get all info from the form in the index page
    design = request.POST["design"]
    zoom   = int(request.POST["zoom2"])
    coord  = request.POST["coord"]
    coord  = tuple(map(float, coord.split(", ")))
    if request.FILES:
        kmlfile = request.FILES["placemarks"].read()   # need to do verification on this!
    else:
        kmlfile = ""

    m_img = mapgift.main(map_provider=design, area=coord, zoom=zoom, by_centre=True, kmlfile=kmlfile)
    
    ## send image off to be stored in S3 through boto
    m_img_file = cStringIO.StringIO()
    m_img.save(m_img_file, "PNG")
    map_name = "map%s.png" % str(map_id)
    send_image_s3(m_img_file, map_name)
    del m_img, m_img_file

    ## save in the database
    where = ", ".join(map(str, coord))
    m = Map(
        area_name    = where, # should reverse geolocalise this to get an actual name
        zoom         = zoom,
        map_provider = design,
        pub_date     = timezone.now()
    )
    m.save()

    return HttpResponseRedirect(reverse('makemap:detail', args=(map_id, )))


def detail(request, map_id):
    m = get_object_or_404(Map, pk=map_id)
    return render(request, 'makemap/detail.html', {'map': m})


