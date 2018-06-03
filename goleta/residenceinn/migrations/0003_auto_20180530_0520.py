# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-30 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0002_auto_20180530_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='android_apk',
            field=models.FileField(blank=True, null=True, upload_to='app/apk/'),
        ),
        migrations.AlterField(
            model_name='app',
            name='android_package_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='android_size',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='android_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='android_version',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_logo',
            field=models.ImageField(blank=True, null=True, upload_to='app/logo/'),
        ),
        migrations.AlterField(
            model_name='app',
            name='app_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='contents',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='ios_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='ms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='number_downloads',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='tj_ms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='applabel',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='banner/'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='short_news/pic/'),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='ms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]