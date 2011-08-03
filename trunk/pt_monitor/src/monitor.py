#!/usr/bin/env python
# -*- coding:GBK -*-
'''
Created on 2011-1-3

@author: ����

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
        if isinstance(unicodeMap[key],unicode):#�������Ĺؼ��֣�Ҫ��unicode����ת��Ϊstr����.
            unicodeMap[key]=unicodeMap[key].encode('GBK')

def getCommonConfig():
    """
      ��ȡivrtrack.ini�������ļ���Ϣ
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
       ���÷����ȡ��ص��ļ�
       ����һ���б����ݽṹ����:
       ����ؼ���֮���Զ������ָ�.
       [{'monitorFile':����ļ�,'keys':�ؼ��֣�'countMonitor':�����澯,'tailRowNum':tail������,'procName':CPU�߳���,'procCpuLimit'��CPU�澯��ֵ},('monitorFile':����ļ�,'keys':�ؼ��֣�'countMonitor':�����澯)]
       	        1 monitorFile monitorFile ����ļ���·��
				2 keys keys ��عؼ��֣�����ؼ���֮�䰴�ж��ŷָ�
				3 countMonitor countMonitor �澯��ֵ
				4 tailRowNum tailRowNum ����ļ�������
                5 log_type   log_type   ��־����:websphere,svcsmgr,ctserver��
				��2   rows=1 cols=4
				1 cpu_idle_limit cpu_idle_limit CPU�澯��ֵ
				2 memory_avi_limit memory_avi_limit �����ڴ�澯��ֵ(KB)
				3 hardspace_name hardspace_name Ӳ������(����/dev/sda3)
				4 hardspace_limit hardspace_limit Ӳ�̸澯��ֵ
				��3   rows=1 cols=2
				1 proc_name proc_name �߳�����
				2 proc_cpu_limit proc_cpu_limit �߳�CPU�澯��ֵ

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
            if monitorObject['monitorFile']=='':#����ǿգ���ʾû��������־���
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
            if monitorProcObject['proc_name']=='':#����ǿգ���ʾû�������̼߳��
                continue
            else:
                monitorProcObjectList.append(monitorProcObject)
    return (monitorFileList,monitorSystemObject,monitorProcObjectList)

def monitorFile(monitorList):
    """
     �����־�ļ�.������Ҫ�澯����־��
    """
    CTI_ERR_KEY='"ConsultationCall\[7\]",OperResult=\[1\]'
    warnToPersonList=[]
    for monitorObject in monitorList:
        #��ز�����ʼ��
        appearCountOfKeyMap={}
        keyList=[]
        if isinstance(monitorObject['keys'],unicode):#�������Ĺؼ��֣�Ҫ��unicode����ת��Ϊstr����.
            keyList=monitorObject['keys'].encode('GBK').split('||')
        else:
            keyList=monitorObject['keys'].split('||')
        for key in keyList:
            appearCountOfKeyMap[key]=0
            log.info('search key:'+key)

        bIsGrepInCtServer=False #�ж��Ƿ��а���CTI�Ĺؼ���.
        try:
            if monitorObject['log_type']=='ctserver' and keyList.index(CTI_ERR_KEY)>-1:
                commondStr='grep \''+CTI_ERR_KEY+'\' '+monitorObject['monitorFile']+' |wc -l'
                bIsGrepInCtServer=True
                keyList.remove(CTI_ERR_KEY)#�������־���Բ���Ҫ����CTI�Ĺؼ���..
                log.info(commondStr)
                searchLogStd=os.popen(commondStr)
                for lineLog in  searchLogStd.readlines():
                    appearCountOfKeyMap[CTI_ERR_KEY]=int(lineLog)
        except ValueError:
            pass

        commondStr='tail -'
        commondStr=commondStr+monitorObject['tailRowNum']+' '+monitorObject['monitorFile']
        isWarnToPerson=True #��Ҫ���Ÿ澯.
        if len(keyList)>0:
            log.info(commondStr)
            searchLogStd=os.popen(commondStr)
            for lineLog in searchLogStd.readlines():#�Ƿ��йؼ�������
                for key in keyList:
                    if re.search(key,lineLog):appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
            ##����Systemout��־�Ƚ��ٴ����Զ�����ʱ����һ���жϣ�������һ����־��ʱ����5����֮ǰ�ľͲ��澯��.
            if monitorObject['monitorFile'].find('SystemOut.log')>0:
                try:
                    lastLineDateTuple=time.strptime(lineLog[1:16],'%y-%m-%d %H:%M:%S')
                    fiveMiniuteBefore=datetime.datetime.now()+datetime.timedelta(minutes=-7)
                    lastLineDate=datetime.datetime(lastLineDateTuple.tm_year,lastLineDateTuple.tm_mon,lastLineDateTuple.tm_mday,lastLineDateTuple.tm_hour,lastLineDateTuple.tm_min,lastLineDateTuple.tm_sec)
                    if lastLineDate<fiveMiniuteBefore:isWarnToPerson=False
                except TypeError:
                    pass


        if bIsGrepInCtServer:keyList.append(CTI_ERR_KEY)#CTI�Ĺؼ��ּ�������.
        for key in keyList:
            log.info( 'key:%s,realLimit:%d,warnLimit:%s'%(key,appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if isWarnToPerson and appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#����澯������д�澯����
                warnStr=MONITOR_NAME+' �澯,��־�ļ�:'+monitorObject['monitorFile']+' �ؼ���:'+key+' ���ִ���:'+str(appearCountOfKeyMap[key])
                log.info(warnStr)
                warnToPersonList.append(warnStr)
    return warnToPersonList

def sendToWarn(warnToPersonList):
    """
    ���͸澯��Ϣ����Ӧ����ϵ��Ա
    """
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    inputStr=inputStr+'\r\n'.join(warnToPersonList)
    log.info('�澯���Ͷ���:%s',inputStr)
    outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    flag=''
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    return flag=='0'
def monitorCoreFile(monitorList):
    """
      �����־Ŀ¼�£��Ƿ��д���core�ļ�.
    """
    warnToPersonList=[]
    fiveMiniuteBefore=datetime.datetime.now()+datetime.timedelta(minutes=-5)#���5����֮ǰ�Ƿ���core��־.
    currTime=datetime.datetime.now()
    for monitorObject in monitorList:
        fileTime=datetime.datetime.now()
        corePathFile=os.path.split(monitorObject['monitorFile'])[0]
        if  monitorObject['log_type']=='ctserver' or monitorObject['log_type']=='svcsmgr':
            #�Ƶ��ϼ����ϼ�Ŀ¼���൱��/home/tnsmcc/LOG/svcsmgr ->�����/home/tnsmcc/bin
            corePathFile=corePathFile+'/../../bin'+os.sep+'core.*'
             #�Ƶ��ϼ����ϼ�Ŀ¼���൱��/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/test_server2 ->�����/opt/IBM/WebSphere/AppServer/profiles/AppSrv01
        elif monitorObject['log_type']=='websphere':
            corePathFile=corePathFile+'/../..'+os.sep+'javacore.*'
        else:#�������͵�core��ʱ�������.
            log.info('��־���ͣ�%s,����core�ļ����.',monitorObject['log_type'])
            continue
        log.info('��ѯcore�ļ�.'+corePathFile)
        fileList=glob.glob(corePathFile)
        for filename in fileList:
            log.info('filename:%s',filename)
            fileTimeTuple=time.localtime(os.path.getctime(filename))
            #�������ڶ���
            fileTime=datetime.datetime(fileTimeTuple.tm_year,fileTimeTuple.tm_mon,fileTimeTuple.tm_mday,fileTimeTuple.tm_hour,fileTimeTuple.tm_min,fileTimeTuple.tm_sec)
            #log.info('fileTime:%s,fiveMiniuteBefore:%s,currTime:%s',str(fileTime),str(fiveMiniuteBefore),str(currTime))
            if fiveMiniuteBefore<fileTime<currTime:#�ļ�����ʱ����5������.
                warnStr=MONITOR_NAME+' �澯,����core�ļ����ļ���:'+filename
                log.info(warnStr)
                warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorProcExist(monitorObjectList):
    """
     �ж�ָ�����߳��Ƿ��д��ڡ�
     @monitorObjectList: [{'proc_name':procName,'proc_cpu_limit':procCpuLimit}]
    """
    warnToPersonList=[]
    procNameMap={}
    for monitorProcObject in monitorObjectList:
        if procNameMap.has_key(monitorProcObject['proc_name'])==False:
            procNameMap[monitorProcObject['proc_name']]=False
    pidObjectList=SystemInfo.getCPUUsedByPidName(procNameMap.keys())
    for pidObject in pidObjectList:#����߳��Ѿ����ڣ���״̬���ó�True
        procNameMap[pidObject[0]]=True
    warnStr=''
    for procName,isExist in procNameMap.iteritems():
        if isExist==False and len(warnStr)==0:
            warnStr=MONITOR_NAME+' �̸߳澯:�߳�����:'+procName+'������.'
        elif isExist==False:
            warnStr+=',�߳�����:'++procName+'������.'
    if len(warnStr)>0:
        log.info('�̸߳澯: %s',warnStr)
        warnToPersonList.append(warnStr)
    return warnToPersonList


def monitorProcCpu(monitorObjectList,saveDbMsgDict):
    """
    1.�����߳����ƻ�ȡ��Ӧ�̵߳ĸ澯��Ϣ.
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
            log.info('�߳�CPU�澯: pid:%s,pid_name:%s,cpu_limit:%s,real_cpu:%s',pidObject[0],pidObject[1],procNameMap[pidObject[0]],str(pidObject[2]))
            warnStr=MONITOR_NAME+' �߳�CPU�澯:�߳�����:'+pidObject[0]+' �߳�ID:'+pidObject[1]+' ��ֵ:'+procNameMap[pidObject[0]]++' ʱ��ֵ:'+str(pidObject[2])
            warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorCpu(cpuIdleLimit,saveDbMsgDict):
    """
     1.����CPU Idle�ĸ澯��ֵ�����͸澯��Ϣ
    """
    warnToPersonList=[]
    cpuIdle=SystemInfo.getCpuIdle()
    saveDbMsgDict['cpuIdle']=cpuIdle
    if cpuIdleLimit.isdigit() and cpuIdle<float(cpuIdleLimit):
        log.info("CPU Idle�澯: cpuIdle_limit:%s,real_cpuIdle:%s",cpuIdleLimit,str(cpuIdle))
        warnStr=MONITOR_NAME+' CPU Idle�澯:cpuIdle_limit:'+cpuIdleLimit+' real_cpuIdle:'+str(cpuIdle)
        warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorMemory(aviPhymenLimit,saveDbMsgDict):
    """
     1.�����ڴ�ĸ澯��ֵ�����͸澯��Ϣ
     2.���ڴ���Ϣ���浽���ݿ���.
    """
    warnToPersonList=[]
    memoryObject=SystemInfo.getMemoryInfo()
    saveDbMsgDict['memory']=memoryObject
    if aviPhymenLimit.isdigit() and memoryObject[1]<float(aviPhymenLimit):
        log.info("�ڴ�澯: aviPhymenLimit:%sKB,real_aviPhymen:%sKB",aviPhymenLimit,str(memoryObject[1]))
        warnStr=MONITOR_NAME+' �ڴ�澯:aviPhymenLimit:'+aviPhymenLimit+'KB real_aviPhymen:'+str(memoryObject[1])+'KB'
        warnToPersonList.append(warnStr)
    return warnToPersonList
def monitorHardSpace(monitorSystemObject,saveDbMsgDict):
    """
     1.����Ӳ�����õĸ澯��ֵ�����ͱ�����Ϣ
     @monitorSystemObject {'cpu_idle_limit':cpu_idle_limit,'memory_avi_limit':memory_avi_limit,'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}
    """
    hardSpaceList=SystemInfo.getHardSpace()#[(�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�)]
    saveDbMsgDict['hardSpace']=hardSpaceList
    warnToPersonList=[]
    if monitorSystemObject.has_key('hardspace_name') and monitorSystemObject['hardspace_limit'].isdigit():
        for hardSpace in hardSpaceList:#(�ļ�ϵͳ,���ÿռ�,���ÿռ�,����%,���ص�)
            if monitorSystemObject['hardspace_name']==hardSpace[0] and float(hardSpace[4])>=float(monitorSystemObject['hardspace_limit']):
                log.info("���̿ռ�澯: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorSystemObject['hardspace_name'],monitorSystemObject['hardspace_limit'],hardSpace[4])
                warnStr=MONITOR_NAME+' ���̿ռ�澯:hardspace_name:'+monitorSystemObject['hardspace_name']+' limit_used_percent:'+monitorSystemObject['hardspace_limit']+' real_used_percent:'+hardSpace[4]
                warnToPersonList.append(warnStr)
    return warnToPersonList
def backupFile():
    """
      backupObject['backup_path'] ��Ҫ���ݵ��ļ���·��,||��Ϊ�ָ�������·����Ҫ����.
      backupObject['ip'].����FTP�ĵ�ַ
      backupObject['user'].����FTP���û���
      backupObject['password'].����FTP������
      backupObject['ftp_backup_path'].����FTP��·��.
      ����ƽ̨����־��
    """
    backupObject={}
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_pt_backup_file", MONITOR_NAME, URL)
    if outputParam.is_success() and len(outputParam.get_tables().get_table_list())>0:#�ж��Ƿ���ֵ
        backupObject['backup_path']=outputParam.get_column_value(0,0,0)
        backupObject['ip']=outputParam.get_column_value(0,0,1)
        backupObject['user']=outputParam.get_column_value(0,0,2)
        backupObject['password']=outputParam.get_column_value(0,0,3)
        backupObject['ftp_backup_path']=outputParam.get_column_value(0,0,4)
    else:#����Ҫ���ݣ�����.
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
                log.info('����'+filename)
                zipFile.add(filename)
            zipFile.close()
        except Exception:
            isCreateZipFileSucess=False
            log.exception('ѹ��������־����.�ļ���:%s',zipFileName)
        #finally:
        if isCreateZipFileSucess==False:return#�������ɹ�����.
        ################################�ϴ���FTP������##########################
        ftp=FTP(backupObject['ip'],backupObject['user'],backupObject['password'])
        ftpBackupPathList=[]
        ftpBackupPathList.append(backupObject['ftp_backup_path'])
        ftpBackupPathList.append(backupObject['ftp_backup_path']+'/'+MONITOR_NAME)
        for ftpBackupPath in ftpBackupPathList:#�޸ģ����Ҵ���·��.
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
            log.exception('�ϴ���־�����ļ������ļ���:%s',zipFileName)
        return

def saveSystemInfo(saveDbMsgDict):
    """
     ���ռ�����ϵͳ��Ϣ��������ݿ���.
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
        hardSpaceList=saveDbMsgDict['hardSpace']#[(�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�)]
    except KeyError:
        pass
    table_1List=[str(cpuIdle)]
    for object in memoryObject:
        table_1List.append(str(object))
    #table1:host_name
    #table2:cpu_idle,total_phy_men,avi_phymen,used_phymen
    #table3:proc_name,pid,used_cpu,used_memory.�п����Ƕ���.
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
        log.info('����savePtResourceInfo����ɹ�.�������:%s,������:%s',inputStr,flagMsg)
    else:
        log.info('����savePtResourceInfo����ʧ��.�������:%s',inputStr)


def get_version():
    version ='1.1.0.13'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  pt_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.01.17 modify time:2011.08.02')
    log.info(' ���ܵ�1.���ƽ̨��־')
    log.info('      2.���CPU���ڴ桢�̡߳�Ӳ�̸澯��Ϣ')
    log.info('      3.�ռ�CPU���ڴ桢�̡߳�Ӳ����Դ��Ϣ')
    log.info('      4.���ƽ̨�µ�core�ļ�����')
    log.info('      5.����ƽ̨�����ü�����')
    log.info('      6.���ƽ̨��ָ�����߳��Ƿ��д���')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'PATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('���ݿ�İ汾����:'+str(versionMsg))
    if versionMsg.has_key('version') and version<>versionMsg['version']:
        log.info(' ���ֳ���汾�����µģ��汾��Ϊ%s,��ʼ���³���',versionMsg['version'])
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
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
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
        log.info( 'û�и�IVR�ļ��������Ϣ����鿴Monitor_Pt_Config����.')
        sys.exit()
    #�ļ����
    warnToPersonList=monitorFile(monitorFileList)
    #core�ļ����
    warnToPersonList=warnToPersonList+monitorCoreFile(monitorFileList)
    saveDBMsgDict={}
    #�̼߳��
    if len(monitorProcList)>0:
        warnToPersonList=warnToPersonList+monitorProcExist(monitorProcList)
        #warnToPersonList=warnToPersonList+monitorProcCpu(monitorProcList,saveDBMsgDict)
    #cpu���
    if monitorSystemInfo.has_key('cpu_idle_limit'):
        warnToPersonList=warnToPersonList+monitorCpu(monitorSystemInfo['cpu_idle_limit'],saveDBMsgDict)
    #�ڴ���
    if monitorSystemInfo.has_key('memory_avi_limit'):
        warnToPersonList=warnToPersonList+monitorMemory(monitorSystemInfo['memory_avi_limit'],saveDBMsgDict)
    #Ӳ�̼��
    warnToPersonList=warnToPersonList+monitorHardSpace(monitorSystemInfo,saveDBMsgDict)


    #���ݳ���
    backupFile()

    saveSystemInfo(saveDBMsgDict)
    if len(warnToPersonList)==0:
        log.info( 'û�и澯��Ϣ')
        h1.close()
        sys.exit()
    sendToWarn(warnToPersonList)
    h1.close()
