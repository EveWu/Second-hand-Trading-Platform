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



def sellClick(fromuser):
    test = u'test'
    #return test
    con = Connect()
 	#return test
    
    res = ExecV(con,"select GoodsSellState from users where openID=%s",fromuser)

    if res:   
        ress = ExecV(con,"update users set MainState=2 where openID=%s",fromuser)  #将当前微信状态设为商品上架填写状态
        
        mtext1 = u''
        
        text = res[0][0]
        if text == 0:      #新商品
            res = ExecV(con,"insert into goods (sellerID) values(%s)",fromuser) 
            #res = ExecV(con,"update users set GoodsSellState=1 where openID=%s",fromuser)
            getgoodID = ExecV(con,"select max(goodID) from goods where sellerID=%s",fromuser) 
            goodID = getgoodID[0][0]
            
            res = ExecV(con,"update users set GoodsSellState=1, latest_goodID=%s where openID=%s",[goodID,fromuser])
            mtext2 = u'请输入商品名称描述（这会显示在您的商品名称中，为了搜索结果的有效性，请尽量详细填写所有可能的名称［不超过30字］）'
        elif text <= 3:    #未完成上架的商品
            mtext1 = u'请继续填写上架信息\n'
            if text == 1:
                mtext2 = u'请输入商品名称描述（这会显示在您的商品名称中，为了搜索结果的有效性，请尽量详细填写所有可能的名称［不超过30字］）'
                
            elif text == 2:
                mtext2 = u'请输入商品价格'
                
            elif text == 3:
                mtext2 = u'关于商品的其他描述［不超过200字］'
        mtext = mtext1+mtext2
            #elif text == 5:
            #    mtext2 = u'上传商品图片2'
            #elif text == 6:
            #    mtext2 = u'上传商品图片3'
            #######
        
    else:       #用户没有绑定，不在表中
        mtext = u'请先前往个人空间，进行身份绑定！'
    return mtext


    