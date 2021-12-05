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

desired_dict_product = {'companyName': '湖南省湘衡盐化有限公司',
                        'mallJumpFlag': '1',
                        'name': '低钠盐',
                        'stageNodes': [{'defaultValue': ['低钠盐',
                                                         '052-599010101',
                                                         '250g',
                                                         'QTP',
                                                         '食盐',
                                                         '矿盐'],
                                        'propertyName': ['产品名称',
                                                         '电话',
                                                         '净含量',
                                                         '产品执行标准号',
                                                         '产品类别',
                                                         '原料盐名称及产地'],
                                        'stageName': ['基本信息']},
                                       {'defaultValue': ['见包装', '见包装'],
                                        'propertyName': ['生产企业', '生产日期'],
                                        'stageName': ['生产灌装']}]}

desired_dict_pack = {'companyName': '湖南省湘衡盐化有限公司',
                     'mallJumpFlag': '0',
                     'name': '食盐包装码',
                     'stageNodes': []}

desired_dict_process = {'companyName': '湖南省湘衡盐化有限公司',
                        'mallJumpFlag': '0',
                        'name': '食盐流通码',
                        'stageNodes': []}

desired_dict_root = {'companyName': '湖南省湘衡盐化有限公司',
                     'mallJumpFlag': '1',
                     'name': '',
                     'stageNodes': []}


class C301:
    name = '盐业标准-单个产品溯码打码'

    def setup(self):
        print('执行C301用例的初始化')

    def teardown(self):
        print('执行C301用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdSalt)['batchNo']
        INFO(f'产品批次：{batchNo1}')
        STEP(2, '单个产品溯码打码')
        batchNo2 = webOpEnterprise.print_product_qrcode(productNameSalt)
        INFO(f'产品批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))
        STEP(4, '查看下载的码文件')
        file_path = get_recent_file(exp='code.txt')
        INFO(f'下载文件：{file_path}')
        STEP(5, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, file_path)
        INFO(f'码值：{qrcode}')
        STEP(6, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_product)


class C302:
    name = '盐业标准-产品批量打码'

    def setup(self):
        print('执行C302用例的初始化')

    def teardown(self):
        print('执行C302用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdSalt)['batchNo']
        INFO(f'产品批次：{batchNo1}')
        STEP(2, '产品批量打码')
        batchNo2 = webOpEnterprise.multi_print_product_qrcode(productNameSalt)
        INFO(f'产品批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.product_qrcode_batch_checkpoint(productIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_product_qrcode(fileZipPath, productNameSalt)
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


class C303:
    name = '盐业标准-产品密唯码打码'

    def setup(self):
        print('执行C303用例的初始化')

    def teardown(self):
        print('执行C303用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.product_qrcodeplusrfid_batch_checkpoint(productIdSalt)['batchNo']
        INFO(f'产品批次：{batchNo1}')
        STEP(2, '产品密唯码打码')
        batchNo2 = webOpEnterprise.print_qrcodeplusrfid(productNameSalt)
        INFO(f'产品批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.product_qrcodeplusrfid_batch_checkpoint(productIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileDecPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileDecPath}')
        STEP(5, '解压码文件')
        filePathList = unzip_file(fileDecPath)
        fileUnzipPath = filePathList[0]
        INFO(f'解压后的文件：{fileUnzipPath}')
        STEP(6, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(1, fileUnzipPath)
        INFO(f'码值：{qrcode}')
        STEP(7, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode, onlyCodeRequired=True)
        onlyCode1 = ret_dict['onlyCode']
        ret_dict.pop('onlyCode')
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_product)
        STEP(8, '获取文件中的第一个唯码')
        rfid = get_qrcode_by_file(2, fileUnzipPath)
        INFO(f'码值：{rfid}')
        STEP(9, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(rfid, onlyCodeRequired=True)
        onlyCode2 = ret_dict['onlyCode']
        ret_dict.pop('onlyCode')
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_product)
        CHECK_POINT('检查是否是唯一编码', onlyCode1 != onlyCode2)


class C304:
    name = '盐业标准-产品唯码打码'

    def setup(self):
        print('执行C304用例的初始化')

    def teardown(self):
        print('执行C304用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.product_rfid_batch_checkpoint(productIdSalt)['batchNo']
        INFO(f'产品批次：{batchNo1}')
        STEP(2, '产品唯码打码')
        batchNo2 = webOpEnterprise.print_product_rfid(productNameSalt)
        INFO(f'产品批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.product_rfid_batch_checkpoint(productIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))


class C305:
    name = '盐业标准-单个包装溯码打码'

    def setup(self):
        print('执行C305用例的初始化')

    def teardown(self):
        print('执行C305用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdSalt)['batchNo']
        INFO(f'包装批次：{batchNo1}')
        STEP(2, '单个包装溯码打码')
        batchNo2 = webOpEnterprise.print_pack_qrcode(packNameSalt)
        INFO(f'包装批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))
        STEP(4, '查看下载的码文件')
        file_path = get_recent_file(exp='code.txt')
        INFO(f'下载文件：{file_path}')
        STEP(5, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, file_path)
        INFO(f'码值：{qrcode}')
        STEP(6, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_pack)


class C306:
    name = '盐业标准-包装批量打码'

    def setup(self):
        print('执行C306用例的初始化')

    def teardown(self):
        print('执行C306用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdSalt)['batchNo']
        INFO(f'包装批次：{batchNo1}')
        STEP(2, '包装批量打码')
        batchNo2 = webOpEnterprise.multi_print_pack_qrcode(packNameSalt)
        INFO(f'包装批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.pack_qrcode_batch_checkpoint(packIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_pack_qrcode(fileZipPath,packNameSalt)
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


class C307:
    name = '盐业标准-包装唯码打码'

    def setup(self):
        print('执行C307用例的初始化')

    def teardown(self):
        print('执行C307用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.pack_rfid_batch_checkpoint(packIdSalt)['batchNo']
        INFO(f'包装批次：{batchNo1}')
        STEP(2, '包装唯码打码')
        batchNo2 = webOpEnterprise.print_pack_rfid(packNameSalt)
        INFO(f'包装批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.pack_rfid_batch_checkpoint(packIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))


class C308:
    name = '盐业标准-单个流通溯码打码'

    def setup(self):
        print('执行C308用例的初始化')

    def teardown(self):
        print('执行C308用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdSalt)['batchNo']
        INFO(f'流通批次：{batchNo1}')
        STEP(2, '单个流通溯码打码')
        batchNo2 = webOpEnterprise.print_process_qrcode(processNameSalt)
        INFO(f'流通批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))
        STEP(4, '查看下载的码文件')
        file_path = get_recent_file(exp='code.txt')
        INFO(f'下载文件：{file_path}')
        STEP(5, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, file_path)
        INFO(f'码值：{qrcode}')
        STEP(6, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode)
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_process)


class C309:
    name = '盐业标准-流通批量打码'

    def setup(self):
        print('执行C309用例的初始化')

    def teardown(self):
        print('执行C309用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdSalt)['batchNo']
        INFO(f'流通批次：{batchNo1}')
        STEP(2, '流通批量打码')
        batchNo2 = webOpEnterprise.multi_print_process_qrcode(processNameSalt)
        INFO(f'流通批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.process_qrcode_batch_checkpoint(processIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1000 == int(successNum))
        STEP(4, '查看下载的码文件')
        fileZipPath = get_recent_file(exp=f'{batchNo2}.zip')
        INFO(f'下载文件：{fileZipPath}')
        STEP(5, '服务端解码')
        webOpEnterprise.service_decode_process_qrcode(fileZipPath,processNameSalt)
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


class C310:
    name = '盐业标准-流通唯码打码'

    def setup(self):
        print('执行C310用例的初始化')

    def teardown(self):
        print('执行C310用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.process_rfid_batch_checkpoint(processIdSalt)['batchNo']
        INFO(f'流通批次：{batchNo1}')
        STEP(2, '流通唯码打码')
        batchNo2 = webOpEnterprise.print_process_rfid(processNameSalt)
        INFO(f'流通批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.process_rfid_batch_checkpoint(processIdSalt)['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))


class C311:
    name = '盐业标准-主体码溯码打码'

    def setup(self):
        print('执行C311用例的初始化')

    def teardown(self):
        print('执行C311用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.root_code_batch_checkpoint()['batchNo']
        INFO(f'主体码批次：{batchNo1}')
        STEP(2, '主体码溯码打码')
        batchNo2 = webOpEnterprise.print_multi_root(mailAddressPlusName)
        INFO(f'主体码批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.root_code_batch_checkpoint()['successNum']
        CHECK_POINT('检查成功数量', 2 == int(successNum))
        STEP(4,'查看解码密码')
        password = webOpEnterprise.send_records()
        STEP(5,'下载码包')
        filePath = retry_download_attachment()
        INFO(f'码包路径：{filePath}')
        STEP(6, '解压码包')
        filePathList = unzip_file(filePath,password)
        fileUnzipPath = filePathList[0]
        INFO(f'解压后的文件：{fileUnzipPath}')
        STEP(7, '获取文件中的第一个溯码')
        qrcode = get_qrcode_by_file(0, fileUnzipPath)
        INFO(f'码值：{qrcode}')
        STEP(8, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode,onlyCodeRequired=True)
        onlyCode1 = ret_dict['onlyCode']
        ret_dict.pop('onlyCode')
        CHECK_POINT('检查码内容是否符合预期', ret_dict == desired_dict_root)
        STEP(9, '获取文件中的第二个溯码')
        qrcode = get_qrcode_by_file(0, fileUnzipPath,2)
        INFO(f'码值：{qrcode}')
        STEP(10, '通过码查询接口查询码内容')
        ret_dict = enterpriseOpApi.search_qrcode_short_info(qrcode,onlyCodeRequired=True)
        onlyCode2 = ret_dict['onlyCode']
        ret_dict.pop('onlyCode')
        CHECK_POINT('检查码是否唯一', onlyCode1 != onlyCode2)


class C312:
    name = '盐业标准-主体码唯码打码'

    def setup(self):
        print('执行C312用例的初始化')

    def teardown(self):
        print('执行C312用例的清除')
        wd = get_global_webdriver()
        wd.refresh()

    def teststeps(self):
        STEP(1, '获取当前最新一条批次信息')
        batchNo1 = enterpriseOpApi.root_code_batch_checkpoint()['batchNo']
        INFO(f'主体码批次：{batchNo1}')
        STEP(2, '主体码唯码打码')
        batchNo2 = webOpEnterprise.print_root_rfid()
        INFO(f'主体码批次：{batchNo2}')
        CHECK_POINT('检查是否生成新的打码批次', batchNo1 != batchNo2)
        STEP(3, '获取当前最新一条批次成功数量')
        successNum = enterpriseOpApi.root_code_batch_checkpoint()['successNum']
        CHECK_POINT('检查成功数量', 1 == int(successNum))


if __name__ == '__main__':
    c = C312()
    webOpEnterprise.operator_login()
    c.teststeps()
