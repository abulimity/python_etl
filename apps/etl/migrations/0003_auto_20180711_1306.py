# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-11 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0002_auto_20180711_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etluser',
            name='source_file',
            field=models.FileField(upload_to='./upload/etl'),
        ),
    ]
