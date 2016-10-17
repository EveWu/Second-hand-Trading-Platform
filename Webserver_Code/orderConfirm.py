#-*-coding:utf-8-*-
#作用: 处理买家和卖家的订单确认请求
#输入: 用户openID，商品goodID
#输出: Y-确认成功
#	  N-非法操作，例如:  1 买家确认等待卖家确认的订单(state=0)
#					   2 卖家确认等待买家确认的订单(state=1)
#					   3 订单不存在或订单中商品和用户信息不匹配
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


def orderconfirm(fromuser,goodID):
    con = Connect()
    
    test = u'test'
    mtext = u'N\n'
    res = ExecV(con,"select state, sellerID, buyerID from orders where goodID=%s",goodID)
    state = res[0][0]
    sellerID = res[0][1]
    buyerID = res[0][2]
    #return state
    #等待卖家确认
    if state == 0:
        
        #用户为卖家
        if sellerID == fromuser:
            res = ExecV(con,"update orders set state=1 where goodID=%s",goodID)
            mtext = u'Y\n'
    #等待买家确认
    elif state == 1:
        #用户为买家
        #return fromuser
        if buyerID == fromuser:
            res = ExecV(con,"select * from goods where goodID=%s",goodID)
            #取出商品信息
            #return test
            name = res[0][2]
            price = res[0][3]
            description = res[0][4]

            #return test
            #将订单放入交易成功订单表
            #res2 = ExecV(con,"insert into buy (buyerID) values(%s)",fromuser)
            res = ExecV(con,"insert into orders_done (sellerID,buyerID) values(%s,%s)",[sellerID,buyerID])
            #return test
            res = ExecV(con,"select max(doneID) from orders_done where sellerID=%s",sellerID)
            #res = Execv(con,"select max(doneID) from orders_done where sellerID=%s",sellerID)
            doneID = res[0][0]
            #return doneID
            res = ExecV(con,"update orders_done set goodID=%s where doneID=%s",[goodID,doneID])
            #res = ExecV(con,"update orders_done set goodID=%s where doneID=%s",[goodID,doneID])
            
            #return test
            #将商品放入已售商品表中
            res = ExecV(con,"insert into goods_done (sellerID,name,description) values(%s,%s,%s)",[sellerID,name,description])
            #return test
            res = ExecV(con,"select max(doneID) from goods_done where sellerID=%s",sellerID)
            #res = Execv(con,"select max(doneID) from orders_done where sellerID=%s",sellerID)
            doneID = res[0][0]
            #return doneID
            res = ExecV(con,"update goods_done set goodID=%s,price=%s where doneID=%s",[goodID,price,doneID])
            #从正在进行的订单表删除订单
            res = ExecV(con,"delete from orders where goodID=%s",goodID)
            #从在架上的商品表删除商品信息
            res = ExecV(con,"delete from goods where goodID=%s",goodID)
            mtext = u'Y\n'
    else:
        mtext = u'N\n'
    return mtext
            

           
                    