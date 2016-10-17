#-*-coding:utf-8-*-
import sae.const  #引入sae的常量
import MySQLdb
import re
import hashlib
import json
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
from identityUnbinding import *
from identityBinding import *
from sqlInterface import *
#add by chenzh for dealing with customer's text operatation    
def textmanage(content):
    Database={'1':u"自行车",'2':u"车",'3':u"书",'4':u"衣服"}
    #content='n'
    #content=u'需要买一辆自行车'
    message=content.encode('utf8')
    if (re.search(Database['1'].encode('utf8'),message)):
        mtext=(re.search(Database['1'].encode('utf8'),message).group())
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'抱歉！您需要的'+mtext+u"暂时还没有被摆上货架" )              
    elif (re.search(Database['2'].encode('utf8'),message)):
        mtext=(re.search(Database['2'].encode('utf8'),message).group())
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'抱歉！您需要的'+mtext+u"暂时还没有被摆上货架"  ) 
    elif (re.search(Database['3'].encode('utf8'),message)):
        mtext=(re.search(Database['3'].encode('utf8'),message).group())
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'抱歉！您需要的'+mtext+u"暂时还没有被摆上货架"  ) 
    elif (re.search(Database['4'].encode('utf8'),message)):
        mtext=(re.search(Database['4'].encode('utf8'),message).group())
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'抱歉！您需要的'+mtext+u"暂时还没有被摆上货架"  )     
    else:
        return self.render.reply_text(fromUser,toUser,int(time.time()),u"抱歉 您所需要的货物暂时未上架")

