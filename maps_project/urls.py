from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
    url(r'^admin/', include(admin.site.urls)),

    url(r'^makemap/', include('makemap.urls', namespace="makemap")),
    url(r'^$', include('makemap.urls')),
)
