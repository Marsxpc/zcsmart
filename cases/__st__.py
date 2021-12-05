#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    :
# @Author  : 
# @Desc    : 
# @File    : __st__.py
# *************************************

from lib.WebUtil import *


def suite_setup():
    print('执行测试套件的初始化')
    os.system('taskkill /f /im chromedriver.exe /t > NUL 2>&1')
    open_browser()


def suite_teardown():
    print('执行测试套件的清除')
    driver = get_global_webdriver()
    driver.quit()