# -*-coding:utf-8-*-
# edit by eve
# date: 2014-12-31
# function: delete orders or goods
# input: fromuser, goodID, opt
#	opt value: 0--delete onsell goods
#			   1--delete ongoing orders
#			   
# output: 
#	Y--delete success
#   N--delete failed due to invalid operation

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

def delete(fromuser,goodID,opt):
    con = Connect()
    mtext = u'Y\n'
    if opt == '0':
        res = ExecV(con,"select * from goods where sellerID=%s and goodID=%s",[fromuser,goodID])
        if res:
            res = ExecV(con,"delete from goods where sellerID=%s and goodID=%s",[fromuser,goodID])
            res = ExecV(con,"delete from orders where goodID=%s",goodID)
        else:
            mtext = u'N\n'
    elif opt == '1':
        res = ExecV(con,"select * from orders where (sellerID=%s or buyerID=%s) and goodID=%s",[fromuser,fromuser,goodID])
        if res:
            res = ExecV(con,"delete from orders where (sellerID=%s or buyerID=%s) and goodID=%s",[fromuser,fromuser,goodID])
            res = ExecV(con,"update goods set state=1 where goodID=%s",goodID)
        else:
            mtext = u'N\n'

    else:
        mtext = u'N\n'
    
    return mtext
    
    