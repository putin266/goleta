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

sys.path.append("../goleta")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goleta.settings")
django.setup()

from residenceinn.models import App, AppLabel, Banner

def update_app_from_json():
    label = AppLabel.objects.filter(type=3).all()[0]
    applist = get_json()
    i = 0
    for app_json in  applist:
        i = i + 1
        try:
            app = App.objects.get(app_name=app_json['app_name'])
        except App.DoesNotExist:
            app = App()
            app.app_name = app_json['app_name']
        app.contents = app_json['contents']
        app.android_package_name = app_json['android_package_name']
        app.ios_url = app_json['ios_url']
        app.web_url = app_json['web_url']
        if not MyUtils.is_file_exist(get_file_name(app_json['android_apk']), settings.MEDIA_ROOT):
            if 'http' in app_json['android_apk']:
                tmp_url = app_json['android_apk']
            else:
                tmp_url = 'http://byb.world' + app_json['android_apk']
            r = requests.get(url=tmp_url, stream=True)
            if r.status_code == 200:
                print('apk success')
                r.raw.decode_content = True
                app.android_apk.save(get_file_name(app_json['android_apk']), r.raw)
            else:
               print('apk failed')
        for root, dirs, files in os.walk('/Users/Ethan/Downloads/appicon/'):
            if str(i) + '.png' in files:
                local_file = open('/Users/Ethan/Downloads/appicon/' + str(i) + '.png', 'rb')
            else:
                local_file = open('/Users/Ethan/Downloads/appicon/' + str(i) + '.jpg', 'rb')
        file = File(local_file)
        salt = ''.join(random.sample(string.digits, 6))
        app.app_logo.save(salt + '.png', file)
        local_file.close()
        label.apps.add(app)
        app.save()
    label.save()

def get_file_name(ip_str):
    return ip_str.split('/')[-1]

def get_json():
     return [{
            "app_name": u"布洛克城",
            "contents":u"布洛克城全新上线,一起参与全民挖宝",
            "android_package_name" : "",
            "android_apk" : "https://gxs-wallet.oss-cn-shanghai.aliyuncs.com/apk/official/gxs-blockcity-1.3.6-official.apk",
            "ios_url" : "https://itunes.apple.com/cn/app/%E5%B8%83%E6%B4%9B%E5%85%8B%E5%9F%8E/id1372814965?mt=8",
            "web_url":"https://blockcity.gxb.io/#/explore/blockchain/intro?platform=browser"
            },
        {
            "app_name": u"网易星球",
            "contents": u"基于区块链生态的价值共享平台",
            "android_package_name" : "",
            "android_apk" : "https://epay.nosdn.127.net/protect_163-e01170001_120.apk",
            "ios_url" : "https://itunes.apple.com/cn/app/%E7%BD%91%E6%98%93%E6%98%9F%E7%90%83/id1347027766?mt=8",
            "web_url": "https://star.8.163.com/"
        },
        {
            "app_name": u"星界",
            "contents": u"让个人信用资产创造更多更有意义的价值",
            "android_package_name" : "",
            "android_apk" : "https://halodown.linkeye.com/halodown/haloworld_1.0.1.apk",
            "ios_url" : "https://haloworld.linkeye.com/haloworld.html#/appdownload",
            "web_url": "https://www.linkeye.com/#/"
        },{
            "app_name": u"2345星球联盟",
            "contents": u"加入星球联盟，上网就能赚钱",
            "android_package_name" : "com.magicbox2345",
            "android_apk" : "http://download.2345.cn/qkl/app/planetAlliance_guanfang_1.1.1_3.apk",
            "ios_url" : "https://itunes.apple.com/cn/app/%E6%98%9F%E7%90%83%E8%81%94%E7%9B%9F-%E6%89%93%E9%80%A0%E5%AE%9E%E7%8E%B0%E7%94%A8%E6%88%B7%E4%BB%B7%E5%80%BC%E7%9A%84%E4%BF%A1%E4%BB%BB%E7%94%9F%E6%80%81/id1387403582?mt=8",
            "web_url": "https://www.2345.org/"
        },{
            "app_name": u"百度度宇宙",
            "contents": u"开启区块链星际旅程",
            "android_package_name" : "",
            "android_apk" : "http://a8.pc6.com/qsj7/duyuzhou.apk",
            "ios_url" : "https://yuzhou.baidu.com/h5/download.html#/",
            "web_url": "http://duyuzhou.baidu.com/#/"
        },{
            "app_name": u"币快报",
            "contents": u"基于元图谱链的区块链和数字货币价值发现平台",
            "android_package_name" : "",
            "android_apk" : "https://beenews-android-1255475383.cos.ap-shanghai.myqcloud.com/beenews-beekan.apk",
            "ios_url" : "https://itunes.apple.com/cn/app/%E5%B8%81%E5%BF%AB%E6%8A%A5/id1378099384",
            "web_url": "http://www.beekan.org/"
        },{
            "app_name": "InsurChain",
            "contents": u"去中心化的保险区块链创新生态系统",
            "android_package_name" : "",
            "android_apk" : "https://insur-ipa.oss-cn-beijing.aliyuncs.com/insurWallet.apk",
            "ios_url" : "https://wallet.qusukj.com/h5/shareSucc.html",
            "web_url": "http://www.insurchain.org/?lang=zh"
        },{
            "app_name": "onechain",
            "contents": u"一站式区块链应用解决方案",
            "android_package_name" : "",
            "android_apk" : "https://app1.haoduobi.cn/android/one208.apk",
            "ios_url" : "https://app1.haoduobi.cn/ios/index.html",
            "web_url": "http://www.onechain.one/"
        },{
            "app_name": u"of社群链",
            "contents": u"全世界在与你协作",
            "android_package_name" : "com.ofbank.wallet",
            "android_apk" : "https://appstore.vivo.com.cn/appinfo/downloadApkFile?id=2175215",
            "ios_url" : "https://fir.im/ofbankAndroid?utm_source=fir&utm_medium=qr",
            "web_url": "http://ofbank.com/"
        },{
            "app_name": u"有链",
            "contents": u"开启全民上链时代",
            "android_package_name" : "",
            "android_apk" : "https://ucstatic.ihuanqu.com/app/pkg/YouChainMobile_release_1.2.0_608_180608_2108.apk",
            "ios_url" : "https://you.ihuanqu.com/download.html?callapp=uchain1352878776%3A%2F%2F",
            "web_url": "http://youchain.cc/"
        }
    ]


update_app_from_json()
