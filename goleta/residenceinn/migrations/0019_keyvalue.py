# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-18 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0018_auto_20180617_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('key', models.CharField(max_length=254, primary_key=True, serialize=False)),
                ('value', models.TextField(blank=True, null=True)),
                ('date_expired', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
