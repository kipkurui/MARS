# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class TfClass(models.Model):
    tf_class_id = models.CharField(db_column='TF_CLASS_ID', primary_key=True, max_length=45)
    tf_class = models.CharField(db_column='TF_CLASS', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TF_CLASS'


class TranscriptionFactor(models.Model):
    tf_id = models.CharField(db_column='TF_ID', primary_key=True, max_length=45)
    tf_name = models.CharField(db_column='TF_NAME', max_length=45, blank=True, null=True)
    alt_tf_name = models.CharField(db_column='ALT_TF_NAME', max_length=45, blank=True, null=True)
    tf_class_id = models.ForeignKey(TfClass, db_column='TF_CLASS_ID')

    class Meta:
        managed = False
        db_table = 'TRANSCRIPTION_FACTOR'

    #def __unicode__(self):
        #return self.alt_tf_name, self.tf_name


class ChipSeq(models.Model):
    chip_id = models.IntegerField(db_column='CHIP_ID', primary_key=True)
    tf_name = models.CharField(db_column='TF_NAME', max_length=45, blank=True, null=True)
    tf_id = models.ForeignKey('TranscriptionFactor', db_column='TF_ID', blank=True, null=True)
    database = models.CharField(db_column='DATABASE', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CHIP_SEQ'


class ChipData(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    chip_id = models.ForeignKey('ChipSeq', db_column='CHIP_ID', blank=True, null=True)
    raw = models.CharField(db_column='RAW', max_length=200, blank=True, null=True)
    at_100 = models.CharField(db_column='AT_100', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CHIP_DATA'


class Publications(models.Model):
    pub_id = models.IntegerField(db_column='PUB_ID', primary_key=True)
    small_ref = models.CharField(db_column='SMALL_REF', max_length=45, blank=True, null=True)
    full_ref = models.CharField(db_column='FULL_REF', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PUBLICATIONS'


class UrlTab(models.Model):
    link_id = models.IntegerField(db_column='LINK_ID', primary_key=True)
    url = models.CharField(db_column='URL', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'URL_TAB'


class Matrix(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    motif_id = models.CharField(db_column='MOTIF_ID', max_length=45, blank=True, null=True)
    motif_name = models.CharField(db_column='MOTIF_NAME', max_length=100, blank=True, null=True)
    tf_id = models.ForeignKey('TranscriptionFactor', db_column='TF_ID', blank=True, null=True)
    collection = models.CharField(db_column='COLLECTION', max_length=45, blank=True, null=True)
    link_id = models.ForeignKey('UrlTab', db_column='LINK_ID', blank=True, null=True)
    type = models.CharField(db_column='TYPE', max_length=45, blank=True, null=True)
    pub_id = models.ForeignKey('Publications', db_column='PUB_ID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MATRIX'


class MatrixData(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    matrix_id = models.ForeignKey(Matrix, db_column='MATRIX_ID')
    row = models.CharField(db_column='ROW', max_length=45)
    col = models.IntegerField(db_column='COL')
    val = models.FloatField(db_column='VAL', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MATRIX_DATA'
        unique_together = (('matrix_id', 'row', 'col'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
