from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    info = models.CharField(max_length=120, blank=True, null=True)
    image = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'


class RequestCategory(models.Model):
    id_request = models.ForeignKey('SellRequest', models.DO_NOTHING, db_column='id_request')
    id_category = models.ForeignKey('Category', models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'request_category'
        unique_together = (('id_request', 'id_category'),)


class SellRequest(models.Model):
    creator = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_creator', related_name="creator_sellreq", blank=True, null=True)
    moderator = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_moderator', related_name="moderator_sellreq", blank=True, null=True)
    date_creation = models.DateField(blank=True, null=True)
    date_formation = models.DateField(blank=True, null=True)
    date_completion = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sell_request'


class Users(models.Model):
    name_user = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'

