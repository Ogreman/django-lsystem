# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Branch'
        db.create_table(u'lsystem_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('startX', self.gf('django.db.models.fields.FloatField')()),
            ('startY', self.gf('django.db.models.fields.FloatField')()),
            ('endX', self.gf('django.db.models.fields.FloatField')()),
            ('endY', self.gf('django.db.models.fields.FloatField')()),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('angle', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'lsystem', ['Branch'])

        # Adding M2M table for field children on 'Branch'
        m2m_table_name = db.shorten_name(u'lsystem_branch_children')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_branch', models.ForeignKey(orm[u'lsystem.branch'], null=False)),
            ('to_branch', models.ForeignKey(orm[u'lsystem.branch'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_branch_id', 'to_branch_id'])

        # Adding model 'Rule'
        db.create_table(u'lsystem_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('left_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('right_of_start', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('probability', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'lsystem', ['Rule'])

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
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Axiom'])),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Branch'], null=True, blank=True)),
            ('generation', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('form', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('theta', self.gf('django.db.models.fields.FloatField')()),
            ('move', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'lsystem', ['Tree'])

        # Adding model 'TreeRule'
        db.create_table(u'lsystem_treerule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tree', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['lsystem.Tree'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Rule'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'lsystem', ['TreeRule'])


    def backwards(self, orm):
        # Deleting model 'Branch'
        db.delete_table(u'lsystem_branch')

        # Removing M2M table for field children on 'Branch'
        db.delete_table(db.shorten_name(u'lsystem_branch_children'))

        # Deleting model 'Rule'
        db.delete_table(u'lsystem_rule')

        # Deleting model 'Axiom'
        db.delete_table(u'lsystem_axiom')

        # Deleting model 'Tree'
        db.delete_table(u'lsystem_tree')

        # Deleting model 'TreeRule'
        db.delete_table(u'lsystem_treerule')


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
            'endX': ('django.db.models.fields.FloatField', [], {}),
            'endY': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'startX': ('django.db.models.fields.FloatField', [], {}),
            'startY': ('django.db.models.fields.FloatField', [], {})
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
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'move': ('django.db.models.fields.FloatField', [], {}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Branch']", 'null': 'True', 'blank': 'True'}),
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