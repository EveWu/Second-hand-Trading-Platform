#-*-coding:utf-8-*-
# edited by eve
# date: 2014-12-31
# function: check goods
# input: user openID
# output: user's own goods
#	from left to right, it is corresponding to goodID,state,name,price,description,startDate
#		state value 0: not available
#                   1: onsell
import sae.const  
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


def getgoodtext(fromuser):
    con = Connect()
    
    test = u'test'
    
    res = ExecV(con,"select count(*) from goods where sellerID=%s",fromuser)
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,name,price,description,startDate,state from goods where sellerID=%s",fromuser)
    mtext = u'您现在在售的商品有：\n'
    #return test
    for i in range(0,num):
        # get goods' information
        goodID = res[i][0]
        name = res[0][1]
        price = res[0][2]
        description = res[0][3]
        startDate = res[0][4]
        state = res[0][5]
        # change the datetime type to string type
        date = datetime.datetime.ctime(startDate)
        mtext = mtext + u'日期: ' + date + u'\n商品序号:%d'%goodID + u'\n名称: ' + name + u'\n价格: ' + '%.2f'%price + u'\n描述: ' + description +'\n\n'

    return mtext
        