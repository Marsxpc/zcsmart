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
        print(ret)
        assert ret['message'] == 'request_success', '新灌装接口调用失败'


class C102:
    name = '接口-新入库'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        timestamp = int(round(time.time() * 1000))
        body = {'data': {'clientId': xh_clientid,
          'collectGroupId': rk_collect,
          'companyId': xh_companyid,
          'connectionSet': [{'childCodes': [xh_ipc.packList[0]],
                             'trayCode': ''}],
          'errorContinue': False,
          'stageNodes': {'parentStageId': parentstageid,
                         'properties': [{'defaultValue': 'admin',
                                         'propertyId': 471,
                                         'propertyName': '仓储管理员',
                                         'stageId': rk_stageid},
                                        {'defaultValue': 'XL003',
                                         'propertyId': 472,
                                         'propertyName': '操作人',
                                         'stageId': rk_stageid},
                                        {'defaultValue': '001',
                                         'propertyId': 473,
                                         'propertyName': '操作人工号',
                                         'stageId': rk_stageid},
                                        {'defaultValue': 'C001',
                                         'propertyId': 474,
                                         'propertyName': '叉车编号',
                                         'stageId': rk_stageid},
                                        {'defaultValue': '李四',
                                         'propertyId': 475,
                                         'propertyName': '叉车司机姓名',
                                         'stageId': rk_stageid},
                                        {'defaultValue': 'CS002',
                                         'propertyId': 476,
                                         'propertyName': '叉车司机工号',
                                         'stageId': rk_stageid},
                                        {'defaultValue': '',
                                         'propertyId': 477,
                                         'propertyName': '托盘编号',
                                         'stageId': rk_stageid},
                                        {'defaultValue': 'KW0005',
                                         'propertyId': 478,
                                         'propertyName': '库位编号',
                                         'stageId': rk_stageid},
                                        {'defaultValue': time.strftime("%Y-%m-%d %H:%M:%S"),
                                         'propertyId': 479,
                                         'propertyName': '入库时间',
                                         'stageId': rk_stageid}],
                         'stageId': rk_stageid},
          'timestamp': timestamp},
 'record': {'productId': productid,
            'unit': '包',
            'wareHouseName': '入库仓A',
            'wareHouseNum': 16,
            'wareHouseTime': timestamp}}
        ret = xh_ipc.warehousing(body=body, key=xh_key, iv=xh_iv, head=xh_ipc.head,
                                 headers=xh_ipc.headers, payload=xh_ipc.payload, token=xh_ipc.token)
        assert ret['message'] == 'request_success', '新入库接口调用失败'

class C103:
    name = '接口-新出库'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        timestamp = int(round(time.time() * 1000))
        body = {'data': {'clientId': xh_clientid,
          'collectGroupId': ck_collect,
          'companyId': xh_companyid,
          'connectionSet': [{'childCodes': [xh_ipc.packList[0]],
                             'trayCode': ''}],
          'errorContinue': False,
          'stageNodes': {'parentStageId': parentstageid,
                         'properties': [{'defaultValue': '20181008001',
                                         'propertyId': 492,
                                         'propertyName': '出库单单号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '1',
                                         'propertyId': 493,
                                         'propertyName': '出库数量',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '箱',
                                         'propertyId': 494,
                                         'propertyName': '出库单位',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '王强',
                                         'propertyId': 495,
                                         'propertyName': '仓库管理员',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '彭于晏',
                                         'propertyId': 496,
                                         'propertyName': '出库操作人',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'CZ0002',
                                         'propertyId': 497,
                                         'propertyName': '出库操作人工号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'CC0001',
                                         'propertyId': 498,
                                         'propertyName': '出库叉车编号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '王磊',
                                         'propertyId': 499,
                                         'propertyName': '出库叉车司机姓名',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'CCSJ005',
                                         'propertyId': 500,
                                         'propertyName': '出库叉车司机工号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'TP0001',
                                         'propertyId': 501,
                                         'propertyName': '出库托盘编号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'KW0001',
                                         'propertyId': 502,
                                         'propertyName': '出库库位编号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'TD0001',
                                         'propertyId': 503,
                                         'propertyName': '出库通道门编号',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '2021-01-04 14:05:00',
                                         'propertyId': 504,
                                         'propertyName': '出库时间',
                                         'stageId': ck_stageid},
                                        {'defaultValue': 'HTTP://zjbaogao.com/baogao001.pdf',
                                         'propertyId': 505,
                                         'propertyName': '质检单url',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '长沙',
                                         'propertyId': 506,
                                         'propertyName': '运输目的地',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '湖南盐业',
                                         'propertyId': 507,
                                         'propertyName': '收货单位',
                                         'stageId': ck_stageid},
                                        {'defaultValue': '湘A001,湘A002,湘A003',
                                         'propertyId': 508,
                                         'propertyName': '运送车车牌号',
                                         'stageId': 0}],
                         'stageId': ck_stageid},
          'timestamp': timestamp},
 'record': {'productId': productid,
            'unit': '包',
            'wareHouseName': '出库仓A',
            'wareHouseNum': 16,
            'wareHouseTime': timestamp}}
        ret = xh_ipc.exWarehousing(body=body, key=xh_key, iv=xh_iv, head=xh_ipc.head,
                                 headers=xh_ipc.headers, payload=xh_ipc.payload, token=xh_ipc.token)
        assert ret['message'] == 'request_success', '新入库接口调用失败'


class C104:
    name = '接口-移库'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        timestamp = int(round(time.time() * 1000))
        body = {'data': {'clientId': xh_clientid,
          'collectGroupId': yk_collect,
          'companyId': xh_companyid,
          'connectionSet': [{'childCodes': [xh_ipc.packList[0]],
                             'trayCode': ''}],
          'stageNodes': {'parentstageid': 110,
                         'properties': [{'defaultValue': '李嘉诚',
                                         'propertyId': 480,
                                         'propertyName': '仓库管理员',
                                         'stageId': yk_stageid},
                                        {'defaultValue': '王诗意',
                                         'propertyId': 481,
                                         'propertyName': '操作人',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'CZ0001',
                                         'propertyId': 482,
                                         'propertyName': '操作人工号',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'C0001',
                                         'propertyId': 483,
                                         'propertyName': '移库叉车编号',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'CCSJ002',
                                         'propertyId': 484,
                                         'propertyName': '移库叉车司机工号',
                                         'stageId': yk_stageid},
                                        {'defaultValue': '王思聪',
                                         'propertyId': 485,
                                         'propertyName': '移库叉车司机姓名',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'YKTD005',
                                         'propertyId': 486,
                                         'propertyName': '移库通道门编号',
                                         'stageId': yk_stageid},
                                        {'defaultValue': '2021-01-04 14:18:27',
                                         'propertyId': 487,
                                         'propertyName': '移库时间',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'CK0001',
                                         'propertyId': 488,
                                         'propertyName': '目标仓库',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'KW0001',
                                         'propertyId': 489,
                                         'propertyName': '目标库位',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'TP0001',
                                         'propertyId': 490,
                                         'propertyName': '目标t托盘',
                                         'stageId': yk_stageid},
                                        {'defaultValue': 'TD0001',
                                         'propertyId': 491,
                                         'propertyName': '目前通道门编号',
                                         'stageId': yk_stageid}],
                         'stageId': yk_stageid},
          'timestamp': timestamp},
 'timestamp': timestamp,
 'token': xh_ipc.token}
        ret = xh_ipc.warehouseShifting(body=body, key=xh_key, iv=xh_iv, head=xh_ipc.head,
                                 headers=xh_ipc.headers, payload=xh_ipc.payload, token=xh_ipc.token)
        assert ret['message'] == 'request_success', '移库接口调用失败'

class C105:
    name = '接口-查询码是否已记录'

    def setup(self):
        pass

    def teardown(self):
        pass

    def teststeps(self):
        body = {"qrCode":"513010Ae0sgAACLEOztEbs0AAgAASPCL25TEDquxLSCE60C-xEPVO47dLPTr9okt4G"}
        ret = xh_ipc.codeIsRecord(body=body, key=xh_key, iv=xh_iv, head=xh_ipc.head,
                                 headers=xh_ipc.headers, payload=xh_ipc.payload, token=xh_ipc.token)
        assert ret['message'] == 'request_success', '查询码是否已记录接口调用失败'


if __name__ == '__main__':
    c = C105()
    c.teststeps()