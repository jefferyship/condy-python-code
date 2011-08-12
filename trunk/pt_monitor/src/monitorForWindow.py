# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        monitorForWindow.py
# Purpose:     window版本的磁盘监控，线程监控。CPU，内存监控.
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
from ftplib import FTP
import time
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import SystemInfo

def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global MONITOR_NAME
    global IS_START
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'monitorForWindow.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def sendToWarn(warnToPersonList):
    """
    发送告警信息跟相应的联系人员
    """
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    inputStr=inputStr+'\r\n'.join(warnToPersonList)
    log.info('告警发送短信:%s',inputStr)
    outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    flag=''
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    return flag=='0'

def getMonitorService():
    """
       调用服务获取监控的文件
       返回一个列表，数据结构如下:
       多个关键字之间以逗号做分隔.
       [{'monitorFile':监控文件,'keys':关键字，'countMonitor':次数告警,'tailRowNum':tail的行数,'procName':CPU线程名,'procCpuLimit'：CPU告警阀值},('monitorFile':监控文件,'keys':关键字，'countMonitor':次数告警)]
       	        1 monitorFile monitorFile 监控文件名路径
				2 keys keys 监控关键字，多个关键字之间按有逗号分隔
				3 countMonitor countMonitor 告警阀值
				4 tailRowNum tailRowNum 监控文件的行数
                5 log_type   log_type   日志类型:websphere,svcsmgr,ctserver等
				表2   rows=1 cols=4
				1 cpu_idle_limit cpu_idle_limit CPU告警阀值
				2 memory_avi_limit memory_avi_limit 可用内存告警阀值(KB)
				3 hardspace_name hardspace_name 硬盘名称(例如/dev/sda3)
				4 hardspace_limit hardspace_limit 硬盘告警阀值
				表3   rows=1 cols=2
				1 proc_name proc_name 线程名称
				2 proc_cpu_limit proc_cpu_limit 线程CPU告警阀值
                表4   rows=1 cols=2   多行输出
                  1 command  command  执行命令的名称 用于执行netstat -nat|grep -i '关键字'|wc -l
                  2 netstat_limit netstat_limit 执行命令返回数字的阀值

    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    monitorFileList=[]
    paramUtil=ParamUtil()
    monitorSystemObject={}
    monitorProcObjectList=[]
    monitorNetstatObjectList=[]
    outputParam=paramUtil.invoke("Monitor_Pt_Config", MONITOR_NAME, URL)
    if outputParam.is_success() :
        table1=outputParam.get_tables().get_first_table()
        for row in table1.get_row_list():
            monitorObject={};
            monitorObject['monitorFile']=row.get_one_column(0).get_value()
            monitorObject['keys']=row.get_one_column(1).get_value()
            monitorObject['countMonitor']=row.get_one_column(2).get_value()
            monitorObject['tailRowNum']=row.get_one_column(3).get_value()
            monitorObject['log_type']=row.get_one_column(4).get_value()
            convertUnicodeToStr(monitorObject)
            if monitorObject['monitorFile']=='':#如果是空，表示没有配置日志监控
                continue
            else:
                monitorFileList.append(monitorObject)
        systemRow=outputParam.get_tables().get_row(1,0)
        if systemRow <> None:
            monitorSystemObject['cpu_idle_limit']=systemRow.get_one_column(0).get_value()
            monitorSystemObject['memory_avi_limit']=systemRow.get_one_column(1).get_value()
            monitorSystemObject['hardspace_name']=systemRow.get_one_column(2).get_value()
            monitorSystemObject['hardspace_limit']=systemRow.get_one_column(3).get_value()
            convertUnicodeToStr(monitorSystemObject)
            if monitorSystemObject['cpu_idle_limit']=='' and monitorSystemObject['memory_avi_limit']=='' and monitorSystemObject['hardspace_name']=='' and monitorSystemObject['hardspace_limit']=='':
                monitorSystemObject={}
        table3=outputParam.get_tables().get_one_table(2)
        for row in table3.get_row_list():
            monitorProcObject={}
            monitorProcObject['proc_name']=row.get_one_column(0).get_value()
            monitorProcObject['proc_cpu_limit']=row.get_one_column(1).get_value()
            convertUnicodeToStr(monitorProcObject)
            if monitorProcObject['proc_name']=='':#如果是空，表示没有配置线程监控
                continue
            else:
                monitorProcObjectList.append(monitorProcObject)
        table4=outputParam.get_tables().get_one_table(3)
        if table4<>None:
            for row in table4.get_row_list():
                monitorNetstatObject={}
                monitorNetstatObject['command']=row.get_one_column(0).get_value()
                monitorNetstatObject['netstat_limit']=row.get_one_column(1).get_value()
                convertUnicodeToStr(monitorProcObject)
                if monitorNetstatObject['command']=='':#如果是空，表示没有配置netstat命令的监控
                    continue
                else:
                    monitorNetstatObjectList.append(monitorNetstatObject)
    return (monitorFileList,monitorSystemObject,monitorProcObjectList,monitorNetstatObjectList)


def get_version():
    version ='1.1.0.0'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  monitorForWindow.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.08.12 modify time:2011.08.05')
    log.info(' 功能点1.监控windows的磁盘空间')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'monitorForWindow'+LinkConst.SPLIT_COLUMN+'PATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('数据库的版本配置:'+str(versionMsg))
    if versionMsg.has_key('version') and version<>versionMsg['version']:
        log.info(' 发现程序版本有最新的，版本号为%s,开始更新程序',versionMsg['version'])
        ftp=FTP(versionMsg['ip'],versionMsg['user'],versionMsg['password'])
        patchFileList=[]
        patchPwd=''
        if versionMsg['dict'][-1]==os.sep:patchPwd=versionMsg['dict']+versionMsg['version']
        else:patchPwd=versionMsg['dict']+os.sep+versionMsg['version']
        patchFileList=ftp.nlst(patchPwd)
        for fileName in patchFileList:
                log.info('get '+fileName+' save to '+config_dir+os.path.split(fileName)[1])
                ftp.retrbinary('RETR '+fileName,open(config_dir+os.path.split(fileName)[1],'wb').writelines)
    log.info( '=========================================================================')

    return version
def monitorDisk(monitorDiskObjectList,saveDbMsgDict):
    """
    windows 版本的磁盘空间检查,monitorDiskOjectList [{'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}]
    """
    warnToPersonList=[]
    saveToDBList=[]#[(文件系统,总计大小,已用空间,可用空间,已用%,挂载点)]
    saveDbMsgDict['hardSpace']=saveToDBList
    for monitorDiskObject in monitorDiskObjectList:
        try:
            total,used,free,usedPecent=SystemInfo.getdiskByPath(monitorDiskObject['hardspace_name'])
            saveToDBList.append((monitorDiskObject['hardspace_name'],total/1024,used/1024,free/1024,usedPecent,''))
            limitPercent=float(monitorDiskObject['hardspace_limit'])
            if usedPecent>=limitPercent:
                log.info("磁盘空间告警: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],str(round(usedPecent,2)))
                warnStr=MONITOR_NAME+' 磁盘空间告警:hardspace_name:'+monitorDiskObject['hardspace_name']+' limit_used_percent:'+monitorDiskObject['hardspace_limit']+' real_used_percent:'+str(round(usedPecent,2))
                warnToPersonList.append(warnStr)
        except Exception:
            log.exception('获取磁盘空间报错。磁盘为:'+monitorDiskObject['hardspace_name'])

    return warnToPersonList




if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'monitor.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    getCommonConfig()

    monitorDiskObjectList=[]
    monitorDiskObjectList.append({'hardspace_name':'c:\\','hardspace_limit':'1'})
    monitorDiskObjectList.append({'hardspace_name':'d:\\','hardspace_limit':'1'})

    try:
        while IS_START=='1':
            #get_version()
            getCommonConfig()
            monitorDisk(monitorDiskObjectList,{})

            time.sleep(10)


        log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('系统报错')

