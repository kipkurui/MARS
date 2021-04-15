# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ChipData(models.Model):
    chip_data_id = models.IntegerField(db_column='ChIP_Data_ID', primary_key=True)  # Field name made lowercase.
    chip = models.ForeignKey('ChipSeq', models.DO_NOTHING, db_column='ChIP_ID', blank=True,
                             null=True)  # Field name made lowercase.
    raw = models.CharField(db_column='Raw', max_length=250, blank=True, null=True)  # Field name made lowercase.
    at_100 = models.CharField(db_column='AT_100', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChIP_Data'


class ChipSeq(models.Model):
    chip_id = models.IntegerField(db_column='ChIP_ID', primary_key=True)  # Field name made lowercase.
    tf_name = models.CharField(db_column='TF_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tf = models.ForeignKey('TranscriptionFactor', models.DO_NOTHING, db_column='TF_ID', blank=True,
                           null=True)  # Field name made lowercase.
    database = models.CharField(db_column='Database', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChIP_Seq'


class MatrixData(models.Model):
    matrix_id = models.AutoField(db_column='Matrix_ID', primary_key=True)  # Field name made lowercase.
    motif = models.ForeignKey('Motif', models.DO_NOTHING, db_column='Motif_ID')  # Field name made lowercase.
    col = models.CharField(db_column='Col', max_length=2)  # Field name made lowercase.
    row = models.IntegerField(db_column='Row')  # Field name made lowercase.
    val = models.FloatField(db_column='VAL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Matrix_Data'
        unique_together = (('matrix_id', 'motif', 'col', 'row'),)


class Motif(models.Model):
    motif_id = models.IntegerField(db_column='Motif_ID', primary_key=True)  # Field name made lowercase.
    motif_coll_id = models.CharField(db_column='Motif_coll_ID', max_length=100, blank=True,
                                     null=True)  # Field name made lowercase.
    motif_name = models.CharField(db_column='Motif_Name', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    collection_db = models.CharField(db_column='Collection_DB', max_length=45, blank=True,
                                     null=True)  # Field name made lowercase.
    tf_id = models.CharField(db_column='TF_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Motif'


class Organism(models.Model):
    taxonomic_id = models.IntegerField(db_column='Taxonomic_ID', primary_key=True)  # Field name made lowercase.
    identity = models.CharField(db_column='Identity', max_length=45)  # Field name made lowercase.
    scientific_name = models.CharField(db_column='Scientific_Name', max_length=60)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Organism'


class Pbm(models.Model):
    pbm_id = models.IntegerField(db_column='PBM_ID', primary_key=True)  # Field name made lowercase.
    tf_name = models.CharField(db_column='TF_NAME', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tf_id = models.CharField(db_column='TF_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PBM'


class PbmData(models.Model):
    pbm_data_id = models.IntegerField(db_column='PBM_Data_ID', primary_key=True)  # Field name made lowercase.
    pbm_id = models.IntegerField(db_column='PBM_ID')  # Field name made lowercase.
    pbm_debru = models.CharField(db_column='PBM_DEBRU', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PBM_Data'


class TfClass(models.Model):
    tf_class_id = models.CharField(db_column='TF_Class_ID', primary_key=True,
                                   max_length=45)  # Field name made lowercase.
    tf_class = models.CharField(db_column='TF_Class', max_length=150, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TF_Class'


class TranscriptionFactor(models.Model):
    tf_id = models.CharField(db_column='TF_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    tf_name = models.CharField(db_column='TF_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    alt_tf_name = models.CharField(db_column='Alt_TF_Name', max_length=150, blank=True,
                                   null=True)  # Field name made lowercase.
    tf_class_id = models.CharField(db_column='TF_Class_ID', max_length=15)  # Field name made lowercase.
    taxonomic_id = models.IntegerField(db_column='Taxonomic_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transcription_Factor'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
        tf_class = Motif.objects.filter(motif_name=tf)[0].tf_id
        motifs = Motif.objects.filter(tf_id=tf_class)
        for i in motifs:
            #print(i.motif_coll_id)
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
        motifs = Motif.objects.filter(tf_id=tf_class)
        for i in motifs:
            get_meme(i, meme_out)
        meme_out.write("\n")


def get_tf(tf):
    # TODO: Picking the first one with assumption it is correct?
    tf_class = Motif.objects.filter(motif_name=tf)[0].tf_id
    motifs = Motif.objects.filter(tf_id=tf_class)
    # tf_class_id = motifs[0].tf_id_id
    return tf_class, motifs


def get_meme(ids, out):
    print(ids.motif_id)
    data = MatrixData.objects.all().filter(motif_id=ids.motif_id)
    a = []
    c = []
    g = []
    t = []
    #print(len(data))
    for r in range(len(data)):
        #print(data[r].val)
        if data[r].col == "A":
            a.append(data[r].val)
        elif data[r].col == "C":
            c.append(data[r].val)
        elif data[r].col == "G":
            g.append(data[r].val)
        else:
            t.append(data[r].val)
    mid = "%s.%s" % (ids.motif_id, ids.collection_db)
    motif = ("\nMOTIF %s %s\n\n" % (mid, ids.motif_name))
    out.write(motif)

    header = ("letter-probability matrix: alength= 4 w= %s nsites= 20 E= 0\n" % (str(len(a) - 1)))
    out.write(header)
    #print(a)
    for j in range(1, len(a)):
        write_out = ("  %.6f\t  %.6f\t  %.6f\t  %.6f\t\n" % (a[j], float(c[j]), float(g[j]), float(t[j])))
        out.write(write_out)
