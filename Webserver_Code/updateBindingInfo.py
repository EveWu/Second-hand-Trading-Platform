#-*-coding:utf-8-*-
#
#change by Xiangxiyun
#edit by eve
#date: 2014-11-30
#describe: This file is used to update the users' info in the database
#



import MySQLdb

from sqlInterface import *


def updateBindingInfo(content,fromuser):
    con = Connect()
    rres = ExecV(con,"select IDBindingState from users where openID=%s",fromuser)

    if rres:
        tex = rres[0][0]

        if tex == 1:           #当前输入为学号
            res = ExecV(con,"update users set sID=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=2 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入真实姓名'   #提示下一步操作
        elif tex == 2:         #当前输入为真实姓名
            res = ExecV(con,"update users set t_name=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=3 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入昵称'
        elif tex == 3:         #当前输入为昵称
            res = ExecV(con,"update users set nickname=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=4 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入性别（数字）：0 男， 1 女'
        elif tex == 4:         #当前输入为性别
            res = ExecV(con,"update users set sex=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=5 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入所在学院名称'
        elif tex == 5:         #当前输入为学院
            res = ExecV(con,"update users set college=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=6 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入手机号码'
        elif tex == 6:			#当前输入为手机号
            res = ExecV(con,"update users set phone=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=7 where openID=%s",fromuser) #更新绑定信息
            mtext = u'请输入交易密码'
        elif tex == 7:			#当前输入为密码
            res = ExecV(con,"update users set password=%s where openID=%s",[content,fromuser])
            res = ExecV(con,"update users set IDBindingState=8 where openID=%s",fromuser) #更新绑定信息
            mtext = u'身份绑定成功！'
            res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser) #回到一般状态
        else:                  #未进入绑定或已经绑定
            mtext = u'无需绑定'
            res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser) #回到一般状态
    return mtext