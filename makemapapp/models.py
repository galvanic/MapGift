from django.db import models

"""
I haven't connected the 2 yet.
But the KML files should in the future be connected to 
the maps by a KML file can have multiple maps and a map 
can have mulitple maps.
This is simpler for the moment than looking at individual
placemarks and paths.
"""

class Map(models.Model):
    area_name    = models.CharField(max_length=20)
    zoom         = models.IntegerField()
    map_provider = models.CharField(max_length=20)
    pub_date     = models.DateTimeField("date published")
    def __unicode__(self):
        return self.area_name

class KMLfile(models.Model):
    filename      = models.FileField(upload_to="kml_files")
    date_uploaded = models.DateField("date uploaded")
    def __unicode__(self):
        return self.filename
