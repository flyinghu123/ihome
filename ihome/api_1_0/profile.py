#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-24 20:44:03
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from . import api
from flask import g, request, jsonify, current_app
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from ihome.utils.object_storage import CosCient
from ihome.models import User
from ihome import db, constants


@api.route('/users/avatar', methods=['POST'])
@login_required
def set_users_avatar():
    '''设置用户头像'''
    # 获取参数
    user_id = g.user_id
    # 获取图片
    image_file = request.files.get('avatar')

    # 校验参数
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    image_data = image_file.read()
    # 业务逻辑
    try:
        # 调用腾讯云对象存储
        cos = CosCient()
        file_name = cos.upload_file(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({'avatar_url': file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存图片信息失败')

    # 成功保存返回
    avatar_url = constants.TENG_XUN_FILE_URL_HEAD + file_name
    return jsonify(errno=RET.OK, errmsg='保存成功', data={'avatar_url': avatar_url})
