from django.db import models

# Create your models here.

class Map(models.Model):
    area_name    = models.CharField(max_length=20)
    zoom         = models.IntegerField()
    map_provider = models.CharField(max_length=20)
    pub_date     = models.DateTimeField("date published")
    def __unicode__(self):
        return self.area_name

class KMLfile(models.Model):
    map_obj       = models.ForeignKey(Map)
    filename      = models.FileField(upload_to="kml_files")
    date_uploaded = models.DateField("date uploaded")
    def __unicode__(self):
        return self.filename
