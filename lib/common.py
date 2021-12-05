#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/12/6 15:37
# @Author  : 
# @Desc    : 
# @File    : common.py
# *************************************
import os
from datetime import datetime
from robot.libraries.BuiltIn import logger

# 存储 全局共享 数据
GSTORE = {}


def INFO(info):
    """
    在运行终端和测试报告中打印 重要信息，
    使得 运行报告更加清晰

    参数：
    info :   信息描述
    """
    logger.info(f'{info}', True, True)


def STEP(stepNo, desc):
    """
    在运行终端和测试报告中打印出 测试步骤说明，
    使得 运行报告更加清晰

    参数：
    stepNo : 指定 是第几步
    desc :   步骤描述
    """
    logger.info(f'\n-- 第 {stepNo} 步 -- {desc} \n', True, True)


def CHECK_POINT(desc, condition):
    """
    检查点

    参数：
    desc :   检查点文字描述
    condition ： 检查点 表达式
    """
    logger.info(f'\n** 检查点 **  {desc} ', True, True)

    if condition:
        logger.info('---->  通过\n', True, True)
    else:
        logger.info('---->   !! 不通过!!\n', True, True)
        raise AssertionError(f'\n** 检查点不通过 **  {desc} ')


now = datetime.now().strftime("%Y%m%d%H%M%S")
jvmPath = r"D:\SoftWare\jre32\bin\client\jvm.dll"
jarPath = os.path.join(os.path.abspath('.'), r'D:\SoftWare\jre32\lib\ext\zcs-aes-1.1.1.jar')
# basePath = os.path.dirname(os.path.abspath('.'))
# basePath = os.path.dirname('.')
# packDataPath = os.path.join(basePath,'data\packData.txt')
# productDataPath = os.path.join(basePath,'data\productData.txt')
packDataPath = '.\data\packData.txt'
productDataPath = '.\data\productData.txt'
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
productid = 307
# productid = 425
parentstageid = 110
xh_KEY_NO = '94a1854d-c069-48e6-9911-6c6923ae4114'
xh_key = 'jkaIAdsclH7XL181gTSV5Qlq'
xh_iv = 'At8O7xVuYJd2TvUu'
###################################################################
g_enterprise_operator_username_universal = 'Jtyscuser'
g_enterprise_operator_password_universal = 'zcs@1234'
g_enterprise_operator_username_salt = 'xh201804'
g_enterprise_operator_password_salt = 'zcs@1234'
g_enterprise_operator_username_pharmaceutical = 'lz001'
g_enterprise_operator_password_pharmaceutical = 'zcs@1234'

g_enterprise_administrators_username = 'Jtyscadmin'
g_enterprise_administrators_password = 'zcs@1234'
g_ops_host = 'ops.vpos.xin'
extension_path = r'D:\工作\20201106\ukey软件\ukeyplugin\hebdpamadojcoeoblajgikefgieimgja_main.crx'
download_path = rf'D:\Downloads\{now}'
uidPath = r'D:\工作\pyfile\zcsmart\data\uid.txt'
driver_path = r'D:\project\driver\chromedriver.exe'
productNameUniversal = '打码测试产品'
packNameUniversal = '打码测试包装码'
processNameUniversal = '打码测试流通码'
productIdUniversal = '1246'
packIdUniversal = '248'
processIdUniversal = '160'
productNameSalt = '低钠盐'
packNameSalt = '食盐包装码'
processNameSalt = '食盐流通码'
productIdSalt = '297'
packIdSalt = '94'
processIdSalt = '97'
productNamePharmaceutical = '氯雷他定'
packNamePharmaceutical = '药品包装码'
processNamePharmaceutical = '药品流通码'
productIdPharmaceutical = '1376'
packIdPharmaceutical = '172'
processIdPharmaceutical = '134'
imgPath = r'D:\工作\pyfile\zcsmart\data\product.jpg'
mailAddress = 'rg_164518@126.com'
authCode = 'NKWBBAZTLPXVQQKT'
mailAddressPlusName = 'xue(%s)' % mailAddress
ukeyImporterDir = r'D:\工作\20201106\app及pack\测试'
packFileUniversal = 'ukey000106340001-jzybiz-test.pack'
packFileSalt = 'ukey010080550001-jzybiz-test.pack'
packFilePharmaceutical = 'ukey020101990001-jzybiz-test.pack'
