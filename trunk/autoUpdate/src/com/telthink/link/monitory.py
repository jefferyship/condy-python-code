#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2011-1-3

@author: 林桦

'''
import ConfigParser
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import logging
import logging.handlers
import SystemInfo

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
    config=ConfigParser.ConfigParser()
    config_dir=''
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log.info(config_dir+'ivrtrack.ini')
    ivrtrackFileObject=open(config_dir+'monitor.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
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
				表2   rows=1 cols=4 
				1 cpu_idle_limit cpu_idle_limit CPU告警阀值 
				2 memory_avi_limit memory_avi_limit 可用内存告警阀值(KB) 
				3 hardspace_name hardspace_name 硬盘名称(例如/dev/sda3) 
				4 hardspace_limit hardspace_limit 硬盘告警阀值 
				表3   rows=1 cols=2 
				1 proc_name proc_name 线程名称 
				2 proc_cpu_limit proc_cpu_limit 线程CPU告警阀值 

    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    monitorFileList=[]
    paramUtil=ParamUtil()
    monitorSystemObject={}
    monitorProcObjectList=[]
    outputParam=paramUtil.invoke("Monitor_Pt_Config", MONITOR_NAME, URL)
    if outputParam.is_success() :
        table1=outputParam.get_tables().get_first_table()
        for row in table1.get_row_list():
            monitorObject={};
            monitorObject['monitorFile']=row.get_one_column(0).get_value()
            monitorObject['keys']=row.get_one_column(1).get_value()
            monitorObject['countMonitor']=row.get_one_column(2).get_value()
            monitorObject['tailRowNum']=row.get_one_column(3).get_value()
            convertUnicodeToStr(monitorObject)
            monitorFileList.append(monitorObject)
        systemRow=outputParam.get_tables().get_row(1,0)
        if systemRow <> None:
            monitorSystemObject['cpu_idle_limit']=systemRow.get_one_column(0).get_value()
            monitorSystemObject['memory_avi_limit']=systemRow.get_one_column(1).get_value()
            monitorSystemObject['hardspace_name']=systemRow.get_one_column(2).get_value()
            monitorSystemObject['hardspace_limit']=systemRow.get_one_column(3).get_value()
            convertUnicodeToStr(monitorSystemObject)
        table3=outputParam.get_tables().get_one_table(2)
        for row in table3.get_row_list():
            monitorProcObject={}
            monitorProcObject['proc_name']=row.get_one_column(0).get_value()
            monitorProcObject['proc_cpu_limit']=row.get_one_column(1).get_value()
            convertUnicodeToStr(monitorProcObject)
            monitorProcObjectList.append(monitorProcObject)
    return (monitorFileList,monitorSystemObject,monitorProcObjectList)

def monitorFile(monitorList):
    """
     监控日志文件.返回需要告警的日志表。
    """
    warnToPersonList=[]
    for monitorObject in monitorList:
        commondStr='tail -'
        commondStr=commondStr+monitorObject['tailRowNum']+' '+monitorObject['monitorFile']
        log.info(commondStr)
        searchLogStd=os.popen(commondStr)
        keyList=[]
        if isinstance(monitorObject['keys'],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
            keyList=monitorObject['keys'].encode('GBK').split('||')
        else:
            keyList=monitorObject['keys'].split('||')
        appearCountOfKeyMap={}
        for key in keyList:
            appearCountOfKeyMap[key]=0
            log.info('search key:'+key)
            for lineLog in searchLogStd.readlines():#是否有关键字内容
                if re.search(key,lineLog):
                    appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
            log.info( 'realLimit:%d,warnLimit:%s'%(appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#到达告警条件，写告警内容
                warnStr=MONITOR_NAME+' Warnning:log file:'+monitorObject['monitorFile']+' key:'+key+' occur times:'+str(appearCountOfKeyMap[key])
                print warnStr
                warnToPersonList.append(warnStr)
    return warnToPersonList

def sendToWarn(warnToPersonList):
    """
    发送告警信息跟相应的联系人员
    """
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    inputStr=inputStr+'\r\n'.join(warnToPersonList)
    outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    flag=''
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    return flag=='0'

def monitorProcCpu(monitorObjectList,saveDbMsgDict):
    """
    1.根据线程名称获取相应线程的告警信息.
    @monitorObjectList: [{'proc_name':procName,'proc_cpu_limit':procCpuLimit}]
    """
    warnToPersonList=[]
    procNameMap={}
    for monitorProcObject in monitorObjectList:
        if procNameMap.has_key(monitorProcObject['proc_name'])==False and monitorProcObject['proc_cpu_limit'].isdigit():
            procNameMap[monitorProcObject['proc_name']]=monitorProcObject['proc_cpu_limit']
    pidObjectList=SystemInfo.getCPUUsedByPidName(procNameMap.keys())
    saveDBMsgDict['procCpu']=pidObjectList
    for pidObject in pidObjectList:
        if pidObject[2]>=float(procNameMap[pidObject[0]]):
            log.info('线程CPU告警: pid:%s,pid_name:%s,cpu_limit:%s,real_cpu:%s',pidObject[0],pidObject[1],procNameMap[pidObject[0]],str(pidObject[2]))
            warnStr=MONITOR_NAME+' proc Warning:pid_name:'+pidObject[0]+' pid_id:'+pidObject[1]+' cpu_limit:'+procNameMap[pidObject[0]]++' real_cpu:'+str(pidObject[2])
            warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorCpu(cpuIdleLimit,saveDbMsgDict):
    """
     1.根据CPU Idle的告警阀值，发送告警信息
    """
    warnToPersonList=[]
    cpuIdle=SystemInfo.getCpuIdle()
    saveDbMsgDict['cpuIdle']=cpuIdle
    if cpuIdleLimit.isdigit() and cpuIdle<float(cpuIdleLimit):
        log.info("CPU Idle告警: cpuIdle_limit:%s,real_cpuIdle:%s",cpuIdleLimit,str(cpuIdle))
        warnStr=MONITOR_NAME+' cpu Idle Warning:cpuIdle_limit:'+cpuIdleLimit+' real_cpuIdle:'+str(cpuIdle)
        warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorMemory(aviPhymenLimit,saveDbMsgDict):
    """
     1.根据内存的告警阀值，发送告警信息
     2.将内存信息保存到数据库中.
    """
    warnToPersonList=[]
    memoryObject=SystemInfo.getMemoryInfo()
    saveDbMsgDict['memory']=memoryObject
    if aviPhymenLimit.isdigit() and memoryObject[1]<float(aviPhymenLimit):
        log.info("内存告警: aviPhymenLimit:%sKB,real_aviPhymen:%sKB",aviPhymenLimit,str(memoryObject[1]))
        warnStr=MONITOR_NAME+' Memory Warning:aviPhymenLimit:'+aviPhymenLimit+'KB real_aviPhymen:'+str(memoryObject[1])+'KB'
        warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorHardSpace(monitorSystemObject,saveDbMsgDict):
    """
     1.根据硬盘配置的告警阀值，发送报警信息
     @monitorSystemObject {'cpu_idle_limit':cpu_idle_limit,'memory_avi_limit':memory_avi_limit,'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}
    """
    hardSpaceList=SystemInfo.getHardSpace()#[(文件系统,总计大小,已用空间,可用空间,已用%,挂载点)]
    saveDbMsgDict['hardSpace']=hardSpaceList
    warnToPersonList=[]
    if monitorSystemObject['hardspace_name']<>None and monitorSystemObject['hardspace_limit'].isdigit():
        for hardSpace in hardSpaceList:#(文件系统,已用空间,可用空间,已用%,挂载点)
            if monitorSystemObject['hardspace_name']==hardSpace[0] and float(hardSpace[4])<=float(monitorSystemObject['hardspace_limit']):
                log.info("磁盘空间告警: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorSystemObject['hardspace_name'],monitorSystemObject['hardspace_limit'],hardSpace[4])
                warnStr=MONITOR_NAME+' hardspace Warning:hardspace_name:'+monitorSystemObject['hardspace_name']+' limit_used_percent:'+monitorSystemObject['hardspace_limit']+' real_used_percent:'+hardSpace[4]
                warnToPersonList.append(warnStr)
    return warnToPersonList
         
def saveSystemInfo(saveDbMsgDict):
    """
     将收集到的系统信息保存大数据库中.
    """
    procCpuList=saveDbMsgDict['procCpu']#[(name,pid,usedCpu,usedMemory)]
    cpuIdle=saveDbMsgDict['cpuIdle']
    memoryObject=saveDbMsgDict['memory']#(total_phymen,avi_phymen.used_phymen) KB 
    hardSpaceList=saveDbMsgDict['hardSpace']#[(文件系统,总计大小,已用空间,可用空间,已用%,挂载点)]
    table_1List=[str(cpuIdle)]
    for object in memoryObject:
        table_1List.append(str(object))
    #table1:host_name
    #table2:cpu_idle,total_phy_men,avi_phymen,used_phymen
    #table3:proc_name,pid,used_cpu,used_memory.有可能是多行.
    #table4:hardspace_name,used_hardspace,avi_hardspace,used_hard_space_percent,file_hand_up
    table_2=str(LinkConst.SPLIT_COLUMN).join(table_1List)
    procInputList=[]
    for procIdObject in procCpuList:
        tempList=[]
        for temp in procIdObject:
            tempList.append(str(temp))
        tempStr=str(LinkConst.SPLIT_COLUMN).join(tempList)
        procInputList.append(tempStr)
    table_3=str(LinkConst.SPLIT_ROW).join(procInputList)
    hardSpaceInputList=[]
    for hardSpaceObject in hardSpaceList:
        hardSpaceInputList.append(str(LinkConst.SPLIT_COLUMN).join(hardSpaceObject))
    table_4=str(LinkConst.SPLIT_ROW).join(hardSpaceInputList)
    inputStr=MONITOR_NAME+LinkConst.SPLIT_TABLE+table_2+LinkConst.SPLIT_TABLE+table_3+LinkConst.SPLIT_TABLE+table_4
    #savePtResourceInfo
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("savePtResourceInfo", inputStr, URL)
    if outputParam.is_success():
        flag=outputParam.get_first_column_value()
        flagMsg=outputParam.get_column_value(0,0,1)
        if isinstance(flagMsg,unicode):
            flagMsg=flagMsg.encode('GBK')
        log.info('调用savePtResourceInfo服务成功.输入参数:%s,输出结果:%s',inputStr,flagMsg)
    else:
        log.info('调用savePtResourceInfo服务失败.输入参数:%s',inputStr)
    
        
def get_version():
    version ='1.1.0.0'
    
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  pt_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.01.17')
    log.info(' 功能点1.监控平台日志')
    log.info('      2.监控CPU，内存、线程、硬盘告警信息')
    log.info('      3.收集CPU，内存、线程、硬盘资源信息')
    log.info( '=========================================================================')
    return version
        
if __name__ == '__main__':
    # set Logger Config
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(os.getcwd()+os.sep+'monitor.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    
    
    
    get_version()
    getCommonConfig()
    log.info('URL:%s,MONITOR_NAME:%s'%(URL,MONITOR_NAME))
    monitorFileList,monitorSystemInfo,monitorProcList=getMonitorService()
    if len(monitorFileList)==0 and len(monitorSystemInfo)==0 and len(monitorProcList)==0:
        log.info( '没有该IVR的监控配置信息，请查看Monitor_Pt_Config服务.')
        sys.exit()
    #文件监控
    warnToPersonList=monitorFile(monitorFileList)
    saveDBMsgDict={}
    #线程监控
    if len(monitorProcList)>0:
        warnToPersonList=warnToPersonList+monitorProcCpu(monitorProcList,saveDBMsgDict)
    #cpu监控
    warnToPersonList=warnToPersonList+monitorCpu(monitorSystemInfo['cpu_idle_limit'],saveDBMsgDict)
    #内存监控
    warnToPersonList=warnToPersonList+monitorMemory(monitorSystemInfo['memory_avi_limit'],saveDBMsgDict)
    #硬盘监控
    warnToPersonList=warnToPersonList+monitorHardSpace(monitorSystemInfo,saveDBMsgDict)
    saveSystemInfo(saveDBMsgDict)
    if len(warnToPersonList)==0:
        log.info( '没有告警信息')
        sys.exit()
    sendToWarn(warnToPersonList)
