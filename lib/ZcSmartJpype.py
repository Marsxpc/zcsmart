#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/11/20 18:00
# @Author  : 
# @Desc    : 
# @File    : ZcSmartJpype.py
# *************************************

import jpype, requests, json, os, base64, time
from lib.common import *
from pprint import pprint


class ZcSmartJpype(object):
    def __init__(self, jvmPath, jarPath, dependency=None):
        # 开启java虚拟机
        # 当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
        if dependency:
            jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarPath,
                           "-Djava.ext.dirs=%s" % dependency)
        else:
            jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarPath)

    def encryptBody(self, body, key, iv):
        # 通过key,iv加密body
        # body传入的是json格式的，但这里比较特殊需要格式化
        body = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
        AES192Impl = jpype.JClass("com.zcsmart.aes.impl.AES192Impl")
        iaes = AES192Impl()
        AESModule = jpype.JClass("com.zcsmart.aes.en.AESModule")
        encBody = iaes.encDataBase64(jpype.JString(body),
                                     AESModule.AES_192_CBC_PKCS7, jpype.JString(key),
                                     jpype.JString(iv))
        SHA256Util = jpype.JClass("com.zcsmart.aes.SHA256Util")
        bytesBody = bytes(SHA256Util.getServerHash_C(encBody))
        base64Body = base64.b64encode(bytesBody)
        print("=========body: " + body)
        print("=========encBody: " + str(encBody))
        print("=========hashBody: " + base64Body.decode('utf8'))
        return str(encBody), base64Body.decode('utf8')

    def encryptHead(self, head):
        # 签名消息头
        AES192Impl = jpype.JClass("com.zcsmart.aes.impl.AES192Impl")
        iaes = AES192Impl()
        signData = iaes.signData(jpype.JString(head))
        print("头信息: " + head)
        print("签名数据: " + str(signData))
        return str(signData)

    def decryptData(self, encData, key, iv):
        # 解密
        AES192Impl = jpype.JClass("com.zcsmart.aes.impl.AES192Impl")
        iaes = AES192Impl()
        AESModule = jpype.JClass("com.zcsmart.aes.en.AESModule")
        decData = iaes.decDataBase64(jpype.JString(encData), AESModule.AES_192_CBC_PKCS7, jpype.JString(key),
                                     jpype.JString(iv))
        return json.loads(str(decData))

    def shutdownJvm(self):
        # 关闭java虚拟机
        print('Executing : Shutdown JVM')
        jpype.shutdownJVM()

    def decorator(self, func):
        # 请求token必传参数：body, key, iv, head, headers, payload
        # 其他接口必传参数：body, key, iv, head, headers, payload，token
        def wrapper(**kargs):
            kargsTuple = (kargs['body'], kargs['key'], kargs['iv'],
                          kargs['head'], kargs['payload'], kargs['headers'])
            body, key, iv, head, payload, headers = kargsTuple
            # 加密
            encBody, hashBody = self.encryptBody(body, key, iv)
            head['hashbody'] = hashBody
            # 签名
            signData = self.encryptHead(json.dumps(head))
            payload['encData'] = encBody
            if 'token' in kargs.keys():
                headers.update({'X-CLIENT-TOKEN': kargs['token']})
            headers.update({'X-CLIENT-AUTH': json.dumps(head), 'X-CLIENT-SIGN': signData})
            encData = func(**kargs)
            # 解密
            return self.decryptData(jpype.JString(encData), key, iv)

        return wrapper


zsj = ZcSmartJpype(jvmPath, jarPath)

if __name__ == '__main__':
    companyid = 8057
    clientid = 9
    collectgroupid = 303
    KEY_NO = '9e3985fc-3513-41c3-a6c4-dbd18a10b5a4'
    key = 'dOm2YTjIFWvqBpy74gxDZ3nG'
    iv = 'Nxx8hgVDSloa77NJ'
    times = time.strftime("%Y%m%d%H%M%S")
    head = {"companyid": companyid, "clientid": clientid, "timestamp": times}
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'KEY-NO': KEY_NO
    }
    payload = {}


    @zsj.decorator
    def getToken(body, key, iv, head, headers, payload):
        url = 'http://apps.vpos.xin/zcs_gateway/ry/getToken'
        response = requests.post(url=url, json=payload, headers=headers)
        encData = response.json()['encData']
        return encData


    body = {"cmd": "auth-token"}
    print(getToken(body=body, key=key, iv=iv, head=head, headers=headers, payload=payload))
