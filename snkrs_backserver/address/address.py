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
import time
import multiprocessing
import django

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../" % cur_dir)
from manager.spider import *
from login.login import Loginer


class Addr(object):
    """配送地址"""

    def __init__(self, username="", password="", lastname="", firstname="", province="", city="",
                 district="", detail_address="", phone_num="", headless=False, proxies=None,
                 timeout=20):
        """
        相关参数初始化
        :param username: 用户名
        :param password: 密码
        :param lastname: 姓
        :param firstname: 名
        :param province: 省份
        :param city: 城市
        :param district: 县城
        :param detail_address: 详细地址
        :param phone_num: 电话号码
        """
        self.username = username
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.province = province
        self.city = city
        self.district = district
        self.detail_address = detail_address
        self.phone_num = phone_num
        self.proxies = proxies
        self.headless = headless
        self.timeout = timeout
        self.setting_status = self.setting_addr(url="https://www.nike.com/cn/zh_cn/p/settings")

    def login(self):
        """配置地址之前需要登陆"""
        loginer = Loginer(username=self.username, password=self.password, headless=self.headless,
                          proxies=self.proxies, timeout=self.timeout)
        if loginer.login(url="https://www.nike.com/cn/launch/").get("status", "-1") == "1":
            return loginer.B

    def setting_addr(self, url):
        """
        设置配送地址
        :param url: url
        :return:
        """
        B = self.login()
        if B:
            try:
                # 设置请求url
                B.get(url)
                # 选中设置地址
                B.wait_for_element_loaded("addresses", By.CLASS_NAME)
                elem_addresses = B.browser.find_element_by_class_name("addresses")
                time.sleep(3)
                raw_input()
                B.click_elem(elem_addresses)
                # 编辑地址
                B.wait_for_element_loaded("edit-button-container", By.CLASS_NAME)
                elem_edit = B.browser.find_element_by_class_name("edit-button-container")
                B.click_elem(elem_edit)
                # 编辑姓名,注意名在前，姓在后
                B.wait_for_element_loaded("address-lastname", By.ID)
                elem_lastname = B.browser.find_element_by_id("address-lastname")
                elem_firstname = B.browser.find_element_by_id("address-firstname")
                elem_lastname.clear()
                elem_firstname.clear()
                elem_lastname.send_keys(self.lastname)
                elem_firstname.send_keys(self.firstname)
                # 编辑省份
                elem_province = B.browser.find_element_by_class_name("state-container")
                B.click_elem(elem_province)
                state_province = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper state-container container2 js-addressState']/div/ul/li")
                for one in state_province:
                    if one.text == self.province:
                        B.click_elem(one)
                # 编辑城市
                city = B.browser.find_element_by_class_name("city-container")
                B.click_elem(city)
                citys = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper city-container container1 js-addressCity']/div/ul/li")
                for one in citys:
                    if one.text == self.city:
                        B.click_elem(one)
                # 编辑县或城市
                district = B.browser.find_element_by_class_name("district-container")
                B.click_elem(district)
                districts = B.browser.find_elements_by_xpath(
                    "//div[@class='input-wrapper district-container container2 js-addressDistrict']/div/ul/li")
                for one in districts:
                    if one.text == self.district:
                        B.click_elem(one)
                # 编辑详细地址
                detail_address = B.browser.find_element_by_id("address-addressone")
                detail_address.clear()
                detail_address.send_keys(self.detail_address)
                # 编辑电话号码
                phonenum = B.browser.find_element_by_id("address-phonenumber")
                phonenum.clear()
                phonenum.send_keys(self.phone_num)
                # 保存设置
                save_button = B.browser.find_element_by_xpath(
                    "//button[@data-qa='my_account.settings.addresses.shipping_address.save_button']")
                save_button.click()
                # todo:这里需要验证是否保存时候一定配置成功
                B.close()
                # todo:这里需要导入相应的django模块数据库，将以下状态存入数据库
                now = time.strftime("%Y-%m-%d",
                                    time.localtime(time.time() - 24 * 60 * 60 * 0))
                return {"username": self.username, "status": "1", "item": "address",
                        "settingTime": "%s" % now}
            except Exception as e:
                logging.exception(
                    "%s :(address defeat %s) %s" % (time.asctime(), self.username, str(e)))
                B.close()
                now = time.strftime("%Y-%m-%d",
                                    time.localtime(time.time() - 24 * 60 * 60 * 0))
                return {"username": self.username, "status": "-1", "item": "address",
                        "settingTime": "%s" % now}
        else:
            now = time.strftime("%Y-%m-%d",
                                time.localtime(time.time() - 24 * 60 * 60 * 0))
            return {"username": self.username, "status": "-1", "item": "login",
                    "settingTime": "%s" % now}


def run(process_num=10):
    """
    addr_info: 命令行获取需要配置的用户信息及配送地址,例如：
                [{"username":"18404983790", "password":"Ljc19941108",
                "lastname":"lee", "firstname":"jack",
                "province":"黑龙江省", "city":"绥化市",
                "district":"安达市", "detail_address":"中国黑龙江绥化市安达市栖霞小区9栋505",
                "phone_num":"00000000000"}]
    进程数默认10个进程
    """
    p = multiprocessing.Pool(process_num)
    addr_info = json.loads(sys.argv[1])
    for one in addr_info:
        username = one.get("username", "")
        password = one.get("password", "")
        lastname = one.get("lastname", "")
        firstname = one.get("firstname", "")
        province = one.get("province", "")
        city = one.get("city", "")
        district = one.get("district", "")
        detail_address = one.get("detail_address", "")
        phone_num = one.get("username", "")
        if username and password and lastname and firstname and province and city and detail_address and phone_num:
            p.apply_async(Addr, args=(
                username, password, lastname, firstname, province, city, district, detail_address,
                phone_num))
    p.close()
    p.join()


def test():
    """unittest"""
    addr = Addr(username="18404983790", password="Ljc19941108", lastname="lee", firstname="jack",
                province=u"黑龙江省", city=u"绥化市",
                district=u"安达市", detail_address=u"中国黑龙江绥化市安达市栖霞小区9栋505",
                phone_num="00000000000", headless=True, proxies=None, timeout=40)
    print(addr.setting_status)


if __name__ == '__main__':
    test()
