#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import os

print('start')
subprocess.call(['python3', './CreateAppLabels.py'])
print('create app lables end')
subprocess.call(['python3', './FetchAppListData.py'])
print('create app end')
subprocess.call(['python3', './CreateBanners.py'])
print('create banner end')
subprocess.call(['python3', './FetchShortNewsData.py'])
print('create short news end')
