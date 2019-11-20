# -*- coding: utf-8 -*-

from . import api


@api.route('/index')
def index():
    return 'index page'
