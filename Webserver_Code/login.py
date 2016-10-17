#-*-coding:utf-8-*-
#
#edit by adonis
#date: 2014-12-29
#describe: This file is a subfunction to realize log_in


import sae.const  #引入sae的常量
import MySQLdb

from sqlInterface import *



def login(xml):
    phone = xml.find("Phone").text
    code = xml.find("Code").text
    phone = phone.encode('utf-8') 
    code = code.encode('utf-8')
    test = phone+'\n'+code
    #return self.render.reply_text(fromUser,toUser,int(time.time()), test)
    res = ExecV(con,"select openID, password from users where phone=%s",phone)
    #return self.render.reply_text(fromUser,toUser,int(time.time()), test)
    if res:
        openID = res[0][0]
        text_code = res[0][1]
        if text_code == code:
            mtext = u""+openID              
        else:
            mtext = u"N\n"
    else:
        mtext = u"N\n"
        
    return mtext