#coding:utf-8

import tornado.ioloop
import tornado.httpserver
import sys
from app import app


PORT = '8009'
ADDR = '0.0.0.0'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(PORT,address=ADDR)
    print 'Development server is running at http://%(addr)s:%(port)s/' % {'addr':ADDR,'port':PORT}
    print 'Quit the server with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
