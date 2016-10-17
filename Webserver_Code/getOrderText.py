#-*-coding:utf-8-*-
# input: openID
# output: orders
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


def getordertext(fromuser):
    con = Connect()
    
    test = u'test'
    mtext = u'正在进行的购买商品订单：\n'
    res = ExecV(con,"select count(*) from orders where buyerID=%s",fromuser)
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,sellerID,buyerID,startDate,state,orderID from orders where buyerID=%s",fromuser)
    # get the ongoing orders
    for i in range(0,num):
        goodID = res[i][0]
        res1 = ExecV(con,"select name,price,description from goods where goodID=%s",goodID)
        if res1:
            sellerID = res[i][1]
            buyerID = res[i][2]
            startDate = res[i][3]
            state = res[i][4]
            orderID = res[i][5]
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
            mtext = mtext + u'订单序号: %d'%orderID + u'\n日期: ' + date + u'\n名称: ' + name + u'\n价格: ' + '%.2f'%price + u'\n描述: ' + description + u'\n卖家昵称: ' + sellername  +'\n\n'

    mtext = mtext + u'正在进行的购买商品订单：\n'       
    res = ExecV(con,"select count(*) from orders where sellerID=%s",fromuser)
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,sellerID,buyerID,startDate,state,orderID from orders where sellerID=%s",fromuser)
    # get the ongoing orders
    for i in range(0,num):
        goodID = res[i][0]
        res1 = ExecV(con,"select name,price,description from goods where goodID=%s",goodID)
        if res1:
            sellerID = res[i][1]
            buyerID = res[i][2]
            startDate = res[i][3]
            state = res[i][4]
            orderID = res[i][5]
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
            mtext = mtext + u'订单序号: %d'%orderID + u'\n日期: ' + date + u'\n名称: ' + name + u'\n价格: ' + '%.2f'%price + u'\n描述: ' + description + u'\n卖家昵称: ' + sellername  +'\n\n'

            
    # get the orders that already done
    res = ExecV(con,"select count(*) from orders_done where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,sellerID,buyerID,startDate from orders_done where buyerID=%s or sellerID=%s",[fromuser,fromuser])
    #mtext = u''
    #return mtext
    mtext = mtext + u'\n已成交订单：\n'
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
            mtext = mtext + u'日期: ' + date + u'\n名称: ' + name + u'\n价格: ' + '%.2f'%price + u'\n描述: ' + description + u'\n卖家昵称: ' + sellername  +'\n\n'
            
    


    return mtext
        