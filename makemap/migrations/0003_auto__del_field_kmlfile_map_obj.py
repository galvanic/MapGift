# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'KMLfile.map_obj'
        db.delete_column(u'makemap_kmlfile', 'map_obj_id')


    def backwards(self, orm):
        # Adding field 'KMLfile.map_obj'
        db.add_column(u'makemap_kmlfile', 'map_obj',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['makemap.Map']),
                      keep_default=False)


    models = {
        u'makemap.kmlfile': {
            'Meta': {'object_name': 'KMLfile'},
            'date_uploaded': ('django.db.models.fields.DateField', [], {}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'makemap.map': {
            'Meta': {'object_name': 'Map'},
            'area_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_provider': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'zoom': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['makemap']