# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Map'
        db.create_table(u'makemap_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('map_provider', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'makemap', ['Map'])

        # Adding model 'KMLfile'
        db.create_table(u'makemap_kmlfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map_obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['makemap.Map'])),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('date_uploaded', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'makemap', ['KMLfile'])


    def backwards(self, orm):
        # Deleting model 'Map'
        db.delete_table(u'makemap_map')

        # Deleting model 'KMLfile'
        db.delete_table(u'makemap_kmlfile')


    models = {
        u'makemap.kmlfile': {
            'Meta': {'object_name': 'KMLfile'},
            'date_uploaded': ('django.db.models.fields.DateField', [], {}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['makemap.Map']"})
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