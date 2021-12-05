#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2021/8/15 19:26
# @Author  : 
# @Desc    : 
# @File    : 打码操作.py
# *************************************
from lib.WebOpEnterprise import webOpEnterprise
from lib.EnterpriseOpApi import enterpriseOpApi
from lib.common import *
from lib.WebUtil import *
import time

desired_dict_product = {'companyName': '0510药业标准企业',
                        'mallJumpFlag': '1',
                        'name': '氯雷他定',
                        'stageNodes': [{'defaultValue': ['wuxi'],
                                        'propertyName': ['address'],
                                        'stageName': ['入库环节']}]}

desired_dict_pack = {'companyName': '0510药业标准企业',
                     'mallJumpFlag': '0',
                     'name': '药品包装码',
                     'stageNodes': []}

desired_dict_process = {'companyName': '0510药业标准企业',
                        'mallJumpFlag': '0',
                        'name': '药品流通码',
                        'stageNodes': []}

class C401:
    name = '药业标准-产品批量打码'

    def setup(self):
        print('执行C401用例的初始化')

    def teardown(self):
        print('执行C401用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdPharmaceutical)['batchNo']
        INFO(f'产品批次：{batchNo1}')
        STEP(2, '产品批量打码')
        batchNo2 = webOpEnterprise.multi_print_product_qrcode(productNamePharmaceutical)
        INFO(f'产品批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdPharmaceutical)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_product_qrcode(fileZipPath,productNamePharmaceutical)
        STEP(6, '查看解码文件')
        fileDecPath = get_recent_file(exp=f'{batchNo2}_dec.zip')
        INFO(f'下载文件：{fileDecPath}')
        STEP(7, '解压码文件')
        filePathList = unzip_file(fileDecPath)
        fileUnzipPath = filePathList[0]
        INFO(f'解压后的文件：{fileUnzipPath}')
        STEP(8, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, fileUnzipPath)
        INFO(f'码值：{qrcode}')
        STEP(9, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_product)


class C402:
    name = '药业标准-包装批量打码'

    def setup(self):
        print('执行C402用例的初始化')

    def teardown(self):
        print('执行C402用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdPharmaceutical)['batchNo']
        INFO(f'包装批次：{batchNo1}')
        STEP(2, '包装批量打码')
        batchNo2 = webOpEnterprise.multi_print_pack_qrcode(packNamePharmaceutical)
        INFO(f'包装批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdPharmaceutical)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_pack_qrcode(fileZipPath,packNamePharmaceutical)
        STEP(6, '查看解码文件')
        fileDecPath = get_recent_file(exp=f'{batchNo2}_dec.zip')
        INFO(f'下载文件：{fileDecPath}')
        STEP(7, '解压码文件')
        filePathList = unzip_file(fileDecPath)
        fileUnzipPath = filePathList[0]
        INFO(f'解压后的文件：{fileUnzipPath}')
        STEP(8, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, fileUnzipPath)
        INFO(f'码值：{qrcode}')
        STEP(9, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_pack)


class C403:
    name = '药业标准-流通批量打码'

    def setup(self):
        print('执行C403用例的初始化')

    def teardown(self):
        print('执行C403用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdPharmaceutical)['batchNo']
        INFO(f'流通批次：{batchNo1}')
        STEP(2, '流通批量打码')
        batchNo2 = webOpEnterprise.multi_print_process_qrcode(processNamePharmaceutical)
        INFO(f'流通批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdPharmaceutical)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_process_qrcode(fileZipPath,processNamePharmaceutical)
        STEP(6, '查看解码文件')
        fileDecPath = get_recent_file(exp=f'{batchNo2}_dec.zip')
        INFO(f'下载文件：{fileDecPath}')
        STEP(7, '解压码文件')
        filePathList = unzip_file(fileDecPath)
        fileUnzipPath = filePathList[0]
        INFO(f'解压后的文件：{fileUnzipPath}')
        STEP(8, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, fileUnzipPath)
        INFO(f'码值：{qrcode}')
        STEP(9, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_process)


if __name__ == '__main__':
    pass
