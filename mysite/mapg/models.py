from django.db import models

# Create your models here.

# The model would be each map being made ? With the url image I guess
# Maybe recording details about it, so that I can run analytics on that later ? Not directly useful to the app though

class Map(models.Model):
    area_name = models.CharField(max_length=20)
    zoom = models.IntegerField()
    map_provider = models.CharField(max_length=20)
    # kmlfile = models.FileField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.area_name

# maybe then add a class for the pins ? What about the viewport(s) ? the layers/filters/effects ?

class Placemark(models.Model):
    on_map = models.ForeignKey(Map)
    latitude = models.FloatField()
    longitude = models.FloatField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __unicode__(self):
        return self.title

# m = Map(area_name="London", zoom=12, map_provider="Stamen", pub_date=timezone.now())