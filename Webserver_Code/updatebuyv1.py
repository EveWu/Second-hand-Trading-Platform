#-*-coding:utf-8-*-
#edit by adonis
#date: 2014-12-10
#describe: This file is used to search goods information for customers and make the order list
import sae.const  #引入sae的常量
import MySQLdb

import hashlib
import json
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
from identityUnbinding import *
from sqlInterface import *


def updatebuy(content,fromuser):    

    test = u'test' 
    con = Connect()
    res = ExecV(con,"select Goodsbuystate from users where openID=%s",fromuser)  
    text=res[0][0]
    if res:  
        if text == 0:  #未输入要求物品
            #return test
            res1 = ExecV(con,"select count(*) from goods where name=%s and sellerID!=%s and state=1",[content,fromuser])
            num = res1[0][0]
            if num > 0:   
                #得到所有符合要求的商品记录
                res1 = ExecV(con,"select * from goods where name=%s and sellerID!=%s and state=1",[content,fromuser])
                mtext = u''
                #遍历输出信息
                for i in range(0,num):
                    #goodID = u'' + '%d'%res1[i][0]
                    goodID = res1[i][0]
                    #将数据插入表，由于将整型的goodsID插入表报错，所以采用先插入buyerID，之后根据最新插入buyerID对应的buyID来插入goodsID
                    res2 = ExecV(con,"insert into buy (buyerID) values(%s)",fromuser)
                    res2 = ExecV(con,"select max(buyID) from buy where buyerID=%s",fromuser)
                    ID = res2[0][0]
                    res2 = ExecV(con,"update buy set goodID=%s where buyID=%s",[goodID,ID])
                    mtext = mtext + u'序号:'+'%d' %res1[i][0]+u'\n'+u'名称:'+res1[i][2]+u'\n' + u'价格:'+'%.1f' %res1[i][3]+u'元\n'+ u'其他描述:'+res1[i][4] + u'\n\n'
                    
                
                mtext1 = u'有' + '%d'%num +u'个符合条件的商品\n输入需要购买的物品序号（输入0则退出购买）'
                #return mtext
                mtext = mtext + mtext1
                res = ExecV(con,"update users set Goodsbuystate=1 where openID=%s",fromuser)   
                
            else :
                mtext = u'抱歉，暂时没有您所需要的商品，欢迎下次光临～'    
                res = ExecV(con,"update users set Goodsbuystate=0 where openID=%s",fromuser)
                res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser) 
        
        elif text == 1: #第二步
            #取消订单
            if content == '0':  
                res = ExecV(con,"delete from buy where buyerID=%s",fromuser)
                res = ExecV(con,"update users set MainState=0,Goodsbuystate=0 where openID=%s",fromuser)
                #res = ExecV(con,"update users set Goodsbuystate=0 where openID=%s",fromuser)
                mtext = u'谢谢您的光临 欢迎下次再来选购'  
            #检查输入，创建订单
            else:
                valid = 1
                try:
                    int(content)
                    res = ExecV(con,"select * from buy where buyerID=%s and goodID=%s",[fromuser,content])
                    # create a new order
                    if res:
                        res = ExecV(con,"delete from buy where buyerID=%s",fromuser)
                        res = ExecV(con,"insert into orders (buyerID) values(%s)",fromuser)
                        res = ExecV(con,"select max(orderID) from orders where buyerID=%s",fromuser)
                        orderID = res[0][0]
                        res = ExecV(con,"select sellerID from goods where goodID=%s",content)
                        seller = res[0][0]
                        res = ExecV(con,"update goods set state=0 where goodID=%s",content)
                        res = ExecV(con,"update orders set goodID=%s,sellerID=%s where orderID=%s",[content,seller,orderID])
                        res = ExecV(con,"update users set Goodsbuystate=0 where openID=%s",fromuser)
                        res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser)
                    else:
                        valid = 0
                       
                except:
                    valid = 0
                # input not valid, should be integer
                if valid == 0:
                    mtext2 = u'输入不符合要求，请输入现有商品的序号!\n\n'
                    res = ExecV(con,"select count(*) from buy where buyerID=%s",fromuser)
                    num = res[0][0]
                    #return num
                    if num > 0:
                        goodsID = ExecV(con,"select goodID from buy where buyerID=%s",fromuser)
                        mtext = u''
                        #return test
                        for i in range(0,num):
                            goodID = goodsID[i][0]
                            res1 = ExecV(con,"select * from goods where goodID=%s",goodID)
                            mtext = mtext + u'序号:'+'%d' %res1[i][0]+u'\n'+u'名称:'+res1[i][2]+u'\n' + u'价格:'+'%.1f' %res1[i][3]+u'元\n'+ u'其他描述:'+res1[i][4] + u'\n\n'
                        mtext1 = u'有' + '%d'%num +u'个符合条件的商品\n输入需要购买的物品序号（输入0则退出购买）'
                        mtext = mtext2 + mtext + mtext1
                        #res = ExecV(con,"update users set Goodsbuystate=1 where openID=%s",fromuser)
            	    else:
                        mtext = u'抱歉，暂时没有您所需要的商品，欢迎下次光临～' 
                        res = ExecV(con,"update users set Goodsbuystate=0 where openID=%s",fromuser)
                        res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser) 
                else:
                    mtext=u'已下单，请等待卖家确认'

    else:       #用户没有绑定，不在表中
        mtext = u'请先前往个人空间，进行身份绑定！'
    return mtext

