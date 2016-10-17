#-*-coding:utf-8-*-
#
#change by Xiangxiyun
#edit by eve
#date: 2014-11-30
#describe: This file is used to bind the users
#

import sae.const  #引入sae的常量
import MySQLdb

from sqlInterface import *



def bindingIdentity(fromuser):
    
    con = Connect()
 
    res = ExecV(con,"select IDBindingState from users where openID=%s",fromuser)
    
    if res:                                                         
        mtext1 = u''
        text = res[0][0]
        
        if text <= 7:
            mtext1 = u"你的绑定信息填写不完整，请继续填写\n"

            
        #if text == 0:               
        #    mtext2 = u'请输入学号'
        #用户在文本输入进行身份绑定中途，点击身份绑定按钮
        if text == 1:    
            mtext2 = u'请输入学号'
        elif text == 2:             
            mtext2 = u'请输入真实姓名'
        elif text == 3:
            mtext2 = u'请输入昵称'
        elif text == 4:
            mtext2 = u'请输入性别'
        elif text == 5:
            mtext2 = u'请输入学院名称'
        elif text == 6:
            mtext2 = u'请输入手机号码'
        elif text == 7:
            mtext2 = u'请输入交易密码'      
        else:
            mtext2 = u'您的身份已经绑定，无需重复绑定'
        #mtext = mtext1+mtext2
        mtext = mtext2
    #用户第一次进入身份绑定
    else:
        res = ExecV(con,"insert into users (openID) values(%s)",fromuser)         #放入用户数据库               
        res = ExecV(con,"update users set IDBindingState=1 where openID=%s",fromuser)         #已绑定openID
        mtext = u'请输入学号!'
                        
    res = ExecV(con,"update users set MainState=1 where openID=%s",fromuser)  #将当前微信状态设为身份绑定状态
    return  mtext
     