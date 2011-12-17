# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        update.py
# Purpose:     重新mointorForWindow.exe的程序，重启完，自己退出.
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
        if isinstance(unicodeMap[key],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
            unicodeMap[key]=unicodeMap[key].encode('GBK')

def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
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
      自动重启本程序
    """
    try:
        global isAleadyReload
        isAleadyReload=False
        log.info( '>update< 程序最新版本更新完毕，%s程序自动重启中.........',path)
        #time.sleep(2)#等待2s中
        win32api.ShellExecute(0,'open',path,'','',1)#重启程序.
        log.info( '>update< ......................,%s程序自动重启完成.......',path)
        isAleadyReload=True
        h1.close()
    except Exception:
        log.exception('系统报错')
        h1.close()

def get_version():
    version ='1.1.0.1'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info(' >update< 自动更新程序启动')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'WINPATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('>update< 数据库的版本配置:'+str(versionMsg))
    log.info('>update< 开始更新主程序,主程序的版本号:%s',versionMsg['version'])
    ftp=FTP(versionMsg['ip'],versionMsg['user'],versionMsg['password'])
    patchFileList=[]
    patchPwd=''
    if versionMsg['dict'][-1]=='/':patchPwd=versionMsg['dict']+versionMsg['version']
    else:patchPwd=versionMsg['dict']+'/'+versionMsg['version']
    patchFileList=ftp.nlst(patchPwd)
    for fileName in patchFileList:
        log.info('>update< get '+fileName+' save to '+config_dir+os.path.split(fileName)[1])
        ftp.retrbinary('RETR '+fileName,open(config_dir+os.path.split(fileName)[1],'wb').writelines)
    log.info('>update< 开始更新主程序成功，准备启动主程序')

if __name__ == '__main__':
    print '>update< 自动更新程序'
    time.sleep(3)
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
        #log.info('>update< 更新成功重新启动mointorForWindow.exe')
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
        log.exception('系统报错')
        h1.close()

