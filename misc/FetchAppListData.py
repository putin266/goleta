#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests
from MyUtils import MyUtils
from django.conf import settings
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime, timezone

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import *

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
                try:
                    app_detail = AppDetail.objects.get(app=app)
                except AppDetail.DoesNotExist:
                    app_detail = AppDetail.objects.create(app=app)
                app_detail.save()
                update_app_detail(appinfo['id'], app_detail)
            label.save()


def get_file_name(ip_str):
    return ip_str.split('/')[-1]


def update_app(app, appinfo):
    if appinfo['app_logo'] is not None and appinfo['app_logo'] and not MyUtils.is_file_exist(get_file_name(appinfo['app_logo']), settings.MEDIA_ROOT):
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
    if appinfo['andr_apk'] is not None and appinfo['andr_apk'] and not MyUtils.is_file_exist(get_file_name(appinfo['andr_apk']), settings.MEDIA_ROOT):
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


def mycrop(file_path):
    print(file_path)
    img = Image.open(file_path)
    print('size:' + str(img.size))
    area = (66 / 400 * img.size[0], 145 / 800 * img.size[1], 335 / 400 * img.size[0], 650 / 800 * img.size[1])
    img = img.crop(area)
    img.save(file_path)


def update_app_detail(app_id, app_detail):
    app_detail_imagelist = AppDetailImage.objects.filter(app_detail=app_detail)
    if len(app_detail_imagelist) == 0:
        r = requests.get(url='http://byb.world/index.php/Index/appinfo/id/' + app_id, stream=True)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            desc = soup.find_all('div', {'class': 'detail-cen-item detail-cen-item-first'})
            if len(desc) > 0:
                desc = desc[0]
                app_detail.app_desc = str(desc)
                app_detail.save()
            img_tags = soup.find(id='sass').find_all('img')
            index = 0
            for img in img_tags:
               index = index + 1
               r2 = requests.get(url='http://byb.world' + img['src'], stream=True)
               if r2.status_code == 200:
                   app_detail_img = AppDetailImage.objects.create(app_detail=app_detail)
                   print('app detail img success')
                   r2.raw.decode_content = True
                   app_detail_img.image.save(get_file_name(img['src']), r2.raw)
                   app_detail_img.index = index
                   app_detail_img.save()
                   mycrop(settings.MEDIA_ROOT + '/' + app_detail_img.image.name)

do()
