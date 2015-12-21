#coding:utf-8

import tornado.web
import json
#from model.entity import Entity

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #entity = Entity.get('ryan\'s blog')
        #self.render('index.html', entity = entity)
        self.write(json.dumps({"msg":"Your know for xxoo"}))
