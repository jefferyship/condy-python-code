#!/usr/bin/env python
# -*- coding: GBK -*-
import urllib2
import urllib
import logging
import logging.handlers
import os
import sys

def getXml():
    for i in range(20):
        filename='/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/log/iservucLog_20110712/iserv_fjas2server2.log.'+str(20-i)
        log.info(filename)
        logFileObject=open(filename)
        xmldata=''
        serviceUrl='http://134.128.196.11:9081/iservuc/ServiceGate/SimpleXMLGate'
        for lineStr in logFileObject.readlines():
            if isinstance(lineStr,unicode):#遇到中文关键字，要把unicode类型转换为str类型.
                lineStr=lineStr.encode('GBK')
            if lineStr.find('com.telthink.link.pub.ParamXmlUtil')>-1 and lineStr.find('sendSurvey')>-1:
                inputXML=lineStr[lineStr.find('<'):]
                log.info(inputXML)
                f=urllib2.urlopen(serviceUrl,urllib.urlencode({'xmldata':inputXML}))
                log.info(f.read().lstrip())

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'test.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    getXml()
