#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-19 23:23:34
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建flask的应用对象
app = create_app('develop')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
