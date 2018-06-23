# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-23 04:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residenceinn', '0022_airdrop'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('app', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='residenceinn.App')),
            ],
        ),
        migrations.CreateModel(
            name='AppDetailImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('index', models.IntegerField(blank=True, default=1, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/app/detail/')),
                ('app_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='residenceinn.AppDetail')),
            ],
        ),
    ]
