# Generated by Django 4.2.5 on 2023-10-31 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellrequest',
            name='name_creator',
        ),
        migrations.AddField(
            model_name='sellrequest',
            name='id_creator',
            field=models.ForeignKey(blank=True, db_column='id_creator', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bmstu_lab.users'),
        ),
    ]
