#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
import requests
import random
import string
from MyUtils import MyUtils
from django.conf import settings
from django.core.files import File
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import *


def do():
    adlist = AirDrop.objects.all()
    for ad in adlist:
        ad.delete()
    index = 0
    r = requests.get(url='http://www.tokenairdrop.org/', stream=True)
    if r.status_code == 200:
        print('get html success')
        r.raw.decode_content = True
        soup = BeautifulSoup(r.raw, 'lxml')
        container_div = soup.find_all("div", {"class": "panel-body"})
        for tag in container_div:
            if tag.strong is not None:
                index = index + 1
                project_name = tag.contents[2].string.split('-')[0].strip()
                coin_name = tag.contents[2].string.split('-')[1].strip()
                desc = tag.contents[4].string.strip()
                airdrop_url = ''
                starts = 0
                record_date = None
                is_need_apply = False
                is_ethereum = False
                is_mail = False
                is_mobile = False
                is_telegram = False
                is_twitter = False
                for i in range(10, len(tag.contents)):
                    str = tag.contents[i].string
                    if str is None:
                        continue
                    str = str.strip()
                    if str  == '':
                        continue
                    if '空投入口' in str:
                        airdrop_url = str.split('href')[1].split('"')[1]
                        continue
                    if '空投详情' in str:
                        continue
                    if '重要程度' in str:
                        strlist = str.split(' ')
                        for tstr in strlist:
                            if tstr.strip() == '':
                                continue
                            if '★' in tstr:
                                starts = tstr.count('★')
                            if '收录时间' in tstr:
                                strdate = tstr.split('：')[1].strip()
                                record_date = datetime.strptime(strdate, '%Y/%m/%d')
                                continue
                        continue
                    if '需申请' in str:
                        is_need_apply = True
                        continue
                    if '手机' in str:
                        is_mobile = True
                        continue
                    if 'Telegram' in str:
                        is_telegram = True
                        continue
                    if 'Ethereum' in str:
                        is_ethereum = True
                        continue
                    if 'Mail' in str:
                        is_mail = True
                        continue
                    if 'Twitter' in str:
                        is_twitter = True
                        continue
                adlist = AirDrop.objects.filter(project_name=project_name).all()
                if len(adlist) > 0:
                    ad = adlist[0]
                else:
                    ad= AirDrop.objects.create(project_name=project_name)
                ad.coin_name = coin_name
                ad.index = index
                ad.desc =desc
                ad.airdrop_url = airdrop_url
                ad.starts = starts
                ad.record_date = record_date
                ad.is_need_apply = is_need_apply
                ad.is_ethereum = is_ethereum
                ad.is_mail = is_mail
                ad.is_mobile = is_mobile
                ad.is_telegram = is_telegram
                ad.is_twitter = is_twitter
                ad.save()

do()



