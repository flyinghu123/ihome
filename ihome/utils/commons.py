#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 19:01:09
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from werkzeug.routing import BaseConverter


# 定义一个正则转换器
class ReConverter(BaseConverter):
    ''''''
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super().__init__(url_map)
        # 保存正则表达式
        self.regex = regex
