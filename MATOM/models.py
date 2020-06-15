# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.


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


class Pbm(models.Model):
    pbm_id = models.IntegerField(db_column='PBM_ID', primary_key=True)  # Field name made lowercase.
    tf_name = models.CharField(db_column='TF_NAME', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tf_id = models.CharField(db_column='TF_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PBM'


class PbmData(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pbm = models.ForeignKey(Pbm, db_column='PBM_ID')  # Field name made lowercase.
    pbm_debru = models.CharField(db_column='PBM_DEBRU', max_length=45, blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PBM_DATA'


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


class Jobs(models.Model):
    job_no = models.IntegerField(primary_key=True)
    mode = models.CharField(max_length=45)
    tf_name = models.CharField(max_length=45)
    score_method = models.CharField(max_length=45)
    date_created = models.DateField()

###############################################################################
#                   Query code
###############################################################################


def get_chip(ids):
    chip = ChipSeq.objects.get(tf_id=ids).chipdata_set.all()
    tf_list = []
    for i in chip:
        tf_list.append(i.at_100)
    return tf_list


def run_get_meme(tf, out):
    """
    Runs the fetch_motif.get_meme function that reads from database and writes output in meme format
    :param tf:
    :param out:
    :return: Writes to file
    """
    with open(out, 'a') as meme_out:
        tf_class = Matrix.objects.filter(motif_name=tf)[0].tf_id_id
        motifs = Matrix.objects.filter(tf_id=tf_class)
        for i in motifs:
            get_meme(i, meme_out)
        meme_out.write("\n")


def run_get_meme_id(tf_class, out):
    """
    Runs the fetch_motif.get_meme function that reads from database and writes output in meme format
    :param tf_class:
    :param out:
    :return: Writes to file
    """
    with open(out, 'a') as meme_out:
        motifs = Matrix.objects.filter(tf_id=tf_class)
        for i in motifs:
            get_meme(i, meme_out)
        meme_out.write("\n")


def get_tf(tf):
    # TODO: Picking the first one with assumption it is correct?
    tf_class = Matrix.objects.filter(motif_name=tf)[0].tf_id_id
    motifs = Matrix.objects.filter(tf_id=tf_class)
    #tf_class_id = motifs[0].tf_id_id
    return tf_class, motifs


def get_meme(ids, out):
    data = MatrixData.objects.filter(matrix_id=ids.id)
    a = []
    c = []
    g = []
    t = []

    for r in range(len(data)):
        if data[r].row == "A":
            a.append(data[r].val)
        elif data[r].row == "C":
            c.append(data[r].val)
        elif data[r].row == "G":
            g.append(data[r].val)
        else:
            t.append(data[r].val)
    mid = ids.motif_id+"."+ids.collection
    motif = ("\nMOTIF %s %s\n\n" % (mid, ids.motif_name))
    out.write(motif)

    header = ("letter-probability matrix: alength= 4 w= %s nsites= 20 E= 0\n" % (str(len(a)-1)))
    out.write(header)
    for j in range(1, len(a)):
        write_out = ("  %.6f\t  %.6f\t  %.6f\t  %.6f\t\n" % (a[j], float(c[j]), float(g[j]), float(t[j])))
        out.write(write_out)