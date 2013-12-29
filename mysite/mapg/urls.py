from django.conf.urls import patterns, url
from mapg import views

urlpatterns = patterns("",
    url(r'^$', views.index, name='index'),
    # ex: /mapg/archive/
    url(r'^archive/$', views.archive, name='archive'),
    # ex: /mapg/5/assemble/
    url(r'^(?P<map_id>\d+)/assemble/$', views.assemble, name='assemble'),
    # ex: /mapg/5/
    url(r'^(?P<map_id>\d+)/$', views.detail, name='detail'),
)