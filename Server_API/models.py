
from django.db import models
from datetime import datetime
from django.utils import timezone



class Category(models.Model):
    name_category = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    info = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class RequestCategory(models.Model):


    id_request = models.ForeignKey('SellRequest', models.DO_NOTHING, db_column='id_request', primary_key=True)
    id_category = models.ForeignKey('Category', models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'request_category'
        unique_together = (('id_request', 'id_category'),)


class SellRequest(models.Model):

    date_creation = models.DateTimeField(blank=True, null=True)
    date_formation = models.DateTimeField(blank=True, null=True)
    date_completion = models.DateTimeField(blank=True, null=True)
    status = models.CharField(default='Черновик', max_length=30, blank=True, null=True)
    id_creator = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_creator', related_name='id_creator_set', blank=True, null=True)
    id_moderator = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_moderator', related_name='sellrequest_id_moderator_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sell_request'


class Users(models.Model):
    name_user = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    moderator_sign = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

