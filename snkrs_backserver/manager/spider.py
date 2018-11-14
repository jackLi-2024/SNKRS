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
import signal
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding("utf-8")

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)
import api_proxy

api = api_proxy.ApiProxy("8a060b135916458790bd342ce378576e")


class Browser(object):
    """browser"""

    def __init__(self, proxies=None, headless=None, timeout=20, phantomjs_driver_path=None):
        """
        :param url: 访问的url
        :param proxies: 代理
        :param headless: 是否使用无界面模式
        """
        self.proxies = proxies
        self.headless = headless
        self.timeout = timeout
        self.phantomjs_driver_path = phantomjs_driver_path
        self.browser = self.driver()

    def proxy(self):
        """get proxy
           如果有其他代理，更改此处函数
        """
        if type(self.proxies) == list:
            one_proxy = random.choice(self.proxies)
        elif self.proxies == "api":
            one_proxy = random.choice(api.available_proxy())
        else:
            one_proxy = None
        return one_proxy

    def driver(self):
        """create a browser"""
        if self.headless == True:
            options = webdriver.FirefoxOptions()
            options.set_headless()
            # options=None
            options.add_argument('headless')
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
        elif self.headless == "PhantomJS":
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities["phantomjs.page.settings.userAgent"] = ua()
            desired_capabilities["phantomjs.page.settings.loadImages"] = False
            if self.proxies:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.MANUAL
                proxy.http_proxy = self.proxy()
                proxy.add_to_capabilities(desired_capabilities)
                browser_driver = webdriver.PhantomJS(executable_path=self.phantomjs_driver_path,
                                                     desired_capabilities=desired_capabilities,
                                                     service_args=['--ignore-ssl-errors=true',
                                                      "--cookies-file=cookie.txt"])
            else:
                browser_driver = webdriver.PhantomJS(executable_path=self.phantomjs_driver_path,
                                                     desired_capabilities=desired_capabilities,
                                                     service_args=['--ignore-ssl-errors=true',
                                                     "--cookies-file=cookie.txt"])
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
        try:
            self.browser.service.process.send_signal(signal.SIGTERM)
            self.browser.quit()
            logging.warn("***********上次关闭异常，此次成功(del)**********")
        except:
            logging.exception("***********上次正常关闭(del)**********")

    def close(self):
        """手动关闭浏览器"""
        for i in range(20):
            try:
                self.browser.service.process.send_signal(signal.SIGTERM)
                self.browser.quit()
                print "browser close sucessful"
                logging.info("browser close sucessful(close)")
                break
            except Exception as e:
                logging.exception("***********关闭异常%d次(close)**********" % (i))
                pass


class Spider(object):
    """爬虫"""

    def __init__(self, proxies=None, try_time=5, frequence=0.1, timeout=20):
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
        elif self.proxies == "api":
            one_proxy = {"http": "http://%s" % random.choice(api.available_proxy()),
                         "https": "http://%s" % random.choice(api.available_proxy())}
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
                    response = self.session.get(url=url, headers=headers, proxies=self.proxy(),
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
                # print traceback.print_exc()
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
                    response = self.session.post(url=url, data=data, headers=headers,
                                                 proxies=self.proxy(),
                                                 verify=False,
                                                 timeout=self.timeout)
                else:
                    response = self.session.post(url=url, data=data, headers=headers,
                                                 verify=False,
                                                 timeout=self.timeout)
                response.encoding = response_encode
                result = response.text
                return result
            except Exception as e:
                logging.exception("%s forbidden:%s" % (time.asctime(), str(e)))
            time.sleep(self.frequence)


def ua():
    """
    :return: get random header
    """
    ua_list = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) \
AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) \
AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/4.0 (compatible; MSIE 8.0;\
Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; \
Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) \
Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101\
Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) \
Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; \
Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    ]
    return random.choice(ua_list)


def test_browser():
    """unittest"""
    import time
    t0 = time.time()
    B = Browser(headless="PhantomJS",
                phantomjs_driver_path="/home/lijiacai/phantomjs-2.1.1-linux-x86_64/bin/phantomjs",
                proxies="api")
    try:
        B.get(url="https://www.qichamao.com")
        time.sleep(4)
        print(B.browser.page_source.encode("utf8"))
        print(time.time() - t0)
    except:
        print(traceback.print_exc())
        B.browser.close()


def test_spider():
    """unittest"""
    spider = Spider(proxies="api")
    headers = {
        "User-Agent": ua(),
        "Host": "www.qichamao.com",

    }
    print headers
    print(spider.get(url="https://www.qichamao.com", headers=headers).encode("utf8"))


if __name__ == '__main__':
    # test_browser()
    test_spider()
