# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-30 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0004_auto_20180530_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='is_hot',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='app',
            name='is_ph',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='app',
            name='is_tj',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shortnews',
            name='is_fav',
            field=models.BooleanField(default=False),
        ),
    ]
