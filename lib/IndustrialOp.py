#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/12/6 16:12
# @Author  : 
# @Desc    : 
# @File    : IndustrialOp.py
# *************************************
import requests, time, json
from pprint import pprint
from lib.common import *
from lib.ZcSmartJpype import zsj


def readData(filePath, lineNum):

    lineNum = int(lineNum)
    with open(filePath, 'rb+') as f:
        lines = f.read().splitlines()
        last_lines = lines[-lineNum:]
        for i in range(lineNum):
            for j in range(len(last_lines[i]) + 2):
                f.seek(-1, os.SEEK_END)
                f.truncate()
    return [one.decode('utf8') for one in last_lines]


class IndstrialOp:
    def __init__(self,companyid,clientid,KEY_NO,key,iv):
        # 获取token
        times = time.strftime("%Y%m%d%H%M%S")
        self.head = {"companyid": companyid, "clientid": clientid, "timestamp": times}
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'KEY-NO': KEY_NO
        }
        self.payload = {}

        @zsj.decorator
        def getToken(body, key, iv, head, headers, payload):
            url = f'http://{ghost}/zcs_gateway/ry/getToken'
            response = requests.post(url=url, json=payload, headers=headers)
            encData = response.json()['encData']
            return encData

        body = {"cmd": "auth-token"}
        ret = getToken(body=body, key=key, iv=iv, head=self.head, headers=self.headers, payload=self.payload)
        self.token = ret['data']['token']
        print(f'token*********{self.token}')
        # packData文件，取后100条数据，并删除；productData文件，取后1条数据，并删除
        self.packList = readData(packDataPath, 2)
        self.productList = readData(productDataPath, 1)

    @staticmethod
    @zsj.decorator
    def codePrint(body, key, iv, head, token, headers, payload):
        # 码印刷
        url = f'http://{ghost}/zcs_gateway/trace/i/s/industry/api/print/record'
        response = requests.post(url=url, json=payload, headers=headers)
        encData = response.json()['encData']
        return encData

    @staticmethod
    @zsj.decorator
    def filling(body, key, iv, head, token, headers, payload):
        # 新灌装
        url = f'http://{ghost}/zcs_gateway/trace/i/s/industry/connect/codes'
        response = requests.post(url=url, json=payload, headers=headers)
        encData = response.json()['encData']
        return encData


jk_ipc = IndstrialOp(jk_companyid,jk_clientid,jk_KEY_NO,jk_key,jk_iv)
xh_ipc = IndstrialOp(xh_companyid,xh_clientid,xh_KEY_NO,xh_key,xh_iv)

if __name__ == '__main__':
    pass