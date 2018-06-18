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
        banner.img = 'index banners'
        banner.index = i + 1
        banner.web_url = ''
        banner.type = 1
        banner.save()

for i in range(4):
    bannerlist = Banner.objects.all().filter(index=str(i + 5))
    if not len(bannerlist) > 0:
        banner = Banner()
        banner.img = 'selected apps banners'
        banner.index = i + 1
        banner.web_url = ''
        banner.type = 2
        banner.save()

