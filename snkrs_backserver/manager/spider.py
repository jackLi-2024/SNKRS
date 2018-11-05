#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   .py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-xx-xx
Description:
"""

import os
import random
import sys
import time
import traceback

import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)


class Browser(object):
    """browser"""

    def __init__(self, proxies=None, headless=None, timeout=20):
        """
        :param url: 访问的url
        :param proxies: 代理
        :param headless: 是否使用无界面模式
        """
        self.proxies = proxies
        self.headless = headless
        self.timeout = timeout
        self.browser = self.driver()

    def proxy(self):
        """get proxy
           如果有其他代理，更改此处函数
        """
        if type(self.proxies) == list:
            one_proxy = {"http": "http://%s" % random.choice(self.proxies),
                         "https": "http://%s" % random.choice(self.proxies)}
        else:
            one_proxy = None
        return one_proxy

    def driver(self):
        """create a browser"""
        if self.headless:
            options = webdriver.FirefoxOptions()
            options.set_headless()
            # options=None
            options.add_argument('-headless')
            options.add_argument('--disable-gpu')
            if self.proxies:
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': self.proxy()  # 代理ip和端口
                    }
                )
                browser_driver = webdriver.Firefox(firefox_options=options, proxy=proxy)
            else:
                browser_driver = webdriver.Firefox(firefox_options=options)
        else:
            if self.proxies:
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': self.proxy()  # 代理ip和端口
                    }
                )
                browser_driver = webdriver.Firefox(proxy=proxy)
            else:
                browser_driver = webdriver.Firefox()
        browser_driver.set_page_load_timeout(self.timeout)
        browser_driver.set_script_timeout(self.timeout)
        return browser_driver

    def get(self, url):
        """driver get request"""
        self.browser.get(url)

    def click_elem(self, elem):
        """
        :param elem: 元素
        :return:
        """
        ActionChains(self.browser).move_to_element(elem).click().perform()

    def wait_for_element_loaded(self, type_name=None, elem_type=None):
        """
        :param type_name: 标签
        :param elem_type:By.CLASS_NAME
        :return:
        """
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((elem_type, type_name))
        )

    def __del__(self):
        """当消除browser时,会先关闭浏览器"""
        self.browser.close()

    def close(self):
        """手动关闭浏览器"""
        self.browser.close()


class Spider(object):
    """爬虫"""

    def __init__(self, proxies=None, try_time=5, frequence=0.1, timeout=600):
        """

        :param proxies: 代理
        :param try_time: 重试次数
        :param frequence: 抓取频率
        :param timeout: 超时
        """
        self.proxies = proxies
        self.session = requests.Session()
        self.try_time = try_time
        self.frequence = frequence
        self.timeout = timeout

    def proxy(self):
        """get proxy
                   如果有其他代理，更改此处函数
                """
        if type(self.proxies) == list:
            one_proxy = {"http": "http://%s" % random.choice(self.proxies),
                         "https": "http://%s" % random.choice(self.proxies)}
        else:
            one_proxy = None
        return one_proxy

    def get(self, url=None, headers=None, response_encode="UTF8"):
        """
        spider get request
        :param url: 请求url
        :param headers: 请求头
        :return:
        """
        for try_time in range(self.try_time):
            try:
                if self.proxies:
                    response = self.session.get(url=url, headers=headers, proxies=self.proxy,
                                                verify=False,
                                                timeout=self.timeout)
                else:
                    response = self.session.get(url=url, headers=headers,
                                                verify=False,
                                                timeout=self.timeout)
                response.encoding = response_encode
                result = response.text
                return result
            except Exception as e:
                logging.exception("%s forbidden:%s" % (time.asctime(), str(e)))
            time.sleep(self.frequence)

    def post(self, url=None, headers=None, data=None, response_encode="UTF8"):
        """
        spider post request
        :param url: 请求url
        :param headers: 请求头
        :param data: 请求参数
        :return:
        """
        for try_time in range(self.try_time):
            try:
                if self.proxies:
                    response = self.session.get(url=url, data=data, headers=headers,
                                                proxies=self.proxy,
                                                verify=False,
                                                timeout=self.timeout)
                else:
                    response = self.session.get(url=url, data=data, headers=headers,
                                                verify=False,
                                                timeout=self.timeout)
                response.encoding = response_encode
                result = response.text
                return result
            except Exception as e:
                logging.exception("%s forbidden:%s" % (time.asctime(), str(e)))
            time.sleep(self.frequence)


def test_browser():
    """unittest"""
    import time
    t0 = time.time()
    B = Browser(headless=False)
    try:
        B.get(url="https://www.nike.com/cn/launch/")
        B.wait_for_element_loaded("join-log-in", By.CLASS_NAME)
        elem_log = B.browser.find_element_by_class_name("join-log-in1")
        B.click_elem(elem_log)
        print(B.browser.page_source.encode("utf8"))
        print(time.time() - t0)
    except:
        print(traceback.print_exc())
        B.browser.close()


def test_spider():
    """unittest"""
    spider = Spider()
    print(spider.get(url="https://www.baidu.com"))


if __name__ == '__main__':
    test_browser()
    # test_spider()
