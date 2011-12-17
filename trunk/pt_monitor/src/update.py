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
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
from ftplib import FTP
import thread
import win32api
import time

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

def reloadProgram(path):
    """
      �Զ�����������
    """
    try:
        global isAleadyReload
        isAleadyReload=False
        log.info( '>update< �������°汾������ϣ�%s�����Զ�������.........',path)
        #time.sleep(2)#�ȴ�2s��
        win32api.ShellExecute(0,'open',path,'','',1)#��������.
        log.info( '>update< ......................,%s�����Զ��������.......',path)
        isAleadyReload=True
        h1.close()
    except Exception:
        log.exception('ϵͳ����')
        h1.close()

def get_version():
    version ='1.1.0.1'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info(' >update< �Զ����³�������')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'WINPATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('>update< ���ݿ�İ汾����:'+str(versionMsg))
    log.info('>update< ��ʼ����������,������İ汾��:%s',versionMsg['version'])
    ftp=FTP(versionMsg['ip'],versionMsg['user'],versionMsg['password'])
    patchFileList=[]
    patchPwd=''
    if versionMsg['dict'][-1]=='/':patchPwd=versionMsg['dict']+versionMsg['version']
    else:patchPwd=versionMsg['dict']+'/'+versionMsg['version']
    patchFileList=ftp.nlst(patchPwd)
    for fileName in patchFileList:
        log.info('>update< get '+fileName+' save to '+config_dir+os.path.split(fileName)[1])
        ftp.retrbinary('RETR '+fileName,open(config_dir+os.path.split(fileName)[1],'wb').writelines)
    log.info('>update< ��ʼ����������ɹ���׼������������')

if __name__ == '__main__':
    print '>update< �Զ����³���'
    time.sleep(3)
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

    try:
        global isAleadyReload
        isAleadyReload=False
        #log.info('>update< ���³ɹ���������mointorForWindow.exe')
        get_version()
        thread.start_new_thread(reloadProgram,('monitorForWindow.exe',))
        for i in range(4):
            if isAleadyReload:break
            else:time.sleep(3)
        #os.popen('monitorForWindow.exe')
        #os.system('monitorForWindow.py')
        #os.popen('monitorForWindow.py')
        #subprocess.Popen('monitorForWindow.py', shell=True)

    except Exception:
        log.exception('ϵͳ����')
        h1.close()

