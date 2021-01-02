#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/12/8 20:45
# @Author  : 
# @Desc    : 
# @File    : 湘蘅.py
# *************************************
from lib.IndustrialOp import xh_ipc
from lib.common import *
import time


class C101:
    name = '接口-新灌装'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        timestamp = int(round(time.time() * 1000))
        # 生产班组批次号生成方式
        # yyyyMMdd + 班组编号 + 工控机编号 + 序号， 如：（20181218cqmyg00001）
        import datetime
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        teamBatch = f'{yesterday}011{timestamp}'
        body = [
            {'data': {'childCodes': xh_ipc.packList,
                      'clientId': xh_clientid,
                      'codeType': 'ZCSMART',
                      'collectGroupId': gz_collect,
                      'companyId': xh_companyid,
                      'packingType': 'PACKING',
                      'parentCode': xh_ipc.productList[0],
                      'stageNode': {'parentStageId': gz_pstageid,
                                    'properties': [{'defaultValue': time.strftime("%Y-%m-%d %H:%M:%S"),
                                                    'propertyId': 469,
                                                    'propertyName': '生产日期',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': 'XH1012',
                                                    'propertyId': 468,
                                                    'propertyName': '操作人',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': 'BZ002',
                                                    'propertyId': 467,
                                                    'propertyName': '班组编号',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': '1:50',
                                                    'propertyId': 532,
                                                    'propertyName': '包装比例',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': '是的发达德芙',
                                                    'propertyId': 466,
                                                    'propertyName': '班组负责人',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': 'XH1004',
                                                    'propertyId': 465,
                                                    'propertyName': '产线编号',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': '1号混合器',
                                                    'propertyId': 464,
                                                    'propertyName': '产线名称',
                                                    'stageId': gz_stageid},
                                                   {'defaultValue': teamBatch,
                                                    'propertyId': 470,
                                                    'propertyName': '生产班组批次号',
                                                    'stageId': gz_stageid}],
                                    'stageId': gz_stageid},
                      'timestamp': timestamp},
             'record': {'fillingName': 'A002',
                        'fillingNum': 16,
                        'fillingTime': timestamp,
                        'productId': productid,
                        'unit': '包'}
             }]
        ret = xh_ipc.filling(body=body, key=xh_key, iv=xh_iv, head=xh_ipc.head,
                               headers=xh_ipc.headers, payload=xh_ipc.payload, token=xh_ipc.token)
        assert ret['message'] == 'request_success', '新灌装接口调用失败'


if __name__ == '__main__':
    c = C101()
    c.teststeps()