#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   .py
Author: Lijiacai (v_lijiacai@baidu.com)
Date: 2018-xx-xx
Description:
"""
import json
import logging
import os
import sys

import re

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../" % cur_dir)

from manager.spider import *
from lxml import etree


class Monitor(object):
    """监控新品"""

    def __init__(self, proxies=None):
        self.proxies = proxies

    def get_url(self):
        """获取新品url,以及售卖时间"""
        urls = []
        headers = {
            "User-Agent": ua(),
            "Host": "www.nike.com",
            "Referer": "https://www.nike.com/cn/launch/?s=upcoming"
        }
        url = "https://www.nike.com/cn/launch/?s=upcoming"
        spider = Spider(proxies=self.proxies)
        result = spider.get(url=url, headers=headers)

        if result:
            figs = re.findall(r"\<figure.+?\<\/figure\>", result)
            for one in figs:
                page = etree.HTML(one)
                a_s = page.xpath("//a/@href")
                if len(a_s) == 2:
                    h3 = (page.xpath("//a")[1].xpath("div/div/h3"))
                    h6 = (page.xpath("//a")[1].xpath("div/div/h6"))
                    if h3:
                        title = h3[0].xpath("string(.)").strip()
                    else:
                        title = ""
                    if h6:
                        sellTime = h6[0].xpath("string(.)").strip()
                    else:
                        sellTime = ""
                    urls.append({"url": "https://www.nike.com%s" % a_s[1], "title": title,
                                 "sellTime": sellTime})
        return urls

    def get_info(self, **kwargs):
        """获取单个产品价格，尺码及类型"""
        out = {}
        url = kwargs.get("url")
        headers = {
            "User-Agent": ua(),
            "Host": "www.nike.com",
            "Referer": "https://www.nike.com/cn/launch/?s=upcoming"
        }
        url = url
        spider = Spider(proxies=self.proxies)
        result = spider.get(url=url, headers=headers)
        if not result:
            result = "<html></html>"
        localizedSize_list = re.findall(r'{"available".+?localizedSize.+?}', result)
        size = []
        for one in localizedSize_list:
            try:
                data = json.loads(one)
                avail = data.get("available", False)
                localizedSize = data.get("localizedSize", "")
                nikeSize = data.get("size", "")
                size.append(
                    {"available": avail, "localizedSize": localizedSize, "nikeSize": nikeSize})
            except Exception as e:
                logging.exception(str(e))

        page = etree.HTML(result)
        h1 = page.xpath("//h1")
        if h1:
            productType = h1[0].xpath("string(.)").strip()
        else:
            productType = ""
        h5 = page.xpath("//h5")
        if h5:
            productTitle = h5[0].xpath("string(.)").strip()
        else:
            productTitle = kwargs.get("title", "")
        price = page.xpath("//div[@data-qa='price']")
        if price:
            productPrice = price[0].xpath("string(.)").strip()
        else:
            productPrice = ""
        out["url"] = url
        out["size"] = size
        out["productType"] = productType
        out["productTitle"] = productTitle
        out["productPrice"] = productPrice
        out["sellTime"] = kwargs.get("sellTime", "")
        return out


def run():
    """run"""
    out = []
    monitor = Monitor()
    for one in monitor.get_url():
        out.append(monitor.get_info(**one))

    print(json.dumps(out, ensure_ascii=False))


def test():
    """unittest"""
    monitor = Monitor()
    # print(json.dumps(monitor.get_url(), ensure_ascii=False))
    print(monitor.get_info(
        url="https://www.nike.com/cn/launch/t/air-jordan-33-white-vast-grey-metallic-silver/"))


if __name__ == '__main__':
    # test()
    run()
