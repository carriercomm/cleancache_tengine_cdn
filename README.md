##清缓存接口说明：

### 一：清理接口（get请求）：
------
      1：清理nginx(cleartype=nginx)
      http://127.0.0.1:8009/clear?cleartype=nginx&url=http://www.xxx.com/index.html

      2:清理akamai(cleartype=akamai)
      http://127.0.0.1:8009/clear?cleartype=akamai&url=http://xxx/index.html

      3:同时清理akamai和nginx(cleartype=nginxakamai)
      http://127.0.0.1:8009/clear?cleartype=nginxakamai&url=http://www.xxx.com/index.html


### 二：维护域名对应nginx的IP列表（post请求，暂未加入认证）：
------
      接口地址：http://127.0.0.1:8009/nginx
      1：查询所有域名
      action=takeallkey
    
      2：根据域名查询对应IP
      action=takebykey&key=www.test.com

      3：根据域名修改IP
      action=changebykey&key=www.test.com&ips=127.0.0.1

      4: 根据域名删除key
      action=delbykey&key=www.test.com

