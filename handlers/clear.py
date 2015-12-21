#coding:utf-8

from urlparse import urlparse
import tornado.web
#import tornado.httpclient
import time
import json
#import urllib
import requests
from bs4 import BeautifulSoup
import re


class ClearHandler(tornado.web.RequestHandler):
    #@tornado.web.asynchronous
    def get(self):
        cleartype = self.get_argument('cleartype','None')
        url = self.get_argument('url','None')

        #三种类型 nginx akamai nginxakamai
        #1.nginxakamai 同时清理
        if cleartype == "nginxakamai":
            nginxmsg = self.clearnginx(url)
            akamaimsg = self.clearakamai(url)
            json_result = {"nginx":nginxmsg,"akamai":akamaimsg}
            self.write(json.dumps(json_result))

        #2.nginx 单独清理nginx
        elif cleartype == "nginx": 
            msg = self.clearnginx(url)
            json_result = {"nginx":msg}
            self.write(json.dumps(json_result))

        #3.akamai
        elif cleartype == "akamai": 
            msg = self.clearakamai(url)
            json_result = {"akamai":msg}
            self.write(json.dumps(json_result))

        #4.没有对应的类型则错误
        else:
            #self.set_status(404)
            msg = "bad cleartype"
            json_result = {"msg":msg}
            self.write(json.dumps(json_result))
                
    def clearnginx(self,url):
        hostname = urlparse(url).hostname
        if hostname is None:
            message = "%s is a valid url" % url
            return message

        #获取url后缀
        schemelen = len(urlparse(url).scheme)
        hostnamelen = len(hostname)
        urlpath = url[schemelen+hostnamelen+3:]
        if urlpath == '':
            urlpath = '/'

         
        ipstrs = self.application.db.hget("nginx",hostname)
        if ipstrs is None:
            message = "not search result for your url!"
            json_result = {'status':'error','message':message}
            self.write(json.dumps(json_result))
        else:
            #client = tornado.httpclient.AsyncHTTPClient()
            #先用同步阻塞方法完成
            message = ""
            ips = ipstrs.split(',')
            for ip in ips:
                headers = {'host':hostname}
                purgeurl = "http://"+ip+"/purge"+urlpath
                rhtml = requests.get(purgeurl,headers=headers)
                httpStatus = str(rhtml.status_code)
                soup = BeautifulSoup(str(rhtml.text).replace("\r\n",""),"html.parser")
                key = str(soup.find_all(text=re.compile("Key")))
                path =  str(soup.find_all(text=re.compile("Path")))
                title = str(soup.title)
                message += " nginx_ip : %s ,httpStatus : %s ,title : %s ,key : %s ,path : %s "  % (ip,httpStatus,title,key,path)
            return message
                


    def clearakamai(self,url):
        hostname = urlparse(url).hostname
        if hostname is None:
            message = "%s is a valid url" % url
            return message
        
        #执行akamai clear cdn cache 同步阻塞方法
        headers = {'content-type': 'application/json'}
        data = '{"objects":["%s"]}' % url
        apiurl = self.application.db.hget("akamai","apiurl")
        akamaiusername = self.application.db.hget("akamai","username")
        akamaipassword = self.application.db.hget("akamai","password")
        message = (requests.post(apiurl,data=data,headers=headers,auth=(akamaiusername, akamaipassword))).text
        return message
        

    def logs(self):
        pass
    def on_response(self, response):
        pass
