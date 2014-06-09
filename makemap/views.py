from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from makemap.models import Map, KMLfile
import mapgift

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
# AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# S3_BUCKET = os.environ.get('S3_BUCKET_NAME')


def send_image_s3(saved_to, image_filename):
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(S3_BUCKET)
    k = Key(bucket)
    k.key = image_filename
    k.set_contents_from_filename(saved_to+image_filename)
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

    design = request.POST["design"]
    zoom   = int(request.POST["zoom2"])
    coord  = request.POST["coord"]
    coord  = tuple(map(float, coord.split(", ")))
    if request.FILES:
        kmlfile = request.FILES["placemarks"].read()   # need to do verification on this!
    else:
        kmlfile = ""

    m_img = mapgift.main(map_provider=design, area=coord, zoom=zoom, by_centre=True, kmlfile=kmlfile)
    
    save_to = os.path.join(BASE_DIR, 'static/makemap/images/map_images/')
    map_name = "map"+str(map_id)
    mapgift.saveMap(m_img, save_to, map_name, False, True)
    del m_img
    map_name += ".png"

    # send image off to be stored in S3 through boto
    send_image_s3(save_to, map_name)

    os.remove(save_to+map_name)

    where = ", ".join(map(str, coord))
    m = Map(
        area_name = where,
        zoom = zoom,
        map_provider = design,
        pub_date = timezone.now()
        )
    m.save() # add map to the database

    return HttpResponseRedirect(reverse('makemap:detail', args=(map_id, )))


def detail(request, map_id):
    m = get_object_or_404(Map, pk=map_id)
    return render(request, 'makemap/detail.html', {'map': m})


