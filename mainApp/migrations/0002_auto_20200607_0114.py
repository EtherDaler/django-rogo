# Generated by Django 3.0.7 on 2020-06-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='car',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='car_number',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='car_year',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
