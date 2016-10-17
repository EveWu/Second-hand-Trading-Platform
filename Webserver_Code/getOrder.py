#-*-coding:utf-8-*-
#输入: 用户openID
#输出：多条查询数据，以换行符分隔，每个字段以|分隔。从左往右对应：商品id，卖家id，买家id，订单日期，订单状态，商品名称，商品价格，商品描述，卖家昵称，买家昵称
import sae.const  #引入sae的常量
import MySQLdb

import hashlib
import json
import web
import lxml
import time
import os
import urllib2,json
import datetime
from lxml import etree
from identityUnbinding import *
from sqlInterface import *


def getorder(fromuser):
    con = Connect()
    
    test = u'test'
    
    res = ExecV(con,"select count(*) from orders where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,sellerID,buyerID,startDate,state from orders where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    mtext = u''
    # get the ongoing orders
    for i in range(0,num):
        goodID = res[i][0]
        res1 = ExecV(con,"select name,price,description from goods where goodID=%s",goodID)
        if res1:
            sellerID = res[i][1]
            buyerID = res[i][2]
            startDate = res[i][3]
            state = res[i][4]
            #获得商品信息
            name = res1[0][0]
            price = res1[0][1]
            description = res1[0][2]
            #获得买家、卖家昵称
            #return test
            res1 = ExecV(con,"select nickname from users where openID=%s",sellerID)
            if res1:
                sellername = res1[0][0]
            else:
                sellername = u'can not tell'
            res1 = ExecV(con,"select nickname from users where openID=%s",buyerID)
            if res1:
                buyername = res1[0][0]
            else:
                buyername = u'can not tell'
            #将datetime类型转换成字符串类型
            date = datetime.datetime.ctime(startDate)
            mtext = mtext + u"|" + '%d' %goodID + u"|" + sellerID + u"|" + buyerID + u"|" + date + u"|" + '%d'%state + u"|" + name + u"|" + '%.1f'%price + u"|" + description + u"|" + sellername + u"|" + buyername +'\n' 
    # get the orders that already done
    res = ExecV(con,"select count(*) from orders_done where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,sellerID,buyerID,startDate from orders_done where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    #mtext = u''
    #return mtext
    state = 2
    for i in range(0,num):
        goodID = res[i][0]
        #return goodID
        res1 = ExecV(con,"select name,price,description from goods_done where goodID=%s",goodID)
        if res1:
            #return test
            sellerID = res[i][1]
            buyerID = res[i][2]
            startDate = res[i][3]
            #获得商品信息
            name = res1[0][0]
            price = res1[0][1]
            description = res1[0][2]
            #获得买家、卖家昵称
            #return test
            res1 = ExecV(con,"select nickname from users where openID=%s",sellerID)
            if res1:
                sellername = res1[0][0]
            else:
                sellername = u'can not tell'
            res1 = ExecV(con,"select nickname from users where openID=%s",buyerID)
            if res1:
                buyername = res1[0][0]
            else:
                buyername = u'can not tell'
            #将datetime类型转换成字符串类型
            date = datetime.datetime.ctime(startDate)
            mtext = mtext + u"|" + '%d' %goodID + u"|" + sellerID + u"|" + buyerID + u"|" + date + u"|" + '%d'%state + u"|" + name + u"|" + '%.2f'%price + u"|" + description + u"|" + sellername + u"|" + buyername +'\n' 
    


    return mtext
        