#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import django
sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import AppLabel

appLableDataList = [('Exchanges', '交易所', 1, 1),
                    ('Wallet', '钱包', 2, 1),
                    ('Market software', '行情软件', 3, 1),
                    ('Tool software', '工具软件', 4, 1),
                    ('Content information', '内容资讯', 5, 1),
                    ('Block chain games', '区块链游戏', 6, 1),
                    ('Industry application', '行业应用', 7, 1),
                    ('Selected', '精选', 8, 2)]

for label in appLableDataList:
    ll = AppLabel.objects.all().filter(name=label[0], cn_name=label[1])
    is_exist = bool(len(ll))
    if not is_exist:
        AppLabel.objects.create(name=label[0], cn_name=label[1], code=label[2], type=label[3])
    else:
        lb = ll[0]
        lb.name = label[0]
        lb.cn_name = label[1]
        lb.code = label[2]
        lb.type = label[3]
        lb.save()


