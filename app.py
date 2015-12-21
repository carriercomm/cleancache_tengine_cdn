#coding:utf-8
from urls import urls
import tornado.web
import os
import redis

class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls
        
        #redis连接池
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.db = redis.Redis(connection_pool=pool)

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"), 
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )

        tornado.web.Application.__init__(self,handlers,**settings)
        
app = Application()
