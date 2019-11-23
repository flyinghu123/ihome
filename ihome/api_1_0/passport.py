#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-23 10:42:31
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from . import api
from flask import request, jsonify, current_app, session
from ihome.utils.response_code import RET
import re
from ihome import redis_store, db, constants
from ihome.models import User
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError


@api.route('/users', methods=['POST'])
def register():
    '''注册
    Args:
        手机号, 短信验证码, 密码, 确认密码     参数格式: json
    '''
    # 1.获取参数
    # 获取请求的json数据, 返回字典
    req_dict = request.json
    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')

    # 2.校验参数
    if not all([mobile, sms_code, password, password2]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg='params not complete')

    # 判断手机号格式
    if not re.match(r'1[34578]\d{9}', mobile):
        # 表示手机号格式错误
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

    # 判断两次密码
    if password != password2:
        # 表示两次密码不一致
        return jsonify(errno=RET.PARAMERR, errmsg='两次密码不一致')

    # 3.业务逻辑处理
    # 从redis取出真实的短信验证码
    try:
        real_sms_code = redis_store.get('sms_code_%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis数据库异常')

    # 判断短信验证码是否过期
    if real_sms_code is None:
        # 表示验证码过期
        return jsonify(errno=RET.NODATA, errmsg='短信验证码失效')

    # 删除redis中短信验证码, 防止同一个短信验证码使用多次
    try:
        redis_store.delete('sms_code_%s' % mobile)
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户输入的短信验证码是否正确
    if real_sms_code != sms_code:
        # 表示短信验证码输入错误
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码填写错误')

    # 判断手机号是否注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='mysql数据库异常')
    # if user:
    #     # 表示手机号已经存在
    #     return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')
    # 将判断手机号是否注册和下面添加用户数据合二为一, 因为手机号字段设置了唯一性, 重复添加也就是手机号注册过或抛异常

    # 保存用户注册数据到mysql数据库中
    user = User(name=mobile, mobile=mobile)
    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现重复值, 即手机号已经注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='mysql数据库异常')

    # 保存登录状态到session中
    session['name'] = mobile
    session['mobile'] = mobile
    session['user_id'] = user.id

    # 4.返回结果
    return jsonify(errno=RET.OK, errmsg='注册成功')


@api.route('/sessions', methods=['POST'])
def login():
    '''用户登录
    Args:
        手机号, 密码
    '''
    # 1.获取参数
    req_dict = request.json
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')
    image_code = req_dict.get('image_code')
    image_code_id = req_dict.get('image_code_id')

    # 2.校验参数
    # 参数完整性校验
    if not all([mobile, password, image_code, image_code_id]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg='params not complete')

    # 手机号格式
    if re.match(r'1[34578]\d{9}', mobile) is None:
        # 表示手机号格式错误
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

    # 3.业务逻辑处理
    # 从redis取出真实的图片验证码
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
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码填写错误')

    # 判断错误次数是否超过次数限制, 如果超过限制则返回
    # redis记录: 'access_nums_请求的ip': 次数
    user_ip = request.remote_addr  # 用户ip
    try:
        access_nums = redis_store.get('access_nums_%s' % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg='登录错误次数过多, 请稍后重试')

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')

    # 用数据库中的密码与用户填写密码进行对比校验
    if user is None or not user.check_password(password):
        # 表示用户不存在, 或者用户密码校验错误
        # 如果验证失败, 记录错误次数, 返回错误信息
        try:
            redis_store.incr('access_nums_%s' % user_ip)
            redis_store.expire('access_nums_%s' % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg='用户或者密码错误')
    # 如果验证成功, 保存登录状态, 保存session中
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    # 4.返回结果
    return jsonify(errno=RET.OK, errmsg='登录成功')


@api.route('/session', methods=['GET'])
def check_login():
    '''检查登陆转态'''
    # 尝试从session中获取用户的名字
    name = session.get('name')
    # 如果session中存在name表示已登录, 否则未登录
    if name:
        # 表示登录了
        return jsonify(errno=RET.OK, errmsg='true', data={'name': name})
    else:
        # 表示未登录
        return jsonify(errno=RET.SESSIONERR, errmsg='false')


@api.route('/session', methods=['DELETE'])
def logout():
    '''登出'''
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg='OK')
