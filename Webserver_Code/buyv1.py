#-*-coding:utf-8-*-
#
#edit by adonis
#date: 2014-12-9
#describe: This file is used to search goods information for customers


import sae.const  #SAE const
import MySQLdb

from sqlInterface import *



def buyClick(fromuser):
    test = u'test' 
    con = Connect()
    res = ExecV(con,"select * from users where openID=%s",fromuser)
    #return test

    if res:   
        ress = ExecV(con,"update users set MainState=3 where openID=%s",fromuser)  #将当前微信状态设为商品购买填写状态
        res = ExecV(con,"select Goodsbuystate from users where openID=%s",fromuser)
        state = res[0][0]
        #首次选择购买
        if state == 0:
            
            mtext = u'在架上的物品有:\n'
            #return fromuser
            res = ExecV(con,"select count(*) from goods where sellerID!=%s and state=1",fromuser)
            #res = ExecV(con,"select count(name) from goods where state==1 and sellerID!=%s",fromuser)
            #return test
            num = res[0][0]
            #return num
            res = ExecV(con,"select name from goods where state=1 and sellerID!=%s",fromuser)
            #return num
            for i in range(0,num):
                mtext = mtext + res[i][0] + u'\n'
            mtext = mtext + u'请问您需要什么物品，请输入已有物品名称'
        #已输入购买物品名称，再次提示商品清单
        elif state == 1:
            res = ExecV(con,"select count(*) from buy where buyerID=%s",fromuser)
            num = res[0][0]
            if num > 0:   
                goodsID = ExecV(con,"select goodID from buy where buyerID=%s",fromuser)
                mtext = u''
                #return num
                for i in range(0,num):
                    goodID = goodsID[i][0]
                    res1 = ExecV(con,"select * from goods where goodID=%s",goodID)
                    mtext = mtext + u'序号:'+'%d' %res1[i][0]+u'\n'+u'名称:'+res1[i][2]+u'\n' + u'价格:'+'%.1f' %res1[i][3]+u'元\n'+ u'其他描述:'+res1[i][4] + u'\n\n'
                
                mtext1 = u'有' + '%d'%num +u'个符合条件的商品\n输入需要购买的物品序号（输入0则退出购买'
                #return mtext
                mtext = mtext + mtext1
                res = ExecV(con,"update users set Goodsbuystate=1 where openID=%s",fromuser)   
                
            else :
                mtext = u'抱歉，暂时没有您所需要的商品，欢迎下次光临～'    
                res = ExecV(con,"update users set Goodsbuystate=0 where openID=%s",fromuser)
                res = ExecV(con,"update users set MainState=0 where openID=%s",fromuser) 
        #未定义的输入
        else:
            mtext = u'非法输入'
    
    else:       #用户没有绑定，不在表中
        mtext = u'请先前往个人空间，进行身份绑定！'
    return mtext










