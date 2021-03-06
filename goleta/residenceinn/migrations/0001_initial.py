# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-30 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('app_name', models.TextField()),
                ('app_logo', models.ImageField(upload_to='app/logo/')),
                ('price', models.IntegerField()),
                ('number_downloads', models.IntegerField()),
                ('star', models.DecimalField(decimal_places=1, max_digits=2)),
                ('ms', models.TextField()),
                ('contents', models.TextField()),
                ('tj_ms', models.TextField()),
                ('index', models.IntegerField()),
                ('is_tj', models.BooleanField()),
                ('is_ph', models.BooleanField()),
                ('is_hot', models.BooleanField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('android_package_name', models.TextField()),
                ('android_apk', models.FileField(upload_to='app/apk/')),
                ('android_version', models.CharField(max_length=254)),
                ('android_size', models.CharField(max_length=254)),
                ('android_url', models.TextField()),
                ('ios_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AppLabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('apps', models.ManyToManyField(to='residenceinn.App')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(upload_to='banner/')),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShortNews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('img', models.ImageField(upload_to='short_news/pic/')),
                ('ms', models.TextField()),
                ('content', models.TextField()),
                ('index', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_fav', models.BooleanField()),
            ],
        ),
    ]
