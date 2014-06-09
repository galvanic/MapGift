from django.conf.urls import patterns, url

from makemap import views


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),

    # ex: /makemap/archive/
    url(r'^archive/$', views.archive, name='archive'),

    # ex: /makemap/5/assemble/
    url(r'^(?P<map_id>\d+)/assemble/$', views.assemble, name='assemble'),

    # ex: /makemap/5/
    url(r'^(?P<map_id>\d+)/$', views.detail, name='detail'),
    
)