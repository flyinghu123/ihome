#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20 08:37:22
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$
from flask import Flask
from flask_session import Session
from flask_wtf import CSRFProtect
from config import config_map
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
import redis
import pymysql
pymysql.install_as_MySQLdb()


# 数据库
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None


# 日志
# 设置日志的记录等级
logging.basicConfig(level=logging.ERROR)  # 调试debug级
# 创建日志记录器,  指明日志的保存的路径, 每个日志的文件的最大大小, 保存日志文件个数上限
file_log_handler = RotatingFileHandler(filename='logs/log', maxBytes=1024 * 1024 * 10, backupCount=10)
# 创建日志记录的格式        日志等级 输入日志信息的文件名  行数  日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象 (flask app使用的) 添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    '''创建flask的应用对象
    Args:
        config_name str 配置模式名字  ('product', 'develop')
    Returns:
        app
    '''
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session, 将session数据保存在redis中
    Session(app)

    # 为flask补充csrf防护
    CSRFProtect(app)

    # 注册蓝图
    # 推迟导入, 避免之后视图函数导入db时出现循环导包
    from ihome import api_1_0

    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')

    return app
