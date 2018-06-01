#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests
from django.core.files import File
from django.conf import settings

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import App, AppLabel

for app in App.objects.all():
    app.android_apk.name = app.android_apk.name.replace('upload/upload/', 'upload/')
    print(app.android_apk.name)
    app.save()

