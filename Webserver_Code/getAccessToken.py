#-*-coding:utf-8-*-

# anthor:     Xiang xiyun
# date:       2014-11-28
# describe:   This file is used to get the access_token regularly from wechat

import sae.const  #引入sae的常量
import urllib2
import json
import pylibmc as memcache

mc = memcache.Client()

token = mc.get("token")
if token == None:
    appid = "wxe1abdf23e3b46c20"
    secret = "4c4c57e68e0e1552f18fb22f23e2a29d"
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
    response = urllib2.urlopen(url)
    html = response.read()
    tokeninfo = json.loads(html)
    token = tokeninfo['access_token']
    #set access_token into memcache, do not compress, expires_in 7100 seconds incase error
    mc.set("token", token, 0, 7100)
    token = mc.get("token")