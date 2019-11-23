#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 18:58:32
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from flask import current_app, Blueprint, make_response
from flask_wtf import csrf


html = Blueprint('web_html', __name__)


@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    '''提供html文件'''
    # 如果file_file_name为‘’， 表示访问的为/ ，请求的是主页
    if not html_file_name:
        html_file_name = 'index.html'

    if html_file_name != 'favicon.ico':
        html_file_name = 'html/' + html_file_name

    # flask提供的返回的静态文件的方法
    # return current_app.send_static_file(html_file_name)

    # 生成一个token
    csrf_token = csrf.generate_csrf()

    response = make_response(current_app.send_static_file(html_file_name))
    # 向cookies添加csrf_token
    response.set_cookie('csrf_token', csrf_token)

    return response
