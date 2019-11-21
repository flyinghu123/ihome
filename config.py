#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20 08:21:22
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

import redis


class Config(object):
    '''配置信息'''
    SECRET_KEY = 'XJKLJKL*()++*&.DKFJALKJljfkljasdfj254325'

    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1152598046@localhost:3306/ihome?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = '1152598046'

    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据有效期, 单位秒


class DevlopmentConfig(Config):
    '''开发模式的配置信息'''
    DEBUG = True


class ProductionConfig(Config):
    '''生产环境配置信息'''
    DEBUG = False


# 映射关系
config_map = {
    'product': ProductionConfig,
    'develop': DevlopmentConfig
}
