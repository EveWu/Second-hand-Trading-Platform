# -*- coding: utf-8 -*-
#encoding=utf-8
import hashlib
import json
import web
import lxml
import time
import os
import urllib2,json
import sae.const  
from lxml import etree

#sql control
from sqlInterface import *


class UpdateDb:
    def GET(self):
        con = Connect()
        res = Exec(con,"delete from goods where (TO_DAYS(now())-TO_DAYS(startDate))>100")
        return res