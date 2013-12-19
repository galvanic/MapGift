from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from mapg.models import Map, Placemark
from django.utils import timezone

import sys
sys.path.append("/Users/jc5809/Dropbox/Programming/Projects/MapGift")
import mapgift

# Create your views here.

def update_map_list():
    map_list = Map.objects.order_by('-pub_date')
    context = { 'map_list': map_list,
                'next_map_id': len(map_list)+1,
                'providers': mapgift.PROVIDERS,
                }
    return context


def index(request):
    return render(request, 'mapg/index.html', update_map_list())

def archive(request):
    return render(request, 'mapg/archive.html', update_map_list())

def assemble(request, map_id):
    # if there are no values or the values don't work, use default ones, for the moment, should re-ask at least location
    try:
        where  = request.POST['where'].title()
        zoom   = int(request.POST['zoom'])
        design = request.POST['design']
        m = Map(
            area_name = where,
            zoom = zoom,
            map_provider = design,
            pub_date = timezone.now()
            )
        m.save() # add map to the database
        m_img = mapgift.main(map_provider=design, area_name=where, zoom=zoom)
    except Exception:
        return render(request, 'mapg/index.html', update_map_list())
    else:
        # ok this url is a disaster, wtf
        mapgift.saveMap(m_img, "/Users/jc5809/Dropbox/Programming/Projects/MapGift/mysite/mapg/static/mapg/images/map_images/", "map"+str(map_id), False, True)

    return HttpResponseRedirect(reverse('mapg:detail', args=(map_id, )))

def detail(request, map_id):
    m = get_object_or_404(Map, pk=map_id)
    return render(request, 'mapg/detail.html', {'map': m})


# There's still the generic views part of the Django tutorial part 4 left, but it works for the moment so I'll change that later