# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-08 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0011_auto_20180605_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
