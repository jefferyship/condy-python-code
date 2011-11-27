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
import datetime
import zipfile
import win32api
import thread

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
    global lastmonitorFileSmContent
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
    if config.has_option('common', 'lastmonitorFileSmContent'):
        lastmonitorFileSmContent=config.get('common', 'lastmonitorFileSmContent')
    else:lastmonitorFileSmContent=''

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def writeCommonConfig(option,value):
    """
     设置值到monitor.ini的common，section中.
    """
    config=ConfigParser.ConfigParser()
    config.read(config_dir+'monitorForWindow.ini')
    config.set('common',option,value)
    ivrtrackFileObject=open(config_dir+'monitorForWindow.ini',"r+")
    config.write(ivrtrackFileObject)
    ivrtrackFileObject.close()

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


def monitorDisk(monitorSystemObject,saveDbMsgDict):
    """
    @monitorSystemObject {'cpu_idle_limit':cpu_idle_limit,'memory_avi_limit':memory_avi_limit,'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}
    hardspace_name:有可能是用||分隔的多行参数.hardspace_limit:有可能是ongoing||分隔的多行.
    windows 版本的磁盘空间检查,monitorDiskOjectList [{'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}]
    """
    warnToPersonList=[]
    monitorDiskObjectList=[]
    saveToDBList=[]#[(文件系统,总计大小,已用空间,可用空间,已用%,挂载点)]
    if monitorSystemObject.has_key('hardspace_name')==False or monitorSystemObject.has_key('hardspace_limit')==False:
        return warnToPersonList
    elif len(monitorSystemObject['hardspace_name'].split('||'))<>len(monitorSystemObject['hardspace_limit'].split('||')):
        log.info('磁盘监控:monitor_pt_system_info表的hardspace_name值与hardspace_limit值配置的不完全匹配')
        return warnToPersonList
    for i in range(len(monitorSystemObject['hardspace_name'].split('||'))):
        monitorDiskObjectList.append({'hardspace_name':monitorSystemObject['hardspace_name'].split('||')[i],'hardspace_limit':monitorSystemObject['hardspace_limit'].split('||')[i]})

    saveDbMsgDict['hardSpace']=saveToDBList
    for monitorDiskObject in monitorDiskObjectList:
        try:
            log.info('磁盘告警配置：%s',str(monitorDiskObject))
            if monitorDiskObject['hardspace_limit'].isdigit():
                total,used,free,usedPecent=SystemInfo.getdiskByPath(monitorDiskObject['hardspace_name'])
                saveToDBList.append((monitorDiskObject['hardspace_name'],str(total/1024),str(used/1024),str(free/1024),str(usedPecent),''))
                limitPercent=float(monitorDiskObject['hardspace_limit'])
                if usedPecent>=limitPercent:
                    log.info("磁盘空间告警: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],str(round(usedPecent,2)))
                    warnStr=MONITOR_NAME+' 磁盘空间告警:hardspace_name:'+monitorDiskObject['hardspace_name']+' limit_used_percent:'+monitorDiskObject['hardspace_limit']+' real_used_percent:'+str(round(usedPecent,2))
                    warnToPersonList.append(warnStr)
            else:
                log.info('磁盘告警配置,磁盘空间%s的阀值非数值=%s',monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'])
        except Exception:
            log.exception('获取磁盘空间报错。磁盘为:'+monitorDiskObject['hardspace_name'])

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
        zipFileName=config_dir+strCurrDate+'.zip'
        zipFile=zipfile.ZipFile(zipFileName,'w')#tarfile.open(zipFileName,"w:gz")
        try:
            for filename in zipFileNameList:
                log.info('备份'+filename)
                zipFile.write(filename)
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
def sendToWarn(warnToPersonList):
    """
    发送告警信息跟相应的联系人员
    """
    global lastmonitorFileSmContent
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    currmonitorFileSmContent='\r\n'.join(warnToPersonList)
    if lastmonitorFileSmContent==currmonitorFileSmContent:
        log.info('重复告警短信不发送:%s',currmonitorFileSmContent)
        return True;

    outputParam=paramUtil.invoke("Monitor_machine_info", MONITOR_NAME, URL)
    planId=''
    if outputParam.is_success() :
       planId=outputParam.get_column_value(0,0,4)
    flag=''
    if planId!='':#调用10000号和外包都通用的服务，外包可以发送邮件。
        inputStr=planId.encode('GBK')+LinkConst.SPLIT_COLUMN+'A'+LinkConst.SPLIT_COLUMN+'\r\n'.join(warnToPersonList)
        outputParam=paramUtil.invoke("WarnToPerson", inputStr, URL)
    else:
        inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
        inputStr=inputStr+'\r\n'.join(warnToPersonList)
        outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    writeCommonConfig('lastmonitorFileSmContent',currmonitorFileSmContent)
    return flag=='0'

def sendToAlive():
    """
     更新monitor_pt_alive_log表，表示本服务处于存活状态,通过脚本的计划监控，如果这个服务器在一定
     时间内没有更新，表示服务器出现异常。需要告警处理。
    """
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_alive", MONITOR_NAME, URL)

def get_version():
    version ='1.1.0.2'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  monitorForWindow.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.08.12 modify time:2011.11.27')
    log.info(' 功能点1.监控windows的磁盘空间')
    log.info(' 功能点2.对指定的目录进行备份')
    log.info(' 功能点3.增加系统是否死机的检测,及程序自动更新')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'WINPATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('数据库的版本配置:'+str(versionMsg))
    needReloadProgram=False;
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
        needReloadProgram=True

    return (version,needReloadProgram)

def reloadProgram(path):
    """
      自动重启本程序
    """
    try:
        global isAleadyReload
        isAleadyReload=False
        log.info( '程序最新版本更新完毕，程序自动重启中.........')
        time.sleep(2)#等待2s中
        win32api.ShellExecute(0,'open',path,'','',1)#重启程序.
        log.info( '......................程序自动重启完成.......')
        h1.close()
    except Exception:
        log.exception('系统报错')
        h1.close()


if __name__ == '__main__':
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

##    monitorDiskObjectList=[]
##    monitorDiskObjectList.append({'hardspace_name':'c:\\','hardspace_limit':'1'})
##    monitorDiskObjectList.append({'hardspace_name':'d:\\','hardspace_limit':'1'})

    try:
        global isAleadyReload
        isAleadyReload=False
        while IS_START=='1':
            (version,needReloadProgram)=get_version()
            if needReloadProgram:#重新有更新，需要重启本程序.
                thread.start_new_thread(reloadProgram,(sys.argv[0]))#tempPath需要修改成本程序的程序名.
                break
            getCommonConfig()
            saveDBMsgDict={}
            sendToAlive()
            monitorFileList,monitorSystemInfo,monitorProcList,monitorNetstatObjectList=getMonitorService()
            warnToPersonList=monitorDisk(monitorSystemInfo,saveDBMsgDict)
            backupFile()
            saveSystemInfo(saveDBMsgDict)
            if len(warnToPersonList)==0:
                log.info( '没有告警信息')
            else:
                sendToWarn(warnToPersonList)
            time.sleep(RECYCLE_TIMES)
        log.info('IS_START value=:'+IS_START+' so exit!')
        if needReloadProgram==False: h1.close()# 如果needReloadProgram==True的话，就在reloadProgram()中关闭程序。
        else:
            for i in range(4):
                print '等待5s,程序尝试结束'
                time.sleep(5)#等待5s中,等待程序重启后关闭。
                if isAleadyReload==True:break

    except Exception:
        log.exception('系统报错')
        h1.close()

