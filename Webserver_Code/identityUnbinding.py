#-*-coding:utf-8-*-
#
#change by Xiangxiyun
#edit by eve
#date: 2014-11-30
#describe: This file is used to unbinding the user and delete their info
#

import sae.const  #引入sae的常量
import MySQLdb

from sqlInterface import *

def unbindingIdentity(fromuser): 
    con = Connect()
    
    res = ExecV(con,"select * from users where openID=%s",fromuser)    #查询是否已经绑定 
    
    if res:
        #return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        res = ExecV(con,"delete from users where openID=%s",fromuser)  #删除记录
        mtext = u"解除绑定成功！"
    else:
        mtext = u'身份未绑定！'
        
    return mtext
        

