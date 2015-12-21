#coding:utf-8

import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            #self.render('public/404.html')
            self.write(json.dumps({"access":"404"}))
        elif status_code == 500:
            self.write(json.dumps({"access":"500"}))
        else:
            self.write('error:' + str(status_code))
