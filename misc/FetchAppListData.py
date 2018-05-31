#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import App, AppLabel

typelist = [11, 1, 2, 4, 13, 14, 15]
typelist = [11]
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
for typeid in typelist:
    r = requests.post(url='http://byb.world/index.php/Index/applist/p/1', data='id=' + str(typeid), headers=headers)
    content = r.json()
    typeinfo = content['typeinfo']
    labellist = AppLabel.objects.filter(cn_name=typeinfo['typename'], name=typeinfo['en_name'])
    if len(labellist) > 0:
        print('f1')
        label = labellist[0]
        yylist = content['yylist']
        for appinfo in yylist:
            print('f2')
            applist = App.objects.filter(app_name=appinfo['app_name'])
            if not len(applist) > 0:
                print('f3')
                app = App(app_name=appinfo['app_name'])
                app.save()
                label.apps.add(app)
        label.save()

