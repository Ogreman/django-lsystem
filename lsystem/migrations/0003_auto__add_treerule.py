# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TreeRule'
        db.create_table(u'lsystem_treerule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tree', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Tree'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lsystem.Rule'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'lsystem', ['TreeRule'])

        # Removing M2M table for field rules on 'Tree'
        db.delete_table(db.shorten_name(u'lsystem_tree_rules'))


    def backwards(self, orm):
        # Deleting model 'TreeRule'
        db.delete_table(u'lsystem_treerule')

        # Adding M2M table for field rules on 'Tree'
        m2m_table_name = db.shorten_name(u'lsystem_tree_rules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tree', models.ForeignKey(orm[u'lsystem.tree'], null=False)),
            ('rule', models.ForeignKey(orm[u'lsystem.rule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tree_id', 'rule_id'])


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
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lsystem.Rule']", 'through': u"orm['lsystem.TreeRule']", 'symmetrical': 'False'})
        },
        u'lsystem.treerule': {
            'Meta': {'ordering': "['order']", 'object_name': 'TreeRule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Rule']"}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lsystem.Tree']"})
        }
    }

    complete_apps = ['lsystem']