#coding:utf-8

import tornado.web
import json

class NginxHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        #post3种请求 
        #一：查   1：查所有key, 2根据key查value,5查所有key和value
        #二：改,增 3:根据key改value(如果key不存在则创建)
        #三：删 4:根据key名删key
        if action == "takebykey":
            #2:根据key取value
            key = self.get_argument('key','None')
            ips = self.application.db.hget("nginx",key) 
        
            if ips is None:
                msg = "not search result for your key!"
                json_result = {'error':msg}
                self.write(json.dumps(json_result))
            else:
                json_result = {'ips':ips}
                self.write(json.dumps(json_result))

        elif action == "takeallkey":
            #1：取所有key
            allkeys = self.application.db.hkeys("nginx")
            self.write(json.dumps({"allkeys":allkeys}))

        elif action == "changebykey":
            #3：根据key改value
            key = self.get_argument('key','None')
            ips = self.get_argument('ips','None')
            if key == "None" or ips == "None":
                self.write(json.dumps({"error":"need key and ips"}))
            else:
                self.application.db.hset("nginx",key,ips)
                self.write(json.dumps({"success":[{"key":key,"ips":ips}]}))
        elif action == "delbykey":
            #4：根据key名删key
            key = self.get_argument('key','None')
            #根据key检查reids中是否存在该key，如果存在则删除
            key_domain = self.application.db.hexists("nginx",key)
            if key_domain is True:
                r = self.application.db.hdel("nginx",key)
                msg = "The %s was del" % key
                json_result = {'succes':msg}
                self.write(json.dumps(json_result))
            else:
                msg = "The %s is not exist!" % key
                json_result = {'error':msg}
                self.write(json.dumps(json_result))

        elif action == "takeall":
            all = self.application.db.hgetall("nginx")
            self.write(json.dumps({"all":all}))
             
        else:
            msg = "bad action"
            self.write(json.dumps({"msg":msg}))


        

    def write_error(self, status_code, **kwargs):
        self.write(json.dumps({"error":status_code}))
