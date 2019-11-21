# -*- coding: utf-8 -*-

from . import api
from ihome import db, models
import logging


@api.route('/index')
def index():
    logging.error('error')
    logging.warn('warn')
    logging.info('info')
    logging.debug('debug')
    return 'index page'
