import sys
import os
import django
import requests
from datetime import datetime
from MyUtils import MyUtils
from django.conf import settings

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import Banner

for i in range(4):
    bannerlist = Banner.objects.all().filter(index=str(i + 1))
    if not len(bannerlist) > 0:
        banner = Banner()
        banner.img = 'test'
        banner.index = i + 1
        banner.save()

