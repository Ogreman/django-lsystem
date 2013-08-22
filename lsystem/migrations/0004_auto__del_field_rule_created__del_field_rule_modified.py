# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rule.created'
        db.delete_column(u'lsystem_rule', 'created')

        # Deleting field 'Rule.modified'
        db.delete_column(u'lsystem_rule', 'modified')


    def backwards(self, orm):
        # Adding field 'Rule.created'
        db.add_column(u'lsystem_rule', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 8, 22, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Rule.modified'
        db.add_column(u'lsystem_rule', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 8, 22, 0, 0), blank=True),
                      keep_default=False)


    models = {
        u'lsystem.axiom': {
            'Meta': {'object_name': 'Axiom'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.branch': {
            'Meta': {'object_name': 'Branch'},
            'angle': ('django.db.models.fields.FloatField', [], {}),
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parent'", 'symmetrical': 'False', 'to': u"orm['lsystem.Branch']"}),
            'colour': ('django.db.models.fields.CharField', [], {'default': "'80,200,80'", 'max_length': '12'}),
            'endX': ('django.db.models.fields.FloatField', [], {}),
            'endY': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'startX': ('django.db.models.fields.FloatField', [], {}),
            'startY': ('django.db.models.fields.FloatField', [], {})
        },
        u'lsystem.rule': {
            'Meta': {'object_name': 'Rule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'probability': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'right_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.tree': {
            'Meta': {'object_name': 'Tree'},
            'branches': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'generation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'move': ('django.db.models.fields.FloatField', [], {}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Branch']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Axiom']"}),
            'theta': ('django.db.models.fields.FloatField', [], {}),
            'tree_rules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lsystem.Rule']", 'through': u"orm['lsystem.TreeRule']", 'symmetrical': 'False'})
        },
        u'lsystem.treerule': {
            'Meta': {'ordering': "['order']", 'object_name': 'TreeRule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Rule']"}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': u"orm['lsystem.Tree']"})
        }
    }

    complete_apps = ['lsystem']