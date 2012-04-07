#!/usr/bin/env python
# -*- coding: GBK -*-
import logging
import logging.handlers
import ConfigParser
import ping
import os
import sys
import time
def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global MONITOR_NAME
    global IS_START
    global RECYCLE_TIMES
    global ipAddressList
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'ping.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    config.items
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10
    try:
        ipAddressList=config.items('ip')
    except Exception:
        ipAddressList=[]
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    alarmObjectMap={}
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'ping.log',maxBytes=2097152,backupCount=20)
    #h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    ping.__log__=log
    getCommonConfig()
    try:
        while IS_START=='1':
            getCommonConfig()
            for (ipname,ipvalue) in ipAddressList:
                ping.ping(ipvalue)
            time.sleep(RECYCLE_TIMES)
            if IS_START=='0':
                log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('系统报错')
    h1.close()
