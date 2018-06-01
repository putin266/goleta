#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


class MyUtils:

    @staticmethod
    def find_file(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    @staticmethod
    def is_file_exist(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return True
        return False
