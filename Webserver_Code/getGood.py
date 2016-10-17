#-*-coding:utf-8-*-
# edited by eve
# date: 2014-12-31
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


def getgood(fromuser):
    con = Connect()
    
    test = u'test'
    
    res = ExecV(con,"select count(*) from goods where sellerID=%s",fromuser)
    num = res[0][0]
    #return num
    res = ExecV(con,"select goodID,name,price,description,startDate,state from goods where sellerID=%s",fromuser)
    mtext = u''
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
        mtext = mtext + u"|" + '%d' %goodID + u"|" + '%d'%state + u"|" + name + u"|" + '%.2f'%price + u"|" + description + u"|" + date + u'\n'

    return mtext
        