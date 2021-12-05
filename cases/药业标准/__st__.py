#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    :
# @Author  : 
# @Desc    : 
# @File    : __st__.py
# *************************************

from lib.WebOpEnterprise import webOpEnterprise
from lib.EnterpriseOpApi import enterpriseOpApi
from lib.WebUtil import *


def suite_setup():
    print('执行测试套件的初始化')
    webOpEnterprise.operator_login(g_enterprise_operator_username_pharmaceutical, g_enterprise_operator_password_pharmaceutical)
    enterpriseOpApi.enterprise_login(g_enterprise_operator_username_pharmaceutical, g_enterprise_operator_password_pharmaceutical)
    INFO('请重新插拔ukey！击回车键结束')
    raw_input = input("input:")
    filling_ukey(packFilePharmaceutical)


def suite_teardown():
    print('执行测试套件的清除')
    webOpEnterprise.operator_logout()