#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-22 19:05:56
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

# -*- coding: UTF-8 -*-
from .CCPRestSDK import REST

# ACCOUNT SID
accountSid = '8a216da86e011fa3016e923e7c1c5631'

# AUTH TOKEN
accountToken = '1b7ce1b8a59f43b289c4d1f5688c520e'

# AppID
appId = '8a216da86e011fa3016e923e7c795638'

# 服务器ip
serverIP = 'app.cloopen.com'

# 服务器端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为列表 例如：['12','34']，如不需替换请填 ''
# @param $tempId 模板Id


class CCP(object):
    '''封装容联云发送短信'''
    # 用来保存对象的类属性
    instance = None

    def __new__(cls):
        if cls.instance is None:
            obj = super().__new__(cls)

            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj
        return cls.instance

    def sendTemplateSMS(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get('statusCode') == '000000':
            return True
        return False


if __name__ == '__main__':
    ccp = CCP()
    print(ccp.sendTemplateSMS('18579091508', ['123456', '180'], 1))
