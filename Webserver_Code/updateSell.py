#-*-coding:utf-8-*-
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


def updatesell(content,fromuser):    
    test = u'test'

    con = Connect()

    res = ExecV(con,"select GoodsSellState from users where openID=%s",fromuser)
    
    if res:                                                         
        mtext1 = u''
        text = res[0][0]
        #return text
        if text == 0:      #新商品
            
            res = ExecV(con,"insert into goods (sellerID) values(%s)",fromuser) 
            res = ExecV(con,"update users set GoodsSellState=1 where openID=%s",fromuser)
            mtext2 = u'请输入商品名称描述（这会显示在您的商品名称中，为了搜索结果的有效性，请尽量详细填写所有可能的名称［不超过30字］）'
        elif text <= 3:    #未完成上架的商品
            
            
            if text == 1:
                #return content
                #return fromuser
                mtext1 = u'请继续填写上架信息\n'
                getgoodID = ExecV(con,"select latest_goodID from users where openID=%s",fromuser)
                goodID = getgoodID[0][0]
                res = ExecV(con,"update goods set name=%s where goodID=%s",[content,goodID])                
                res = ExecV(con,"update users set GoodsSellState=2 where openID=%s",fromuser)
                #return test
                mtext2 = u'请输入商品价格'

            elif text == 2:
                mtext1 = u'请继续填写上架信息\n'
                try:
                    float(content)
                    #return cont
                    getgoodID = ExecV(con,"select latest_goodID from users where openID=%s",fromuser)
                    goodID = getgoodID[0][0]
                    res = ExecV(con,"update goods set price=%s where goodID=%s",[content,goodID])
                    res = ExecV(con,"update users set GoodsSellState=3 where openID=%s",fromuser)
                    mtext2 = u'关于商品的其他描述［不超过200字］' 
                    #return u'float or int'
                except:
                    mtext2 = u'价格必须是整数或是小数，不能包含除小数点以外的字母。请重新输入商品价格'
               
            
                #return content
            
           #     res = ExecV(con,"update goods set price=%f where userOpenID=%s",[content,fromuser])
           #     res = ExecV(con,"update users set GoodsSellState=3 where openID=%s",fromuser)
           #     mtext2 = u'请输入商品新旧程度，0-10的整数'
            #elif text == 3:
                
            #    res = ExecV(con,"update goods set condition=%s where userOpenID=%s",[content,fromuser])
            #    return test
            #    res = ExecV(con,"update users set GoodsSellState=4 where openID=%s",fromuser)
            #    mtext2 = u'关于商品的其他描述［不超过200字］' 

                
            elif text == 3:
                #return 1
                getgoodID = ExecV(con,"select latest_goodID from users where openID=%s",fromuser)
                #return 2
                goodID = getgoodID[0][0]
                #return 3
                res = ExecV(con,"update goods set description=%s,state=1 where goodID=%s",[content,goodID])
                #return 4
                res = ExecV(con,"update users set GoodsSellState=0 where openID=%s",fromuser)
                res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser)
                mtext2 = u'商品上架成功！'
            ############
            #elif text == 5:
            #    mtext2 = u'上传商品图片2'
            #elif text == 6:
            #    mtext2 = u'上传商品图片3'
            ###################
        mtext = mtext1+mtext2
    else:       #用户没有绑定，不在表中
        mtext = u'请先前往个人空间，进行身份绑定！'
    return mtext


    