#-*-coding:utf-8-*-
#edit by eve
#date: 2014-12-30
#fuction: check whether the user's orders have changed
#input: user openID
#output: Y1--new orders
#		 Y2--seller has confirmed the order
#        S---order is done
#        N---no news

import sae.const  
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

def hint(fromuser):
    con = Connect()
    test = u'test'
    mtext1 = u''
    mtext2 = u''
    mtext3 = u''
    mtext4 = u''
    #check new orders
    res = ExecV(con,"select count(*) from orders where sellerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate,state from orders where sellerID=%s",fromuser)
    sell = 0
    for i in range(0,num):
        startDate = res[i][0]
        state = res[i][1]
        dif = (datetime.datetime.now() - startDate).seconds  #time measure
        if dif <= duration:
            #new orders
            if state == 0:
                mtext1 = u'Y1\n'
                sell = 1
                break

    #check whether seller has confirmed the order
    res = ExecV(con,"select count(*) from orders where buyerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate,state from orders where buyerID=%s",fromuser)
    buy = 0
    for i in range(0,num):
        startDate = res[i][0]
        state = res[i][1]
        dif = (datetime.datetime.now() - startDate).seconds  #time measure
        if dif <= duration:
            #confirm orders
            if state == 1:
                mtext2 = u'Y2\n'
                buy = 1
                break       
    #check whether orders are done
    res = ExecV(con,"select count(*) from orders_done where sellerID=%s",fromuser)
    num = res[0][0]
    res = ExecV(con,"select startDate from orders_done where sellerID=%s",fromuser)
    success = 0
    for i in range(0,num):
        startDate = res[i][0]
        dif = (datetime.datetime.now() - startDate).seconds  #time measure
        if dif <= duration:
            #done
            mtext3 = u'S\n'
            success = 1
            break
    #no news
    if ~sell and ~buy and ~success:
        mtext4 = u'N\n'    
    mtext = mtext1 + mtext2 + mtext3 + mtext4
    return mtext
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    	
    