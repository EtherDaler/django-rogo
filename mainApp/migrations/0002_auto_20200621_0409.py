# Generated by Django 3.0.7 on 2020-06-20 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rides',
            name='date_create',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 21, 4, 9, 52, 167224), null=True, verbose_name='Дата создания'),
        ),
    ]