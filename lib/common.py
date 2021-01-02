#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/12/6 15:37
# @Author  : 
# @Desc    : 
# @File    : common.py
# *************************************
import os
GSTROE = {}
jvmPath = r"D:\SoftWare\jre32\bin\client\jvm.dll"
jarPath = os.path.join(os.path.abspath('.'), r'D:\SoftWare\jre32\lib\ext\zcs-aes-1.1.1.jar')
basePath = os.path.dirname(os.path.abspath('.'))
packDataPath = os.path.join(basePath,'data\packData.txt')
productDataPath = os.path.join(basePath,'data\productData.txt')
ghost = 'apps.vpos.xin'
# dependency = os.path.join(os.path.abspath('.'), 'F:/JPypeTestl/dependency')
# 8057-晶科数据
#################################################################
jk_companyid = 8057
jk_clientid = 9
jk_collectgroupid = 303
jk_KEY_NO = '9e3985fc-3513-41c3-a6c4-dbd18a10b5a4'
jk_key = 'dOm2YTjIFWvqBpy74gxDZ3nG'
jk_iv = 'Nxx8hgVDSloa77NJ'
#################################################################
# 8055-湘蘅数据
xh_companyid = 8055
xh_clientid = 8
gz_collect = 447
gz_pstageid = 106
gz_stageid = 179
rk_collect = 308
rk_stageid = 180
ck_collect = 309
ck_stageid = 182
yk_collect = 310
yk_stageid = 181
productid = 425
xh_KEY_NO = '94a1854d-c069-48e6-9911-6c6923ae4114'
xh_key = 'jkaIAdsclH7XL181gTSV5Qlq'
xh_iv = 'At8O7xVuYJd2TvUu'