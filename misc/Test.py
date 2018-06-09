#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests
from MyUtils import MyUtils
from django.conf import settings
from django.core.files import File

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import App, AppLabel, Banner

def do():
    banners = Banner.objects.all()
    for banner in banners:
        if banner.type != 2:
            banner.type = 1
            banner.save()

def addlableapps():
    label = AppLabel.objects.filter(id='8').all()[0]
    list = ['MyToken', '电报telegram',  'NasNano', '币用',  '支点', '知币', '火币',  'AICoin',   '币世界',  '链得得',  '知识星球',   '芥末圈', '币用',  '币牛牛', '币安Binance',  'IMToken',  '网易星球',  '布洛克城',  'ONO']
    for name in list:
        applist = App.objects.filter(app_name=name).all()
        if len(applist) > 0 :
            print(applist[0].id)
            label.apps.add(applist[0])
        else:
            print(name)
    label.save()

def add_a_new_app():
    app = App.objects.filter(app_name='币车').all()[0]
    local_file = open('/root/www/goleta/media/upload/app/logo/tmp.png', 'rb')
    file = File(local_file)
    app.app_logo.save('biche_log.png', file)
    local_file.close()
    local_file = open('/root/www/goleta/media/upload/app/apk/tmp.apk', 'rb')
    file = File(local_file)
    app.android_apk.save('biche.apk', file)
    local_file.close()
    app.save()


def do2():
    app = App.objects.filter(app_name='币车')
    app.price = 10
    app.number_downloads = 3936
    app.star = 4.5
    app.ms = '链接你的价值圈'
    app.contents = '链接你的价值圈'
    app.tj_ms = '链接你的价值圈'
    app.index = 900
    app.is_tj = True
    app.is_ph = True
    app.is_hot = True
    app.android_package_name =  'biche'
    app.android_version = '2.0.1'
    app.android_size = '6.8M'
    app.android_url = ''
    app.ios_url = ''
    app.web_url = 'https://biche.yaofache.com/app/pc'
    app.save()


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

do()

