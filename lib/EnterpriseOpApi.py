#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2021/7/28 20:33
# @Author  : 
# @Desc    : 
# @File    : EnterpriseOpApi.py
# *************************************
from lib.common import *
import requests, json, jsonpath
from pprint import pprint


def handle_ret_json(jsonObj):
    s = json.dumps(jsonObj, ensure_ascii=False)
    ss = s.replace('\\', '').replace('"{', '{').replace('}"', '}')
    return json.loads(ss, encoding='utf-8')


def _batch_checkpoint(data):
    ret = {'batchNo': '', 'successNum': ''}
    if 0 != int(data['records']):
        ret = {
            'batchNo': data['rows'][0]['batchNo'],
            'successNum': data['rows'][0]['successNum']}
    return ret


class EnterpriseOpApi:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json; charset=UTF-8'}

    def enterprise_login(self, username, password):
        if 'enterpriseOpToken' in GSTORE.keys():
            self.token = GSTORE['enterpriseOpToken']
        else:
            url = f'https://{g_ops_host}/ops/v1/login'
            payload = {"username": username, "password": password}
            headers = {
                'Content-Type': 'application/json; charset=UTF-8'
            }
            response = requests.post(url=url, json=payload, headers=headers)
            pprint(response.json())
            self.token = GSTORE['enterpriseOpToken'] = response.json()['token']
        self.headers.update({'X-AUTH-TOKEN': self.token})

    def search_qrcode_info(self, qrcode):
        url = f'https://{g_ops_host}/ops/v2/code/info'
        payload = {"qrCodeId": qrcode, "uuid": 1111}
        response = requests.post(url=url, json=payload, headers=self.headers)
        ret = handle_ret_json(response.json())
        return ret

    def search_qrcode_short_info(self, qrcode, onlyCodeRequired=False, codeSearchTimesRequired=False):
        retlist = []
        info = self.search_qrcode_info(qrcode)
        companyName = info['message']['companyInfo']['companyName']
        name = info['message']['productInfo']['name']
        onlyCode = info['message']['codeInfo']['onlyCode']
        codeSearchTimes = info['message']['codeSearchTimes']
        mallJumpFlag = info['message']['mallInfo']['mallJumpFlag']
        stageNodes = info['message']['traceInfo']['stageNodes']
        for stageNode_info in stageNodes:
            stageName = jsonpath.jsonpath(stageNode_info, '$...stageName')
            defaultValue = jsonpath.jsonpath(stageNode_info, '$...defaultValue')
            propertyName = jsonpath.jsonpath(stageNode_info, '$...propertyName')
            retlist.append({'stageName': stageName, 'defaultValue': defaultValue, 'propertyName': propertyName})
        ret = {'companyName': companyName, 'name': name, 'mallJumpFlag': mallJumpFlag, 'stageNodes': retlist}
        if onlyCodeRequired:
            ret.update({'onlyCode': onlyCode})
        if codeSearchTimesRequired:
            ret.update({'codeSearchTimes': codeSearchTimes})
        return ret

    def account_top_list(self):
        url = f'https://{g_ops_host}/ops/account/top/list'
        response = requests.post(url=url, headers=self.headers)
        return response.json()

    def code_left(self):
        info = self.account_top_list()
        qrcode, qrcodePlusRfid, rfid = info['data']['qrcode'], info['data']['qrcodePlusRfid'], info['data']['rfid']
        qrcodeLeft, qrcodePlusRfidLeft, rfidLeft = int(qrcode.split('/')[0]), int(qrcodePlusRfid.split('/')[0]), int(
            rfid.split('/')[0])
        ret = {'qrcodeLeft': qrcodeLeft, 'qrcodePlusRfidLeft': qrcodePlusRfidLeft, 'rfidLeft': rfidLeft}
        return ret

    def product_qrcode_batch_checkpoint(self,productId):
        url = f'https://{g_ops_host}/ops/company/opr/product/qrcode/list'
        payload = {"pageIndex":1,"pageSize":10,"displayFlag":0,"displayActiveFlag":1,"date":[],"beginTime":"","endTime":"","productId":productId}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def product_rfid_batch_checkpoint(self,productId):
        url = f'https://{g_ops_host}/ops/company/opr/product/rfid/list'
        payload = {"pageSize": 10, "pageIndex": 1, "productId": productId, "batchNo": "", "creator": "",
                   "beginTime": "", "endTime": ""}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def product_qrcodeplusrfid_batch_checkpoint(self,productId):
        url = f'https://{g_ops_host}/ops/company/opr/product/qrcodeplusrfid/list'
        payload = {"productId":productId,"pageIndex":1,"pageSize":10}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def pack_qrcode_batch_checkpoint(self,packId):
        url = f'https://{g_ops_host}/ops/pack/qrcode/batch/list'
        payload = {"pageSize":10,"pageIndex":1,"productPackId":packId,"batchNo":"","creator":"","beginTime":"","endTime":""}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def pack_rfid_batch_checkpoint(self,packId):
        url = f'https://{g_ops_host}/ops/pack/rfid/batch/list'
        payload = {"pageSize":10,"pageIndex":1,"productPackId":packId,"batchNo":"","creator":"","beginTime":"","endTime":""}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def process_qrcode_batch_checkpoint(self,processId):
        url = f'https://{g_ops_host}/ops/process/qrcode/batch/list'
        payload = {"pageSize":10,"pageIndex":1,"productProcessId":processId,"batchNo":"","creator":"","beginTime":"","endTime":""}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def process_rfid_batch_checkpoint(self,processId):
        url = f'https://{g_ops_host}/ops/process/rfid/batch/list'
        payload = {"pageSize":10,"pageIndex":1,"productProcessId":processId,"batchNo":"","creator":"","beginTime":"","endTime":""}
        response = requests.post(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json()['data'])

    def root_code_batch_checkpoint(self):
        url = f'https://{g_ops_host}/ops/v1/root/batch/list'
        payload = {"pageIndex":1,"pageSize":10}
        response = requests.get(url=url,json=payload,headers=self.headers)
        return _batch_checkpoint(response.json())


enterpriseOpApi = EnterpriseOpApi()

if __name__ == '__main__':
    enterpriseOpApi.enterprise_login(g_enterprise_operator_username_universal, g_enterprise_operator_password_universal)
    # qrcode = 'http://fuli.zcsmart.com/q/514012AAT64ACiCEGIKMOGaL5CECAIAAgE4Vu28YVjinupj_Q50n2us0_SMQJnpo2pqXxGLQ'
    # aa = enterpriseOpApi.search_qrcode_short_info(qrcode)
    # pprint(aa)
    # print(enterpriseOpApi.code_left())
    aa = enterpriseOpApi.root_code_batch_checkpoint()
    pprint(aa)