#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 21:35:10
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from . import api
from flask import jsonify, make_response, current_app
from ihome.utils.create_captcha import create_image_code
from ihome import redis_store
from ihome import constants
from ihome.utils.response_code import RET


# RESTful风格    GET 127.0.0.1:5000/api/v1.0/image_codes/<image_code_id>
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    '''获取图片验证码
    Args:
        image_code_id 图片验证码编号
    Return:
        验证码图片
    '''
    # 固定思路
    # 1.获取参数
    # 2.检验参数
    # 3.业务逻辑处理
    # 4.决定返回值

    # 生成验证码图片
    code_str, image_data = create_image_code()
    # 将图片真实值和编号保存到redis中
    try:
        redis_store.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, code_str)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='save image code id failed')

    # 返回图片
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/png'
    return resp

    # return image_data, 200, {'Content-Type': 'image/png'}
