#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-19 23:23:34
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from flask import Flask
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)


class Config(object):
    '''配置信息'''
    DEBUG = True
    SERECT_KEY = 'XJKLJKL*()++*&.DKFJALKJljfkljasdfj254325'

    # 数据库
    SQLALCHEMY_DATABASE_RUI = 'mysql+mysqlconnector://root:1152598046@localhost:3306/ihome?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask-session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据有效期, 单位秒


app.config.from_object(Config)

# 数据库
db = SQLAlchemy(app)

# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask-session, 将session数据保存在redis中
Session(app)

# 为flask补充csrf防护
CSRFProtect(app)


@app.route('/index')
def index():
    return 'index page'


if __name__ == '__main__':
    app.run()
