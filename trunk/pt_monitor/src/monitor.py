#!/usr/bin/env python
# -*- coding:GBK -*-
'''
Created on 2011-1-3

@author: 林桦

'''
import ConfigParser
import os
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
    config=ConfigParser.ConfigParser()
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
                5 log_type   log_type   日志类型:websphere,svcsmgr,ctserver等
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
    return (monitorFileList,monitorSystemObject,monitorProcObjectList)

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
        isWarnToPerson=True #需要短信告警.
        if len(keyList)>0:
            log.info(commondStr)
            searchLogStd=os.popen(commondStr)
            for lineLog in searchLogStd.readlines():#是否有关键字内容
                for key in keyList:
                    if re.search(key,lineLog):appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
            ##由于Systemout日志比较少打，所以对最后的时间做一个判断，如果最后一条日志的时间在5分钟之前的就不告警了.
            if monitorObject['monitorFile'].find('SystemOut.log')>0:
                try:
                    lastLineDateTuple=time.strptime(lineLog[1:16],'%y-%m-%d %H:%M:%S')
                    fiveMiniuteBefore=datetime.datetime.now()+datetime.timedelta(minutes=-7)
                    lastLineDate=datetime.datetime(lastLineDateTuple.tm_year,lastLineDateTuple.tm_mon,lastLineDateTuple.tm_mday,lastLineDateTuple.tm_hour,lastLineDateTuple.tm_min,lastLineDateTuple.tm_sec)
                    if lastLineDate<fiveMiniuteBefore:isWarnToPerson=False
                except TypeError:
                    pass


        if bIsGrepInCtServer:keyList.append(CTI_ERR_KEY)#CTI的关键字加入运算.
        for key in keyList:
            log.info( 'key:%s,realLimit:%d,warnLimit:%s'%(key,appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if isWarnToPerson and appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#到达告警条件，写告警内容
                warnStr=MONITOR_NAME+' 告警,日志文件:'+monitorObject['monitorFile']+' 关键字:'+key+' 出现次数:'+str(appearCountOfKeyMap[key])
                log.info(warnStr)
                warnToPersonList.append(warnStr)
    return warnToPersonList

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
    if monitorSystemObject.has_key('hardspace_name') and monitorSystemObject['hardspace_limit'].isdigit():
        for hardSpace in hardSpaceList:#(文件系统,已用空间,可用空间,已用%,挂载点)
            if monitorSystemObject['hardspace_name']==hardSpace[0] and float(hardSpace[4])>=float(monitorSystemObject['hardspace_limit']):
                log.info("磁盘空间告警: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorSystemObject['hardspace_name'],monitorSystemObject['hardspace_limit'],hardSpace[4])
                warnStr=MONITOR_NAME+' 磁盘空间告警:hardspace_name:'+monitorSystemObject['hardspace_name']+' limit_used_percent:'+monitorSystemObject['hardspace_limit']+' real_used_percent:'+hardSpace[4]
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
        for root,dirnames,filenames in os.walk(backupPath):
            for filename in filenames:
                if filename.find('core')==-1 and filename.find('.log')==-1 and filename.find('nohup.out')==-1 and filename.find('.bak')==-1 and filename<>'.' and filename<>'..':
                    zipFileNameList.append(os.path.join(root,filename))
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
            #os.remove(zipFileName)
        except Exception:
            log.exception('上次日志备份文件错误，文件名:%s',zipFileName)
        return

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


def get_version():
    version ='1.1.0.13'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  pt_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.01.17 modify time:2011.08.02')
    log.info(' 功能点1.监控平台日志')
    log.info('      2.监控CPU，内存、线程、硬盘告警信息')
    log.info('      3.收集CPU，内存、线程、硬盘资源信息')
    log.info('      4.监控平台下的core文件生成')
    log.info('      5.备份平台的配置及程序')
    log.info('      6.监控平台的指定的线程是否有存在')
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
    log.info('URL:%s,MONITOR_NAME:%s'%(URL,MONITOR_NAME))
    monitorFileList,monitorSystemInfo,monitorProcList=getMonitorService()
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


    #备份程序
    backupFile()

    saveSystemInfo(saveDBMsgDict)
    if len(warnToPersonList)==0:
        log.info( '没有告警信息')
        h1.close()
        sys.exit()
    sendToWarn(warnToPersonList)
    h1.close()
