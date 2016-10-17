#-*-coding:utf-8-*-
#edit by eve
#date: 2014-12-30
#作用：查看用户订单状态是否发生改变，动态提醒用户
#输入：接受安卓定时发来的更新消息
#输出：Y1-有新的订单(卖家)
#     Y2-卖家确认订单(买家)
#	  S-买家确认收货，订单交易成功(卖家）
#	  N-没有更新
import sae.const  #引入sae的常量
import MySQLdb

import hashlib
import json
import web
import lxml
import time
import datetime
import os
import urllib2,json
from lxml import etree
from identityUnbinding import *
from sqlInterface import *

def hinttext(fromuser):
    con = Connect()
    duration = 3600
    test = u'test'
    mtext1 = u''
    mtext2 = u''
    mtext3 = u''
    mtext4 = u''
    #return test
    #查找作为卖家身份是否有新订单
    res = ExecV(con,"select count(*) from orders where sellerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate,state from orders where sellerID=%s",fromuser)
    #return test
    sell = 0
    for i in range(0,num):
        startDate = res[i][0]
        state = res[i][1]
        dif = (datetime.datetime.now() - startDate).seconds  #操作距离现在的时间
        if dif <= duration:
            #新的订单
            if state == 0:
                mtext1 = u'您有新的订单\n'
                sell = 1
                break
    #return test

    #查找作为买家身份,卖家是否确认订单
    res = ExecV(con,"select count(*) from orders where buyerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate,state from orders where buyerID=%s",fromuser)
    buy = 0
    for i in range(0,num):
        startDate = res[i][0]
        state = res[i][1]
        dif = (datetime.datetime.now() - startDate).seconds  #操作距离现在的时间
        if dif <= duration:
            #新的订单
            if state == 1:
                mtext2 = u'您的订单已经被卖家确认\n'
                buy = 1
                break       
    #return test
    #查找作为卖家身份是否有订单被买家确认
    res = ExecV(con,"select count(*) from orders_done where sellerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate from orders_done where sellerID=%s",fromuser)
    success = 0
    #return num
    for i in range(0,num):
        startDate = res[i][0]
        dif = (datetime.datetime.now() - startDate).seconds  #操作距离现在的时间
        #return test
        if dif <= duration:
            #新的订单
            mtext3 = u'您的订单交易成功\n'
            success = 1
            break
    #return test
    #没有任何更新
    #return buy
    if sell==0 and buy==0 and success==0:
        mtext4 = u'没有新消息\n'    
    mtext = mtext1 + mtext2 + mtext3 + mtext4
    return mtext
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    	
    