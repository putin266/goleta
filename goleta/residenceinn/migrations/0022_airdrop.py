# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-22 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0021_userprofile_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirDrop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(db_index=True, max_length=254)),
                ('coin_name', models.CharField(max_length=254)),
                ('desc', models.TextField(blank=True, null=True)),
                ('airdrop_url', models.CharField(blank=True, max_length=254, null=True)),
                ('starts', models.IntegerField(blank=True, null=True)),
                ('record_date', models.DateTimeField(blank=True, null=True)),
                ('is_need_apply', models.BooleanField(default=False)),
                ('is_ethereum', models.BooleanField(default=False)),
                ('is_mail', models.BooleanField(default=False)),
                ('is_mobile', models.BooleanField(default=False)),
                ('is_telegram', models.BooleanField(default=False)),
                ('is_twitter', models.BooleanField(default=False)),
                ('index', models.IntegerField(default=99)),
            ],
        ),
    ]
