# -*- coding: utf-8 -*-
#encoding=utf-8
import hashlib
import json
import web
import lxml
import time
import os
import urllib2,json
import sae.const  #引入sae的常量
from lxml import etree

#sql control
from sqlInterface import *

#身份绑定
from identityBinding import *
from identityUnbinding import *
from updateBindingInfo import *
#商品上架
from sell import *
from updateSell import *
#商品购买
from buyv1 import *
from updatebuyv1 import *
# get orders
from getOrder import *
from getOrderText import *
#定时查看订单是否变化
from Hint import *
from hintText import *
#确认订单
from orderConfirm import *
# get goods
from getGood import *
from getGoodText import *
# delete goods or orders
from Delete import *


class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        
    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="myexgood" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def POST(self):
        #从获取的xml构造xml dom树
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        #获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
                
        fromuser = fromUser.encode('utf-8')  # Change unicode to string type
        
        #edited by eve
        con = Connect()
        #edited by eve
        
        if msgType == "text":
            content = xml.find("Content").text
            content = content.encode('utf-8') 
            #return self.render.reply_text(fromUser,toUser,int(time.time()), content)
            #edited by eve
            res = ExecV(con,"select MainState from users where openID=%s",fromuser)     #check current state  
            if res:
                text = res[0][0]     
                #人机对话
                if text == 0:   
                    
                   # mtext = u'欢迎来到人机对话界面，您是需要买东西还是卖东西？'  
                    #mtext = content
                    if content == '查看订单':
                        #mtext = u'test'
                        mtext = getordertext(fromuser)
                    elif content == '买':
                        mtext = buyClick(fromuser)
                    elif content == '卖':
                        mtext = buyClick(fromuser)
                    #elif content == '确认订单':
                    #    mtext = orderconfirm(fromuser,'35')
                    elif content == '查看物品':
                        mtext = getgoodtext(fromuser)
                    elif content == '新消息':
                        #mtext = u'test'
                        mtext = hinttext(fromuser)
                    #elif content == '删除':
                    #    mtext = delete('11','39',1)
                    else:
                        mtext = u'不符合条件的输入！\n'
                        mtext = mtext + u'主界面有效的指令输入为：\n买 —— 购买物品\n卖 —— 出售物品\n查看订单 —— 查看现有订单\n查看物品 —— 查看自己的在售物品\n新消息 —— 查看新消息\n'
                # changed by Xiang
                # 身份绑定
                elif text == 1:
                    mtext = updateBindingInfo(content,fromuser)
                # 卖东西
                elif text == 2:
                    mtext = updatesell(content,fromuser)
                    
                # 买东西
                elif text == 3:
                    mtext = updatebuy(content,fromuser)
                    
            else:
                mtext = u'请先前往个人空间，进行身份绑定！'
          
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)                         
            
            #edited by eve
            
        elif msgType == "event":
            event = xml.find("Event").text
            if event == "subscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()), u"欢迎关注 二货 ！")
            elif event == "unsubscribe":
                return self.render.reply_text(fromUser,toUser,int(time.time()), u"已解除关注，谢谢使用！")
            elif event == "CLICK":
                eventKey = xml.find("EventKey").text
                if eventKey == "rselfmenu_0_0":
                    mtext = u"二货团队：\n 我们是五个人 \n 我们的邮箱: \n snail_walkers@163.com \n 欢迎提出宝贵意见～～\n\n"
                    mtext = mtext + u'主界面有效的指令输入为：\n买 —— 购买物品\n卖 —— 出售物品\n查看订单 —— 查看现有订单\n查看物品 —— 查看自己的在售物品\n新消息 —— 查看新消息\n'
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
                #身份绑定
                elif eventKey == "rselfmenu_0_1":
                    mtext = bindingIdentity(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
                #解除绑定
                elif eventKey == "rselfmenu_0_3":
                    mtext = unbindingIdentity(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
                #买买买
                elif eventKey == "rselfmenu_1_0":  
                    mtext = buyClick(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()),mtext )  
                # 卖卖卖
                elif eventKey == "rselfmenu_2_0":
                    mtext = sellClick(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
                # query orders
                elif eventKey == "queryorders":
                    mtext = getorder(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
                # query goods
                elif eventKey == "querygoods":
                    mtext = getgood(fromuser)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        #登录信息处理
        #返回信息:
        #--Y: 密码正确
        #--N：用户名或密码错误
       
        elif msgType == "login":
            phone = xml.find("Phone").text
            code = xml.find("Code").text
            phone = phone.encode('utf-8') 
            code = code.encode('utf-8')
            test = phone+'\n'+code
            res = ExecV(con,"select openID, password from users where phone=%s",phone)
            if res:
                openID = res[0][0]
                text_code = res[0][1]
                if text_code == code:
                    mtext = u""+openID              
                else:
                    mtext = u"N"
            else:
                mtext = u"N"
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        	
        #注册信息处理
        #--N:注册的手机号已被注册
		#--Y:注册成功
        elif msgType == "register":
            test = u'test'
            name = xml.find("Name").text
            code = xml.find("Code").text
            sid  = xml.find("Sid").text
            phone = xml.find("Phone").text
            nickname = xml.find("Nickname").text
            college = xml.find("College").text
            sex = xml.find("Sex").text
            
            name = name.encode('utf-8')
            code = code.encode('utf-8')
            sid = sid.encode('utf-8')
            phone = phone.encode('utf-8')
            nickname = nickname.encode('utf-8')
            college = college.encode('utf-8')
            sex = sex.encode('utf-8')
            res = ExecV(con,"select * from users where phone=%s",phone)
            if res:
                mtext = u"N"
            else:
                res = ExecV(con,"insert into users (openID,sID,t_name,nickname,sex,college,password,phone) values(%s,%s,%s,%s,%s,%s,%s,%s)",[fromuser,sid,name,nickname,sex,college,code,phone])
                res = ExecV(con,"select * from users where phone=%s",phone)
                if res:
                    mtext = u"Y"
                else:
                    mtext = u"N"
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        # confirm orders
        elif msgType == "confirm":
            #mtext = 1
            #return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
            goodID = xml.find("Content").text
            goodID = goodID.encode('utf-8')
            #return goodID
            mtext = orderconfirm(fromuser,goodID)
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        # automatically check whether the fromuser's orders have changed
        elif msgType == "hint":
            mtext = hint(fromuser)
            #mtext = u'test'
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        # cancle orders or goods
        elif msgType == "delete":
            goodID = xml.find("Content").text
            opt = xml.find("Event").text
            goodID = goodID.encode('utf-8')
            opt = opt.encode('utf-8')
            mtext = delete(fromuser,goodID,opt)
            return self.render.reply_text(fromUser,toUser,int(time.time()), mtext)
        elif msgType == "image":
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"发了一个image")
        else:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"null")
        


            
            
            
            
            
            
            
            
        