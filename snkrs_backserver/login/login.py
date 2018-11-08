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
import logging
import time

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../" % cur_dir)
from manager.spider import *


class Loginer(object):
    """login"""

    def __init__(self, username="", password="", headless=True, proxies=None, timeout=20):
        """

        :param username: 用户名
        :param password: 密码
        :param headless: 是否使用无界面
        :param proxies: 代理
        """
        self.username = username
        self.password = password
        self.proxies = proxies
        self.headless = headless
        self.timeout = timeout
        self.B = Browser(self.proxies, self.headless, self.timeout)

    def login(self, url):
        """
        登陆
        :param url: 访问url
        :return:
        """
        try:
            self.B.get(url)
            self.B.wait_for_element_loaded("join-log-in", By.CLASS_NAME)
            elem = self.B.browser.find_element_by_class_name("join-log-in")
            self.B.click_elem(elem)
            self.B.wait_for_element_loaded("verifyMobileNumber", By.CLASS_NAME)
            name = self.B.browser.find_element_by_name("verifyMobileNumber")
            pwd = self.B.browser.find_element_by_name("password")
            name.send_keys(self.username)
            pwd.send_keys(self.password)
            self.B.wait_for_element_loaded("mobileLoginSubmit", By.CLASS_NAME)
            elem_submit = self.B.browser.find_element_by_class_name("mobileLoginSubmit")
            self.B.click_elem(elem_submit)
            self.B.browser.implicitly_wait(10)
            elem_username = self.B.browser.find_element_by_xpath("//span[@data-qa='user-name']")
            logging.info("%s : (login successful %s)" % (time.asctime(), self.username))
            return {"username": self.username, "status": "1", "item": "login"}
        except Exception as e:
            logging.exception(
                "%s : (login defeat %s) %s" % (time.asctime(), self.username, str(e)))
            self.B.close()
            return {"username": self.username, "status": "-1", "item": "login", "msg": e.args[0]}


def test():
    """unittest"""
    browsers = []
    loginer = Loginer(username="18404983790", password="Ljc199411081", headless=True, proxies=None, timeout=5)
    if loginer.login(url="https://www.nike.com/cn/launch/").get("status", "-1") == "1":
        browsers.append(loginer.B)
    for one in browsers:
        one.get("https://www.baidu.com")
        one.close()


if __name__ == '__main__':
    test()
