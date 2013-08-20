# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rule'
        db.create_table(u'lsystem_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'lsystem', ['Rule'])

        # Adding model 'ContextSensitiveRule'
        db.create_table(u'lsystem_contextsensitiverule', (
            (u'rule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lsystem.Rule'], unique=True, primary_key=True)),
            ('left_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('right_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal(u'lsystem', ['ContextSensitiveRule'])

        # Adding model 'StochasticRule'
        db.create_table(u'lsystem_stochasticrule', (
            (u'rule_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lsystem.Rule'], unique=True, primary_key=True)),
            ('probability', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'lsystem', ['StochasticRule'])

        # Adding model 'Axiom'
        db.create_table(u'lsystem_axiom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('seed', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'lsystem', ['Axiom'])

        # Adding model 'Tree'
        db.create_table(u'lsystem_tree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Axiom'])),
            ('generation', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('form', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'lsystem', ['Tree'])

        # Adding M2M table for field rules on 'Tree'
        m2m_table_name = db.shorten_name(u'lsystem_tree_rules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tree', models.ForeignKey(orm[u'lsystem.tree'], null=False)),
            ('rule', models.ForeignKey(orm[u'lsystem.rule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tree_id', 'rule_id'])


    def backwards(self, orm):
        # Deleting model 'Rule'
        db.delete_table(u'lsystem_rule')

        # Deleting model 'ContextSensitiveRule'
        db.delete_table(u'lsystem_contextsensitiverule')

        # Deleting model 'StochasticRule'
        db.delete_table(u'lsystem_stochasticrule')

        # Deleting model 'Axiom'
        db.delete_table(u'lsystem_axiom')

        # Deleting model 'Tree'
        db.delete_table(u'lsystem_tree')

        # Removing M2M table for field rules on 'Tree'
        db.delete_table(db.shorten_name(u'lsystem_tree_rules'))


    models = {
        u'lsystem.axiom': {
            'Meta': {'object_name': 'Axiom'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.contextsensitiverule': {
            'Meta': {'object_name': 'ContextSensitiveRule', '_ormbases': [u'lsystem.Rule']},
            'left_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'right_of_start': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'rule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['lsystem.Rule']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'lsystem.rule': {
            'Meta': {'object_name': 'Rule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'lsystem.stochasticrule': {
            'Meta': {'object_name': 'StochasticRule', '_ormbases': [u'lsystem.Rule']},
            'probability': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'rule_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['lsystem.Rule']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'lsystem.tree': {
            'Meta': {'object_name': 'Tree'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'generation': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Axiom']"}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lsystem.Rule']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['lsystem']