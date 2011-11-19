# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        update.py
# Purpose:     ����mointorForWindow.exe�ĳ��������꣬�Լ��˳�.
#
# Author:      Condy
#
# Created:     10-08-2011
# Copyright:   (c) Administrator 2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import os
import sys
import logging
import logging.handlers
import ConfigParser
import subprocess


def convertUnicodeToStr(unicodeMap):
    for key in unicodeMap.keys():
        if isinstance(unicodeMap[key],unicode):#�������Ĺؼ��֣�Ҫ��unicode����ת��Ϊstr����.
            unicodeMap[key]=unicodeMap[key].encode('GBK')

def getCommonConfig():
    """
      ��ȡivrtrack.ini�������ļ���Ϣ
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global MONITOR_NAME
    global IS_START
    global RECYCLE_TIMES
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'monitorForWindow.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'monitorForWindow.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    getCommonConfig()

##    monitorDiskObjectList=[]
##    monitorDiskObjectList.append({'hardspace_name':'c:\\','hardspace_limit':'1'})
##    monitorDiskObjectList.append({'hardspace_name':'d:\\','hardspace_limit':'1'})

    try:
        log.info('>update< ���³ɹ���������mointorForWindow.exe')
        #os.popen('monitorForWindow.exe')
        #os.system('monitorForWindow.exe')
        subprocess.Popen('monitorForWindow.exe', shell=True)
        log.info('>update< ���������ɹ����˳���������')
        h1.close()
        sys.exit()
    except Exception:
        log.exception('ϵͳ����')
        h1.close()

