from django.contrib import admin

# Register your models here.

from makemapapp.models import Map, KMLfile

admin.site.register(Map)
admin.site.register(KMLfile)