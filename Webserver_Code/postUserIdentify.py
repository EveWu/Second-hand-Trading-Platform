#-*-coding:utf-8-*-

# anthor:     Xiang xiyun
# date:       2014-11-28
# describe:   This file is used to post the identity of the user to others when
#             they want to buy or sale things.

import sae.const  #引入sae的常量
import MySQLdb

from sqlInterface import *
    
def postUserIdentify(User):

    con = Connect()
    name = ExecV(con,"select nickname from users where openID=%s",User)
    
    return name
    
   




