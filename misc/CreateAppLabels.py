#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import AppLabel

appLableDataList = [('Exchanges', '交易所', 1),
                    ('Wallet', '钱包', 2),
                    ('Market software', '行情软件', 3),
                    ('Tool software', '工具软件', 4),
                    ('Content information', '内容资讯', 5),
                    ('Block chain games', '区块链游戏', 6),
                    ('Industry application', '行业应用', 7)]

for label in appLableDataList:
    ll = AppLabel.objects.all().filter(name=label[0], cn_name=label[1])
    is_exist = bool(len(ll))
    if not is_exist:
        AppLabel.objects.create(name=label[0], cn_name=label[1])
    else:
        lb = ll[0]
        lb.code = label[2]
        lb.save()


