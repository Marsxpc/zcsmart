#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/12/8 22:45
# @Author  : 
# @Desc    : 
# @File    : 晶科.py
# *************************************
from lib.IndustrialOp import jk_ipc
from lib.common import *
import time


class C001:
    name = '接口-码印刷'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        # 大码卷编号规则 (L+班组号+工控机编号+日期(yyyyMMdd)+自增序号)
        # 小码卷编号规则 只传输大码卷的时候，本字段可以传空 (S+班组号+工控机编号+ 日期(yyyyMMdd)+自增序号)
        bundleNumber = ''
        largeBundleNumber = f'LJX0001{time.strftime("%Y%m%d")}A01-{time.strftime("%H%M%S")}'
        body = {
            'data': {'bundleInfoSet': [{'qrcode': one, 'serialNo': idx + 1} for idx, one in enumerate(jk_ipc.packList)],
                     'bundleNumber': bundleNumber,
                     'bundleSize': len(jk_ipc.packList),
                     'bundleType': 'LARGE_BUNDLE',
                     'clientId': jk_clientid,
                     'collectGroupId': jk_collectgroupid,
                     'companyId': jk_companyid,
                     'createTime': time.strftime("%Y-%m-%d %H:%M:%S"),
                     'largeBundleNumber': largeBundleNumber,
                     'stageNode': {
                         'parentStageId': 177,
                         'properties': [
                             {
                                 'defaultValue': time.strftime("%Y-%m-%d %H:%M:%S"),
                                 'propertyId': 453,
                                 'propertyName': '印刷时间',
                                 'stageId': 178},
                             {'defaultValue': '王三',
                              'propertyId': 454,
                              'propertyName': '操作人',
                              'stageId': 178},
                             {'defaultValue': 'NO000001',
                              'propertyId': 455,
                              'propertyName': '操作人工号',
                              'stageId': 178},
                             {'defaultValue': 'NO.8443992990',
                              'propertyId': 456,
                              'propertyName': '打印机喷头编号',
                              'stageId': 178},
                             {'defaultValue': 'NO.00000567',
                              'propertyId': 457,
                              'propertyName': '扫码器编号',
                              'stageId': 178},
                             {'defaultValue': 'GP00001',
                              'propertyId': 458,
                              'propertyName': '班组号',
                              'stageId': 178},
                             {'defaultValue': '张琳',
                              'propertyId': 459,
                              'propertyName': '班组负责人',
                              'stageId': 178},
                             {'defaultValue': '2号混料机',
                              'propertyId': 460,
                              'propertyName': '产线名称',
                              'stageId': 178},
                             {'defaultValue': '5',
                              'propertyId': 461,
                              'propertyName': '产线编号',
                              'stageId': 178},
                             {'defaultValue': largeBundleNumber,
                              'propertyId': 462,
                              'propertyName': '大码卷编号',
                              'stageId': 178},
                             {'defaultValue': bundleNumber,
                              'propertyId': 463,
                              'propertyName': '小码卷编号',
                              'stageId': 178}],
                         'stageId': 178}},
            'timestamp': time.strftime("%Y%m%d%H%M%S"),
            'token': jk_ipc.token}
        ret = jk_ipc.codePrint(body=body, key=jk_key, iv=jk_iv, head=jk_ipc.head,
                               headers=jk_ipc.headers, payload=jk_ipc.payload, token=jk_ipc.token)
        assert ret['message'] == 'request_success','码印刷接口调用失败'


class C002:
    name = ''

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        pass