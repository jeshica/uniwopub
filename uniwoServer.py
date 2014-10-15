#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import MySQLdb
import json
import sys
import gzip
import urllib2
import time
import ssl

import sys 
from tornado.options import define, options
import os
#reload(sys) 
#sys.setdefaultencoding('utf-8')

from sdkConfig import *

# from mylog import Log

class NetReceiver(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs);
        self.initAttr();
                
    def initAttr(self):
        self.cmdFormat = []
    
    @tornado.web.asynchronous
    def post(self):    
        data = self.request.body
        print "Client post data received: %s" % repr(data)
        jsondata = self.get_argument('data')
        
        outdata = self.operation(jsondata)
        self.write(outdata)
        self.finish()        
    
    def operation(self):
        pass
        
        
    def Recharge(self, serverurl, sessionid, rechargeid, money,psd):
        URL = serverurl + "/sdkRecharge"
        dict = {"SessionID":sessionid, "RechargeID":rechargeid, "RechargeMoney":money,"PSD":psd}
        
        strData = json.dumps(dict)
        print ("request data str: " + strData)
        
        Paras = gzip.zlib.compress(strData)
        
        ZLKJReq = urllib2.Request(URL, Paras)
    
        RESFile = urllib2.urlopen(ZLKJReq)
    
        RES_Submit = RESFile.read()
    
        decmpressStr = gzip.zlib.decompress(RES_Submit)
        print ("decmpress str: " + decmpressStr)
        
        return json.loads(decmpressStr)['msgFlag']


class NetSender():
    def __init__(self):
        self.desUrl="https://open.wo.com.cn/openapi/getchannelpaymentsms/v1.0"
        self.params={}
        self.request=None
    
    def setHeader(self,token,val):
        self.request.add_header(token, val)
        
    def addParam(self,token,val):
        self.params[token]=val
        
    def addParams(self,params):
        self.params=params  
        
    def getRequest(self):
        self.request=urllib2.Request(self.desUrl,self.decodeJson())         
        
    def send(self):
        self.result=urllib2.urlopen(self.request)   
        return self.result
    
    def decodeJson(self):
        return json.dumps(self.params)
    
    def encodeJson(self):
        pass
    

        
class reloadonline(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('psd') == SYSTEMPSD:
            
            Recharge_G.clear()
                       
            self.write("SdkServer reloaded!")
            self.finish()
        else:
            self.write("Not allowed!")
            self.finish()

application = tornado.web.Application([
    (r'/', reloadonline),
   
#    (r'/testgh', testgh)
    ]
)

paramEx={
        "outTradeNo":"8938057637279851",
         "timeStamp":"20130128023312",
         "subject": "捕鱼达人金币",
         "description": "捕鱼达人金币购买",
         "price": 5,
         "quantity": 1,
         "totalFee": 5,
         "callbackUrl": "http://10.137.99.100/getPaymentResult",
         "callbackData":"QAZWSXEDC",
         "appKey":"000000001",
         "appName":"捕鱼达人",
         "iapId": "",
         "imsi": "460030912121001",
         "imei": "860275020104961",
         "signType":"HMAC-SHA1",
         "signature":"KEISDADADDDDA73NC6HN23D6GJ78K1J3N5N423F5G78"
         }

if __name__ == "__main__": 
    
    #tornado.options.parse_command_line()
    
    mySender=NetSender()
    
    #mySender.addParams(paramEx)
    
    #mySender.encodeJson()
    
    mySender.getRequest()
    
    #mySender.setHeader("Authorization", "platformID=\"88149731e0ed75daa03a6e1e30427cddfa4ch3ci\",password=\"keisda73nc6hn234k5kj6j78k1j34n5n4n6n7l9f\"")
    #mySender.setHeader("Accept", "application/json")    
    #mySender.setHeader("Content-Type", "application/json")
    
    print mySender.request.header_items()
    
    
    print mySender.send()
    #print (sys.argv[0])
    
    #print("sys default encoding: " + sys.getdefaultencoding())
     
    #print('Listening on port: ' + str(options.port))
    #os.system("title SDK Server: Port=" + str(options.port) + " Encoding=" + sys.getdefaultencoding())
    
    #http_server = tornado.httpserver.HTTPServer(application)
    #http_server.listen(options.port)
    #tornado.ioloop.IOLoop.instance().start()
