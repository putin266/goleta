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

from residenceinn.models import ShortNews

def do():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url='http://byb.world/index.php/Index/kuaixun', headers=headers)
    if r.status_code != 200:
        print('request failed')
        return
    snlist = ShortNews.objects.all().order_by('-date_created')
    if snlist is None or len(snlist) == 0:
        latest_timestamp = 0
    else:
        sn = snlist[0]
        latest_timestamp = int(sn.date_created.timestamp())
    print('latest timestamp' + str(latest_timestamp))
    content = r.json()
    zxlist = content['zxlist']
    for zx in zxlist:
        kxlist = zx['kx']
        for kx in kxlist:
            if int(kx['times']) > latest_timestamp:
                print('adding new one')
                new_sn = ShortNews()
                new_sn.title = kx['title']
                new_sn.ms = kx['ms']
                new_sn.content = kx['concent']
                new_sn.index = kx['level']
                new_sn.date_created = datetime.fromtimestamp(int(kx['times']))
                new_sn.is_fav = not (kx['is_fav'] == '2')
                new_sn.save()


do()
