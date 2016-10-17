# coding: UTF-8  python文件的编码是UTF-8
import os

import sae
import web
import pylibmc
import sys
sys.modules['memcache'] = pylibmc

from weixinInterface import WeixinInterface
from UpdateDatabase import UpdateDb

urls = (
    '/weixin','WeixinInterface',
    '/update','UpdateDb',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)