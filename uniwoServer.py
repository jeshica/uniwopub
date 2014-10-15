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
import base64,hashlib

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
        "outTradeNo":"004",
         "timeStamp":"20140128023312",
         "subject": "itemid",
         "description": 0.01,
         "callbackUrl": "http://10.137.99.100/getPaymentResult",
         "appKey":"000000001",
         "appName":"appname",         
         
         "signature":"KEISDADADDDDA73NC6HN23D6GJ78K1J3N5N423F5G78"
         }

if __name__ == "__main__": 
    url= "https://open.wo.com.cn/openapi/getchannelpaymentsms/v1.0"
    send_headers = {
     'Authorization':'platformID=\"b692bc21-5bb0-4904-a95e-2ab44828b03e\",password=\"yllk2014\"',
     'Accept':'application/json;charset=UTF-8',
     'Content-Type':'application/json'
    }
    a={"signType":"HMAC-SHA1"}
    parastr=paramEx['outTradeNo']
    parastr+=paramEx["timeStamp"]
    parastr+=paramEx["subject"]
    parastr+=str(paramEx["description"])
    parastr+=paramEx["callbackUrl"]
    parastr+=paramEx["appKey"]
    parastr+=paramEx["appName"]
    
    
    parastr+="b692bc21-5bb0-4904-a95e-2ab44828b03e&"
    parastr+="yllk2014"
    
    sha1obj = hashlib.sha1()
    sha1obj.update(parastr)
    hash = sha1obj.hexdigest()
    signature=base64.encodestring(hash)
    print signature
    paramEx["signature"]=signature
    print json.dumps(paramEx)
    req = urllib2.Request(url,data=json.dumps(paramEx),headers=send_headers)
    print req.header_items()
    r = urllib2.urlopen(req)
    #tornado.options.parse_command_line()
    
    #mySender=NetSender()
    
    #mySender.addParams(paramEx)
    
    #mySender.encodeJson()
    
    #mySender.getRequest()
    
    #mySender.setHeader("Authorization", "platformID=\"b692bc21-5bb0-4904-a95e-2ab44828b03e\",password=\"yllk2014\"")
    #mySender.setHeader("Accept", "application/json;charset=UTF-8")    
    #mySender.setHeader("Content-Type", "application/json")
    
    #print mySender.request.header_items()
    
    
    #print mySender.send()
    print r.read()
    #print (sys.argv[0])
    
    #print("sys default encoding: " + sys.getdefaultencoding())
     
    #print('Listening on port: ' + str(options.port))
    #os.system("title SDK Server: Port=" + str(options.port) + " Encoding=" + sys.getdefaultencoding())
    
    #http_server = tornado.httpserver.HTTPServer(application)
    #http_server.listen(options.port)
    #tornado.ioloop.IOLoop.instance().start()
