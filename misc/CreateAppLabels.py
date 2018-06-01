#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import AppLabel

appLableDataList = [('Exchanges', '交易所'),
                    ('Wallet', '钱包'),
                    ('Market software', '行情软件'),
                    ('Tool software', '工具软件'),
                    ('Content information', '内容资讯'),
                    ('Block chain games', '区块链游戏'),
                    ('Industry application', '行业应用')]

for label in appLableDataList:
    is_exist = bool(len(AppLabel.objects.all().filter(name=label[0], cn_name=label[1])))
    if not is_exist:
        AppLabel.objects.create(name=label[0], cn_name=label[1])


