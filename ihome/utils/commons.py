#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 19:01:09
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from werkzeug.routing import BaseConverter
from ihome.utils.response_code import RET
from flask import session, jsonify, g
import functools


# 定义一个正则转换器
class ReConverter(BaseConverter):
    ''''''
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super().__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 定义验证登录状态的装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户登录状态
        user_id = session.get('user_id')
        # 如果用户登录, 执行视图函数
        if user_id:
            # 将user_id保存到g对象当中
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    return wrapper
