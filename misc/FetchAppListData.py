#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests
from MyUtils import MyUtils
from django.conf import settings

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import App, AppLabel

def do():
    typelist = [11, 1, 2, 4, 13, 14, 15]
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    for typeid in typelist:
        r = requests.post(url='http://byb.world/index.php/Index/applist/p/1', data='id=' + str(typeid), headers=headers)
        content = r.json()
        typeinfo = content['typeinfo']
        labellist = AppLabel.objects.filter(cn_name=typeinfo['typename'], name=typeinfo['en_name'])
        if len(labellist) > 0:
            label = labellist[0]
            if not MyUtils.is_file_exist(get_file_name(typeinfo['pic']), settings.MEDIA_ROOT):
                r = requests.get(url='http://byb.world' + typeinfo['pic'], stream=True)
                if r.status_code == 200:
                    print('success')
                    r.raw.decode_content = True
                    label.img.save(get_file_name(typeinfo['pic']), r.raw)
            yylist = content['yylist']
            for appinfo in yylist:
                applist = App.objects.filter(app_name=appinfo['app_name'])
                if not len(applist) > 0:
                    app = App(app_name=appinfo['app_name'])
                    update_app(app, appinfo)
                    label.apps.add(app)
                else:
                    app = applist[0]
                    update_app(app, appinfo)
            label.save()


def get_file_name(ip_str):
    return ip_str.split('/')[-1]


def update_app(app, appinfo):
    if appinfo['app_logo'] is not None and not appinfo['app_logo'] and not MyUtils.is_file_exist(get_file_name(appinfo['app_logo']), settings.MEDIA_ROOT):
        r = requests.get(url='http://byb.world' + appinfo['app_logo'], stream=True)
        if r.status_code == 200:
            print('app logo success')
            r.raw.decode_content = True
            app.app_logo.save(get_file_name(appinfo['app_logo']), r.raw)
    app.price = appinfo['wallet']
    app.number_downloads = int(appinfo['number'])
    app.star = float(appinfo['start'])
    app.ms = appinfo['ms']
    app.contents = appinfo['contents']
    app.tj_ms = appinfo['tj_ms']
    app.index = int(appinfo['level'])
    app.is_tj = bool(appinfo['is_tj'])
    app.is_ph = bool(appinfo['is_ph'])
    app.is_hot = bool(appinfo['is_hot'])
    app.android_package_name = appinfo['andr_baoname']
    if appinfo['andr_apk'] is not None and not appinfo['andr_apk'] and not MyUtils.is_file_exist(get_file_name(appinfo['andr_apk']), settings.MEDIA_ROOT):
        if 'http' in appinfo['andr_apk']:
            tmp_url = appinfo['andr_apk']
        else:
            tmp_url = 'http://byb.world' + appinfo['andr_apk']
        r = requests.get(url=tmp_url, stream=True)
        if r.status_code == 200:
            print('apk success')
            r.raw.decode_content = True
            app.android_apk.save(get_file_name(appinfo['andr_apk']), r.raw)
    app.android_version = appinfo['andr_banben']
    app.android_size = appinfo['andr_size']
    app.android_url = appinfo['andr_url']
    app.ios_url = appinfo['ios_url']
    app.web_url = ''
    app.save()


do()

