# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-17 10:36
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.etl.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='temp_20180817183639', max_length=30)),
                ('type', models.CharField(default='未分类', max_length=20)),
                ('user_id', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('pass_word', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, default=None, null=True, protocol='IPv4')),
                ('port', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('service_name', models.CharField(blank=True, default=None, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('source_file', models.FileField(blank=True, upload_to=apps.etl.models.source_file_path)),
                ('source_table', models.CharField(blank=True, max_length=30, null=True)),
                ('target_table', models.CharField(blank=True, max_length=30, null=True)),
                ('truncate', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('cnt_source', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('cnt_target', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('status', models.CharField(blank=True, default='等待', max_length=10, null=True)),
                ('complete_time', models.DateTimeField(auto_now=True)),
                ('source_container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='SourceContainer', to='etl.DataContainer')),
                ('target_container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='TargetContainer', to='etl.DataContainer')),
            ],
        ),
    ]
