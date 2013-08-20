# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'StochasticRule'
        db.delete_table(u'lsystem_stochasticrule')

        # Deleting model 'ContextSensitiveRule'
        db.delete_table(u'lsystem_contextsensitiverule')

        # Adding field 'Rule.left_of_start'
        db.add_column(u'lsystem_rule', 'left_of_start',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)

        # Adding field 'Rule.right_of_start'
        db.add_column(u'lsystem_rule', 'right_of_start',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)

        # Adding field 'Rule.probability'
        db.add_column(u'lsystem_rule', 'probability',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'StochasticRule'
        db.create_table(u'lsystem_stochasticrule', (
            (u'rule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lsystem.Rule'], unique=True, primary_key=True)),
            ('probability', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'lsystem', ['StochasticRule'])

        # Adding model 'ContextSensitiveRule'
        db.create_table(u'lsystem_contextsensitiverule', (
            ('right_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('left_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            (u'rule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lsystem.Rule'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'lsystem', ['ContextSensitiveRule'])

        # Deleting field 'Rule.left_of_start'
        db.delete_column(u'lsystem_rule', 'left_of_start')

        # Deleting field 'Rule.right_of_start'
        db.delete_column(u'lsystem_rule', 'right_of_start')

        # Deleting field 'Rule.probability'
        db.delete_column(u'lsystem_rule', 'probability')


    models = {
        u'lsystem.axiom': {
            'Meta': {'object_name': 'Axiom'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.rule': {
            'Meta': {'object_name': 'Rule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'probability': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'right_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.tree': {
            'Meta': {'object_name': 'Tree'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'generation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Axiom']"}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lsystem.Rule']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['lsystem']