#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 21:35:10
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from . import api
from flask import jsonify, make_response, current_app, request
from ihome.utils.create_captcha import create_image_code
from ihome import redis_store, db, constants
from ihome.models import User
from ihome.utils.response_code import RET
from ihome.libs.yuntongxun.sms import CCP
import random


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


@api.route('/sms_codes/<re(r"1[35678]\d{9}"):mobile>')
def get_sms_code(mobile):
    '''获取短信验证码'''
    # 1.获取参数
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')
    # 2.检验参数
    if not all([image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg='params not complete')

    # 3.业务逻辑处理
    # 从redis去除真实的图片验证码
    try:
        real_image_code = redis_store.get('image_code_%s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis数据库异常')

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或者过期
        return jsonify(errno=RET.NODATA, errmsg='图片验证码失效')

    # 删除redis中图片验证码  防止用一个验证码被多次使用
    try:
        redis_store.delete('image_code_%s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写进行对比
    if real_image_code.decode().lower() != image_code.lower():
        # 表示用户填写错误
        print(str(real_image_code).lower(), image_code.lower())
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码填写错误')

    # 判断对同一个手机号是否在60秒内有操作记录, 如果有判断用户操作频繁, 不接受处理
    try:
        send_flag = redis_store.get('send_sms_code_%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag:
            # 表示在60秒内有操作记录
            return jsonify(errno=RET.REQERR, errmsg='请求过于频繁, 请60秒后重试')

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user:
            # 表示手机号已经存在
            return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')

    # 如果手机号不存在生成短信验证码
    sms_code = '%06d' % random.randint(0, 999999)

    # 保存短信验证码
    try:
        redis_store.setex('sms_code_%s' % mobile, constants.IMAGE_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录， 防止用户在60秒内重复发送短信操作
        redis_store.setex('send_sms_code_%s' % mobile, constants.SEND_SMS_CODE_INTERVEL, 1)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='save sms code id failed')

    # 发送短信验证码
    try:
        ccp = CCP()
        result = ccp.sendTemplateSMS(mobile, [sms_code, str(int(constants.SMS_CODE_REDIS_EXPIRES/60)) + '分钟'], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='发送异常')

    # 4.返回值
    if result:
        # 发送成功
        return jsonify(errno=RET.OK, errmsg='发送成功')
    else:
        return jsonify(errno=RET.THIRDERR, errmsg='发送失败')
