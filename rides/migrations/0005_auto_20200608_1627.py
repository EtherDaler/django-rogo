# Generated by Django 3.0.7 on 2020-06-08 11:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0004_auto_20200607_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rides',
            name='total_rides',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)], verbose_name='Количество пассажиров'),
        ),
    ]
