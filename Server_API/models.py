
from django.db import models
from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractBaseUser


class Category(models.Model):
    name_category = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    info = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(max_length=120, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'category'


class RequestCategory(models.Model):


    id_request = models.ForeignKey('SellRequest', models.DO_NOTHING, related_name='uniq_id_req', db_column='id_request')
    id_category = models.ForeignKey('Category', models.DO_NOTHING, related_name='uniq_id_cat', db_column='id_category')

    class Meta:
        managed = True
        db_table = 'request_category'
        unique_together = (('id_request', 'id_category'),)


class SellRequest(models.Model):

    date_creation = models.DateTimeField(blank=True, null=True)
    date_formation = models.DateTimeField(blank=True, null=True)
    date_completion = models.DateTimeField(blank=True, null=True)
    status = models.CharField(default='Черновик', max_length=30, blank=True, null=True)
    id_user = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='id_creator', related_name="creator_sellreq", blank=True, null=True)
    id_moderator = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='id_moderator', related_name="moderator_sellreq", blank=True, null=True)
    status_priority = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sell_request'



class NewUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    class Meta:
        managed = True


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=200, verbose_name="Пароль")
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'email'

    objects = NewUserManager()

    class Meta:
        managed = True