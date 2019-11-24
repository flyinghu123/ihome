#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-24 19:57:29
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import hashlib

secret_id = 'AKIDmMhgPvSIABxTpEnKI0TiieIhqsfDqbQ7'
secret_key = 'c2LQHtLYaNuKVR8uSt51kHZcPYSEjNoz'
region = 'ap-guangzhou'
bucket = 'robot-1259307444'


class CosCient(object):
    '''腾讯对象存储客户端'''
    instance = None

    def __new__(cls):
        if cls.instance is None:
            obj = super().__new__(cls)

            # 初始化REST SDK
            obj.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
            obj.client = CosS3Client(obj.config)
            # 获取一个MD5的加密算法对象
            obj.md5 = hashlib.md5()
            cls.instance = obj
        return cls.instance

    def upload_file(self, data):
        key = self.get_data_md5(data)
        response = self.client.put_object(
            Bucket=bucket,
            Body=data,
            Key=key,
            StorageClass='STANDARD',
            EnableMD5=False
        )
        return response['ETag'][1:-1]

    def get_data_md5(self, data):
        self.md5.update(data)
        # 以16进制返回消息
        return self.md5.hexdigest()


if __name__ == '__main__':
    cos = CosCient()
    with open('D:/QQPCmgr/Desktop/1.png', 'rb') as f:
        data = f.read()
        print(cos.upload_file(data))
