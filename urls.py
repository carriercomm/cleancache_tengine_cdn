#coding:utf-8
from handlers.index import MainHandler
from handlers.clear import ClearHandler
from handlers.base import BaseHandler
from handlers.nginx import NginxHandler

urls = [
    (r'/', MainHandler),
    (r'/clear', ClearHandler),
    (r'/nginx', NginxHandler),
    (r'.*', BaseHandler),
]
