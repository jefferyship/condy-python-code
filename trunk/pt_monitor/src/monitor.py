#!/usr/bin/env python
# -*- coding:GBK -*-
'''
Created on 2011-1-3

@author: 林桦

'''
import ConfigParser
import os
import os.path
import re
import sys
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import logging
import logging.handlers
import SystemInfo
import glob
import datetime
import time
from ftplib import FTP
import tarfile

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
    config=ConfigParser.SafeConfigParser()
    ivrtrackFileObject=open(config_dir+'monitor.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    ivrtrackFileObject.close()
def writeCommonConfig(option,value):
    """
     设置值到monitor.ini的common，section中.
    """
    config=ConfigParser.SafeConfigParser()
    config.read(config_dir+'monitor.ini')
    config.set('common',option,value)
    ivrtrackFileObject=open(config_dir+'monitor.ini',"rb+")
    config.write(ivrtrackFileObject)
    ivrtrackFileObject.close()
def readLastmonitorFileSmContent():
    global lastmonitorFileSmContent
    try:
        lastmonitorFileSmContentFileObject=open(config_dir+'lastmonitorFileSmContent.log','rb+')
        lastmonitorFileSmContent=lastmonitorFileSmContentFileObject.read(2048)
        lastmonitorFileSmContentFileObject.close()
    except:
        lastmonitorFileSmContent=''

def writeLastmonitorFileSmContent(value):
    """
      写上次短信的记录到文件中.
    """
    try:
        lastmonitorFileSmContentFileObject=open(config_dir+'lastmonitorFileSmContent.log','wb+')
        lastmonitorFileSmContentFileObject.write(value)
        lastmonitorFileSmContentFileObject.close()
    except:
        log.exception('写短信发送内容到,%s文件中失败',config_dir+'lastmonitorFileSmContent.log')

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

def monitorFile(monitorList):
    """
     监控日志文件.返回需要告警的日志表。
    """

    CTI_ERR_KEY='"ConsultationCall\[7\]",OperResult=\[1\]'
    warnToPersonList=[]
    for monitorObject in monitorList:
        #相关参数初始化
        appearCountOfKeyMap={}
        keyList=[]
        if isinstance(monitorObject['keys'],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
            keyList=monitorObject['keys'].encode('GBK').split('||')
        else:
            keyList=monitorObject['keys'].split('||')
        for key in keyList:
            appearCountOfKeyMap[key]=0
            log.info('search key:'+key)

        bIsGrepInCtServer=False #判断是否有包含CTI的关键字.
        try:
            if monitorObject['log_type']=='ctserver' and keyList.index(CTI_ERR_KEY)>-1:
                commondStr='grep \''+CTI_ERR_KEY+'\' '+monitorObject['monitorFile']+' |wc -l'
                bIsGrepInCtServer=True
                keyList.remove(CTI_ERR_KEY)#后面的日志可以不需要搜索CTI的关键字..
                log.info(commondStr)
                searchLogStd=os.popen(commondStr)
                for lineLog in  searchLogStd.readlines():
                    appearCountOfKeyMap[CTI_ERR_KEY]=int(lineLog)
        except ValueError:
            pass

        commondStr='tail -'
        commondStr=commondStr+monitorObject['tailRowNum']+' '+monitorObject['monitorFile']
        if len(keyList)>0:
            log.info(commondStr)
            searchLogStd=os.popen(commondStr)
            for lineLog in searchLogStd.readlines():#是否有关键字内容
                for key in keyList:
                    if re.search(key,lineLog):appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
        if bIsGrepInCtServer:keyList.append(CTI_ERR_KEY)#CTI的关键字加入运算.
        for key in keyList:
            log.info( 'key:%s,realLimit:%d,warnLimit:%s'%(key,appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if  appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#到达告警条件，写告警内容
                warnStr=MONITOR_NAME+' 告警,日志文件:'+monitorObject['monitorFile']+' 关键字:'+key+' 出现次数:'+str(appearCountOfKeyMap[key])
                lastmonitorFileSmContent=warnStr
                log.info(warnStr)
                warnToPersonList.append(warnStr)
    return warnToPersonList

def sendToWarn(warnToPersonList):
    """
    发送告警信息跟相应的联系人员
    """
    global lastmonitorFileSmContent
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    currmonitorFileSmContent='.'.join(warnToPersonList)
    if lastmonitorFileSmContent==currmonitorFileSmContent:
        log.info('重复告警短信不发送:%s',currmonitorFileSmContent)
        return True;

    outputParam=paramUtil.invoke("Monitor_machine_info", MONITOR_NAME, URL)
    planId=''
    if outputParam.is_success() and outputParam.get_tables().get_first_table().has_row():
       planId=outputParam.get_column_value(0,0,4)
    else:
        log.error('调用Monitor_machine_info失败，或者是%s机器名没有在monitor_pt_machine_name表中配置',MONITOR_NAME)
        return False
    flag=''
    if planId!='':#调用10000号和外包都通用的服务，外包可以发送邮件。
        inputStr=planId.encode('GBK')+LinkConst.SPLIT_COLUMN+'A'+LinkConst.SPLIT_COLUMN+'\r\n'.join(warnToPersonList)
        log.info('发送短信:调用服务WarnToPerson,输入参数:%s',inputStr)
        outputParam=paramUtil.invoke("WarnToPerson", inputStr, URL)
    else:
        inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
        inputStr=inputStr+'\r\n'.join(warnToPersonList)
        log.info('发送短信:调用服务Monitor_Warn_To_Person,输入参数:%s',inputStr)
        outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    writeLastmonitorFileSmContent(currmonitorFileSmContent)
    return flag=='0'
def monitorCoreFile(monitorList):
    """
      监控日志目录下，是否有存在core文件.
    """
    warnToPersonList=[]
    fiveMiniuteBefore=datetime.datetime.now()+datetime.timedelta(minutes=-5)#检查5分钟之前是否有core日志.
    currTime=datetime.datetime.now()
    for monitorObject in monitorList:
        fileTime=datetime.datetime.now()
        corePathFile=os.path.split(monitorObject['monitorFile'])[0]
        if  monitorObject['log_type']=='ctserver' or monitorObject['log_type']=='svcsmgr':
            #推到上级，上级目录。相当于/home/tnsmcc/LOG/svcsmgr ->变更成/home/tnsmcc/bin
            corePathFile=corePathFile+'/../../bin'+os.sep+'core.*'
             #推到上级，上级目录。相当于/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/test_server2 ->变更成/opt/IBM/WebSphere/AppServer/profiles/AppSrv01
        elif monitorObject['log_type']=='websphere':
            corePathFile=corePathFile+'/../..'+os.sep+'javacore.*'
        else:#其他类型的core暂时不做监控.
            log.info('日志类型：%s,不做core文件监控.',monitorObject['log_type'])
            continue
        log.info('查询core文件.'+corePathFile)
        fileList=glob.glob(corePathFile)
        for filename in fileList:
            log.info('filename:%s',filename)
            fileTimeTuple=time.localtime(os.path.getctime(filename))
            #生成日期对象
            fileTime=datetime.datetime(fileTimeTuple.tm_year,fileTimeTuple.tm_mon,fileTimeTuple.tm_mday,fileTimeTuple.tm_hour,fileTimeTuple.tm_min,fileTimeTuple.tm_sec)
            #log.info('fileTime:%s,fiveMiniuteBefore:%s,currTime:%s',str(fileTime),str(fiveMiniuteBefore),str(currTime))
            if fiveMiniuteBefore<fileTime<currTime:#文件生成时间在5分钟内.
                warnStr=MONITOR_NAME+' 告警,产生core文件。文件名:'+filename
                log.info(warnStr)
                warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorProcExist(monitorObjectList):
    """
     判断指定的线程是否有存在。
     @monitorObjectList: [{'proc_name':procName,'proc_cpu_limit':procCpuLimit}]
    """
    warnToPersonList=[]
    procNameMap={}
    for monitorProcObject in monitorObjectList:
        if procNameMap.has_key(monitorProcObject['proc_name'])==False:
            procNameMap[monitorProcObject['proc_name']]=False
    pidObjectList=SystemInfo.getCPUUsedByPidName(procNameMap.keys())
    if pidObjectList==None:
        log.info('psutil的插件没有安装，或者不支持psutil的低版本的linux。')
        return warnToPersonList
    for pidObject in pidObjectList:#如果线程已经存在，将状态设置成True
        procNameMap[pidObject[0]]=True
    warnStr=''
    for procName,isExist in procNameMap.iteritems():
        if isExist==False and len(warnStr)==0:
            warnStr=MONITOR_NAME+' 线程告警:线程名称:'+procName+'不存在.'
        elif isExist==False:
            warnStr+=',线程名称:'++procName+'不存在.'
    if len(warnStr)>0:
        log.info('线程告警: %s',warnStr)
        warnToPersonList.append(warnStr)
    return warnToPersonList


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
    if pidObjectList==None:
        log.info('psutil的插件没有安装，或者不支持psutil的低版本的linux。')
        return warnToPersonList
    saveDBMsgDict['procCpu']=pidObjectList
    for pidObject in pidObjectList:
        if pidObject[2]>=float(procNameMap[pidObject[0]]):
            log.info('线程CPU告警: pid:%s,pid_name:%s,cpu_limit:%s,real_cpu:%s',pidObject[0],pidObject[1],procNameMap[pidObject[0]],str(pidObject[2]))
            warnStr=MONITOR_NAME+' 线程CPU告警:线程名称:'+pidObject[0]+' 线程ID:'+pidObject[1]+' 阀值:'+procNameMap[pidObject[0]]++' 时间值:'+str(pidObject[2])
            warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorCpu(cpuIdleLimit,saveDbMsgDict):
    """
     1.根据CPU Idle的告警阀值，发送告警信息
    """
    warnToPersonList=[]
    cpuIdle=SystemInfo.getCpuIdle()
    if cpuIdle==None:
        log.info('psutil的插件没有安装，或者不支持psutil的低版本的linux。')
        return warnToPersonList
    saveDbMsgDict['cpuIdle']=cpuIdle
    if cpuIdleLimit.isdigit() and cpuIdle<float(cpuIdleLimit):
        log.info("CPU Idle告警: cpuIdle_limit:%s,real_cpuIdle:%s",cpuIdleLimit,str(cpuIdle))
        warnStr=MONITOR_NAME+' CPU Idle告警:cpuIdle_limit:'+cpuIdleLimit+' real_cpuIdle:'+str(cpuIdle)
        warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorMemory(aviPhymenLimit,saveDbMsgDict):
    """
     1.根据内存的告警阀值，发送告警信息
     2.将内存信息保存到数据库中.
    """
    warnToPersonList=[]
    memoryObject=SystemInfo.getMemoryInfo()
    if memoryObject==None:
        log.info('psutil的插件没有安装，或者不支持psutil的低版本的linux。')
        return warnToPersonList
    saveDbMsgDict['memory']=memoryObject
    if aviPhymenLimit.isdigit() and memoryObject[1]<float(aviPhymenLimit):
        log.info("内存告警: aviPhymenLimit:%sKB,real_aviPhymen:%sKB",aviPhymenLimit,str(memoryObject[1]))
        warnStr=MONITOR_NAME+' 内存告警:aviPhymenLimit:'+aviPhymenLimit+'KB real_aviPhymen:'+str(memoryObject[1])+'KB'
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
    monitorDiskObjectList=[]
    if monitorSystemObject.has_key('hardspace_name')==False or monitorSystemObject.has_key('hardspace_limit')==False:
        return warnToPersonList
    elif len(monitorSystemObject['hardspace_name'].split('||'))<>len(monitorSystemObject['hardspace_limit'].split('||')):
        log.info('磁盘监控:monitor_pt_system_info表的hardspace_name值与hardspace_limit值配置的不完全匹配')
        return warnToPersonList
    for i in range(len(monitorSystemObject['hardspace_name'].split('||'))):
        monitorDiskObjectList.append({'hardspace_name':monitorSystemObject['hardspace_name'].split('||')[i],'hardspace_limit':monitorSystemObject['hardspace_limit'].split('||')[i]})
    for monitorDiskObject in monitorDiskObjectList:
        try:
            if monitorDiskObject.has_key('hardspace_name') and monitorDiskObject['hardspace_limit'].isdigit():
                for hardSpace in hardSpaceList:#(文件系统,已用空间,可用空间,已用%,挂载点)
                    if monitorDiskObject['hardspace_name']==hardSpace[0] and float(hardSpace[4])>=float(monitorDiskObject['hardspace_limit']):
                        log.info("磁盘空间告警: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],hardSpace[4])
                        warnStr=MONITOR_NAME+' 磁盘空间告警:hardspace_name:'+monitorDiskObject['hardspace_name']+' limit_used_percent:'+monitorDiskObject['hardspace_limit']+' real_used_percent:'+hardSpace[4]
                        warnToPersonList.append(warnStr)
                    elif monitorDiskObject['hardspace_name']==hardSpace[0]:
                        log.info("磁盘空间:达不到告警阀值 hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],hardSpace[4])
        except Exception:
            log.exception('磁盘监控报错:%s,告警阀值为:%s',monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'])

    return warnToPersonList

def monitorNetstat(monitorNetstatObjectList):
    """
      监控机器上的netstat的连接数。通过netstat -nat|grep -i '关键字'|wc -l。获取连接数大小.
    """
    warnToPersonList=[]
    for monitorNetstatObject in monitorNetstatObjectList:
        log.info('netstat连接监控: 执行监控命令 %s',str(monitorNetstatObject['command']))
        netstatmsgStd=os.popen(monitorNetstatObject['command'])
        real_count=netstatmsgStd.read().strip()
        log.info('netstat连接监控: 执行结果为 %s,监控阀值为 %s',real_count,str(monitorNetstatObject['netstat_limit']))
        if int(real_count)>=int(monitorNetstatObject['netstat_limit']):
            warnStr=MONITOR_NAME+' netstat连接数告警:命令:'+str(monitorNetstatObject['command'])+'实际连接数:'+real_count+' 监控阀值为:'+str(monitorNetstatObject['netstat_limit'])
            warnToPersonList.append(warnStr)


    return warnToPersonList
def backupFile():
    """
      backupObject['backup_path'] 需要备份的文件的路径,||作为分隔如果多个路径需要备份.
      backupObject['ip'].备份FTP的地址
      backupObject['user'].备份FTP的用户名
      backupObject['password'].备份FTP的密码
      backupObject['ftp_backup_path'].备份FTP的路径.
      备份平台的日志。
    """
    backupObject={}
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_pt_backup_file", MONITOR_NAME, URL)
    if outputParam.is_success() and len(outputParam.get_tables().get_table_list())>0:#判断是否有值
        backupObject['backup_path']=outputParam.get_column_value(0,0,0)
        backupObject['ip']=outputParam.get_column_value(0,0,1)
        backupObject['user']=outputParam.get_column_value(0,0,2)
        backupObject['password']=outputParam.get_column_value(0,0,3)
        backupObject['ftp_backup_path']=outputParam.get_column_value(0,0,4)
    else:#不需要备份，返回.
        return ;
    convertUnicodeToStr(backupObject)
    backupPath=backupObject['backup_path']
    backupPathList=backupPath.split('||')
    zipFileNameList=[]
    for backupPath in backupPathList:
        if os.path.isdir(backupPath):
            for root,dirnames,filenames in os.walk(backupPath):
                for filename in filenames:
                    if filename.find('core')==-1 and filename.find('.log')==-1 and filename.find('nohup.out')==-1 and filename.find('.bak')==-1 and filename<>'.' and filename<>'..':
                        zipFileNameList.append(os.path.join(root,filename))
        elif os.path.isfile(backupPath):
            zipFileNameList.append(backupPath)
        else:
            log.info('无法识别的备份路径:%s',backupPath)

    isCreateZipFileSucess=True
    if len(zipFileNameList)>0:
        strCurrDate=datetime.date.today().strftime('%Y%m%d')
        zipFileName=config_dir+strCurrDate+'.tar.gz'
        zipFile=tarfile.open(zipFileName,"w:gz")#ZipFile(zipFileName,'w')
        try:
            for filename in zipFileNameList:
                log.info('备份'+filename)
                zipFile.add(filename)
            zipFile.close()
        except Exception:
            isCreateZipFileSucess=False
            log.exception('压缩备用日志出错.文件名:%s',zipFileName)
        #finally:
        if isCreateZipFileSucess==False:return#创建不成功返回.
        ################################上传到FTP服务器##########################
        ftp=FTP(backupObject['ip'],backupObject['user'],backupObject['password'])
        ftpBackupPathList=[]
        ftpBackupPathList.append(backupObject['ftp_backup_path'])
        ftpBackupPathList.append(backupObject['ftp_backup_path']+'/'+MONITOR_NAME)
        for ftpBackupPath in ftpBackupPathList:#修改，并且创建路径.
            try:
                ftp.cwd(ftpBackupPath)
            except Exception:
                log.info('creating direcotry '+ ftp.mkd(ftpBackupPath))
                ftp.cwd(ftpBackupPath)
        try:
            uploadzipFile=open(zipFileName)
            log.info('upload file:%s ',zipFileName)
            ftp.storbinary('STOR '+os.path.split(zipFileName)[1],uploadzipFile)
            uploadzipFile.close()
            os.remove(zipFileName)
        except Exception:
            log.exception('上次日志备份文件错误，文件名:%s',zipFileName)
        return

def sendToAlive():
    """
     更新monitor_pt_alive_log表，表示本服务处于存活状态,通过脚本的计划监控，如果这个服务器在一定
     时间内没有更新，表示服务器出现异常。需要告警处理。
    """
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_alive", MONITOR_NAME, URL)
def saveSystemInfo(saveDbMsgDict):
    """
     将收集到的系统信息保存大数据库中.
    """
    procCpuList=[]
    try:
        procCpuList=saveDbMsgDict['procCpu']#[(name,pid,usedCpu,usedMemory)]
    except KeyError:
        pass
    cpuIdle=None
    try:
        cpuIdle=saveDbMsgDict['cpuIdle']
    except KeyError:
        pass
    memoryObject=()
    try:
        memoryObject=saveDbMsgDict['memory']#(total_phymen,avi_phymen.used_phymen) KB
    except KeyError:
        pass
    hardSpaceList=[]
    try:
        hardSpaceList=saveDbMsgDict['hardSpace']#[(文件系统,总计大小,已用空间,可用空间,已用%,挂载点)]
    except KeyError:
        pass
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

def getNohupVersion(monitorList):
    """
     将写在nohup.out文件中程序的版本，提取出来写到数据库中。nohup.out中的文件格式一般为:
******************************************************
*       SVCSMGR           2.4.3                      *
*       SVCSMGR_LIB     Version=2.0                  *
******************************************************
******************************************************
*       SVCSMGR           2.4.3                      *
*       SVCSMGR_LIB     Version=2.0                  *
******************************************************
******************************************************
*       SVCSMGR           2.4.3                      *
*       SVCSMGR_LIB     Version=2.0                  *
******************************************************
或者为:virmgr
        ******************************************************
        *         VRI MANAGER     Release V1.4.0             *
        ******************************************************
[TMLIB_RUN]: In 10 second process 1471 times.
[TMLIB_RUN]: In 10 second process 1534 times.
[TMLIB_RUN]: In 10 second process 1523 times.
[TMLIB_RUN]: In 10 second process 1682 times.
[TMLIB_RUN]: In 10 second process 1617 times.
[TMLIB_RUN]: In 10 second process 1731 times.
[TMLIB_RUN]: In 10 second process 1778 times.
[TMLIB_RUN]: In 10 second process 1720 times.
[TMLIB_RUN]: In 10 second process 1636 times.
[TMLIB_RUN]: In 10 second process 1642 times.
[TMLIB_RUN]: In 10 second process 1684 times.
[TMLIB_RUN]: In 10 second process 1446 times.
[TMLIB_RUN]: In 10 second process 1582 times.
[TMLIB_RUN]: In 10 second process 1683 times.
[TMLIB_RUN]: In 10 second process 1582 times.
[TMLIB_RUN]: In 10 second process 1537 times.
[TMLIB_RUN]: In 10 second process 1721 times.
[TMLIB_RUN]: In 10 second process 1727 times.
    """
    try:
        #ctserver,websphere,不要获取版本
        if len(monitorList)<>0 and monitorList[0]['log_type'] in ['websphere','ctserver']:
            return
        if len(monitorList)>0:
            nohupFilePath=os.path.split(monitorList[0]['monitorFile'])[0]
            nohupFilePath=nohupFilePath+'/../../bin'+os.sep+'nohup.out'
        else:
            nohupFilePath=config_dir+'../bin/nohup.out'

        if os.path.isfile(nohupFilePath)==False:
            log.info('从nohup中获取程序版本:找不到:%s文件',nohupFilePath)
            return
        if len(monitorList)>0 and monitorList[0]['log_type']=='vrimgr':
            commondStr='tail -30 '+nohupFilePath
            searchLogStd=os.popen(commondStr)
            lineLogList=searchLogStd.readlines()
            lineLogLength=len(lineLogList)
            versionCountPointor=-1
            for i in range(lineLogLength):
                versionCountPointor=lineLogLength-(i+1)
                lineLog=lineLogList[versionCountPointor]
                if lineLog.find('***************')<>-1:
                    break;
            if versionCountPointor<0:
                return
            versionMsg=lineLogList[versionCountPointor-1].replace('*','').strip()
        else:
            commondStr='tail -4 '+nohupFilePath
            searchLogStd=os.popen(commondStr)
            lineLogList=searchLogStd.readlines()
            #没有值，或者不是**********开头的.
            if len(lineLogList)==0 or len(lineLogList)<>4 or lineLogList[0].find('**********')==-1 :
                return
            versionMsg=lineLogList[1].replace('*','').strip()+' '+lineLogList[2].replace('*','').strip()

        log.info('程序的版本号为:%s',versionMsg)
        paramUtil=ParamUtil()
        outputParam=paramUtil.invoke("Monitor_nohupVersion", MONITOR_NAME+LinkConst.SPLIT_COLUMN+versionMsg, URL)
    except Exception:
        log.exception('getNohupVersion办法执行异常')

def get_version():
    version ='1.2.0.8'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  pt_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.01.17 modify time:2012.01.27')
    log.info(' 功能点1.监控平台日志')
    log.info('      2.监控CPU，内存、线程、硬盘告警信息')
    log.info('      3.收集CPU，内存、线程、硬盘资源信息')
    log.info('      4.监控平台下的core文件生成')
    log.info('      5.备份平台的配置及程序')
    log.info('      6.监控平台的指定的线程是否有存在')
    log.info('      7.监控平台增加netstat命令的监控')
    log.info('      8.增加系统是否死机的检测')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'PATCH', URL)
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

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    ##文件监控的短信告警，由于websphere的日志报警的时，日志跳动不频繁，造成同一的短信一直告警。
    lastmonitorFileSmContent='' #文件监控的短信告警
    readLastmonitorFileSmContent()
    # set Logger Config
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'monitor.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)



    getCommonConfig()
    get_version()
    #表示系统处于存活状态.
    sendToAlive()
    log.info('URL:%s,MONITOR_NAME:%s'%(URL,MONITOR_NAME))
    monitorFileList,monitorSystemInfo,monitorProcList,monitorNetstatObjectList=getMonitorService()
    if len(monitorFileList)==0 and len(monitorSystemInfo)==0 and len(monitorProcList)==0:
        log.info( '没有该IVR的监控配置信息，请查看Monitor_Pt_Config服务.')
        sys.exit()
    #文件监控
    warnToPersonList=monitorFile(monitorFileList)
    #core文件监控
    warnToPersonList=warnToPersonList+monitorCoreFile(monitorFileList)
    saveDBMsgDict={}
    #线程监控
    if len(monitorProcList)>0:
        warnToPersonList=warnToPersonList+monitorProcExist(monitorProcList)
        #warnToPersonList=warnToPersonList+monitorProcCpu(monitorProcList,saveDBMsgDict)
    #cpu监控
    if monitorSystemInfo.has_key('cpu_idle_limit'):
        warnToPersonList=warnToPersonList+monitorCpu(monitorSystemInfo['cpu_idle_limit'],saveDBMsgDict)
    #内存监控
    if monitorSystemInfo.has_key('memory_avi_limit'):
        warnToPersonList=warnToPersonList+monitorMemory(monitorSystemInfo['memory_avi_limit'],saveDBMsgDict)
    #硬盘监控
    warnToPersonList=warnToPersonList+monitorHardSpace(monitorSystemInfo,saveDBMsgDict)
    #netstat监控
    warnToPersonList=warnToPersonList+monitorNetstat(monitorNetstatObjectList)



    #备份程序
    backupFile()
    #程序的版本信息收集
    getNohupVersion(monitorFileList)

    saveSystemInfo(saveDBMsgDict)
    if len(warnToPersonList)==0:
        log.info( '没有告警信息')
        h1.close()
        sys.exit()
    sendToWarn(warnToPersonList)
    h1.close()
