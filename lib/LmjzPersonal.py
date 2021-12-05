#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2021/8/29 17:49
# @Author  : 
# @Desc    : 
# @File    : LmjzPersonal.py
# *************************************

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoAlertPresentException,InvalidElementStateException
import time, traceback
from lib.common import *
from lib.AppUtil import *
from appium.webdriver.connectiontype import ConnectionType
import os
from threading import Thread
import threading


class LmjzPersonal:
    def __init__(self):
        if 'global_appdriver' not in GSTORE.keys():
            # 进入手机桌面
            open_desktop()
        self.ad = get_global_appdriver()
        # 设置wifi连接（Appium Settings应用->权限管理->设置相关权限打开）
        self.ad.set_network_connection(ConnectionType.WIFI_ONLY)
        print(self.ad.network_connection)
        t = Thread(target=usb_install,args=(self.ad,))
        t.start()
        # 安装立马见真应用
        os.system('adb install -r %s' % appInstallPath)
        seconds = 10
        while seconds > 0:
            if not app_is_installed('com.zcsmart.lmjz'):
                time.sleep(1)
                seconds -= 1
            else:
                print('installed')
                break

        self.ad.start_activity("com.zcsmart.lmjz","com.iwall.msjz.ui.PrivacyPolicyActivity")
        self.ad.implicitly_wait(10)

        scroll_into_view(self.ad,'new UiSelector().className("android.widget.Button").instance(0)')
        # confirm_btn = self.ad.find_element_by_android_uiautomator(
        #     'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().className("android.widget.Button").instance(0));')
        # print(confirm_btn)
        # confirm_btn.click()
        # for i in range(0,2):
        #     w = self.ad.get_window_size()['width']
        #     self.ad.swipe(0, 0.9 * w, 0, 0.1 * w, 5000)
        #     time.sleep(1)
        # self.ad.find_element_by_android_uiautomator('new UiSelector().resourceId("com.zcsmart.lmjz:id/btn_try")').click()
        # self.ad.find_element_by_android_uiautomator('new UiSelector().resourceId("com.lbe.security.miui:id/permission_allow_foreground_only_button")').click()
        # self.ad.find_element_by_android_uiautomator(
        #     'new UiSelector().resourceId("com.lbe.security.miui:id/permission_allow_foreground_only_button")').click()


# os.system('adb uninstall com.zcsmart.lmjz')
# time.sleep(3)
lmjz = LmjzPersonal()