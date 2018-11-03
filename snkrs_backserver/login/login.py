#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   .py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-xx-xx
Description:
"""

import os
import sys
from selenium import webdriver

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)


class Loginer(object):
    """login"""

    def __init__(self, username="", password=""):
        self.username = username
        self.password = password
        self.browser = webdriver.Firefox()

    def login(self):
        pass