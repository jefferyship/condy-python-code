# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        monitorForWindow.py
# Purpose:     window�汾�Ĵ��̼�أ��̼߳�ء�CPU���ڴ���.
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
     ����ֵ��monitor.ini��common��section��.
    """
    config=ConfigParser.ConfigParser()
    config.read(config_dir+'monitorForWindow.ini')
    config.set('common',option,value)
    ivrtrackFileObject=open(config_dir+'monitorForWindow.ini',"r+")
    config.write(ivrtrackFileObject)
    ivrtrackFileObject.close()

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
                ��4   rows=1 cols=2   �������
                  1 command  command  ִ����������� ����ִ��netstat -nat|grep -i '�ؼ���'|wc -l
                  2 netstat_limit netstat_limit ִ����������ֵķ�ֵ

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
        table4=outputParam.get_tables().get_one_table(3)
        if table4<>None:
            for row in table4.get_row_list():
                monitorNetstatObject={}
                monitorNetstatObject['command']=row.get_one_column(0).get_value()
                monitorNetstatObject['netstat_limit']=row.get_one_column(1).get_value()
                convertUnicodeToStr(monitorProcObject)
                if monitorNetstatObject['command']=='':#����ǿգ���ʾû������netstat����ļ��
                    continue
                else:
                    monitorNetstatObjectList.append(monitorNetstatObject)
    return (monitorFileList,monitorSystemObject,monitorProcObjectList,monitorNetstatObjectList)

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


def monitorDisk(monitorSystemObject,saveDbMsgDict):
    """
    @monitorSystemObject {'cpu_idle_limit':cpu_idle_limit,'memory_avi_limit':memory_avi_limit,'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}
    hardspace_name:�п�������||�ָ��Ķ��в���.hardspace_limit:�п�����ongoing||�ָ��Ķ���.
    windows �汾�Ĵ��̿ռ���,monitorDiskOjectList [{'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}]
    """
    warnToPersonList=[]
    monitorDiskObjectList=[]
    saveToDBList=[]#[(�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�)]
    if monitorSystemObject.has_key('hardspace_name')==False or monitorSystemObject.has_key('hardspace_limit')==False:
        return warnToPersonList
    elif len(monitorSystemObject['hardspace_name'].split('||'))<>len(monitorSystemObject['hardspace_limit'].split('||')):
        log.info('���̼��:monitor_pt_system_info���hardspace_nameֵ��hardspace_limitֵ���õĲ���ȫƥ��')
        return warnToPersonList
    for i in range(len(monitorSystemObject['hardspace_name'].split('||'))):
        monitorDiskObjectList.append({'hardspace_name':monitorSystemObject['hardspace_name'].split('||')[i],'hardspace_limit':monitorSystemObject['hardspace_limit'].split('||')[i]})

    saveDbMsgDict['hardSpace']=saveToDBList
    for monitorDiskObject in monitorDiskObjectList:
        try:
            log.info('���̸澯���ã�%s',str(monitorDiskObject))
            if monitorDiskObject['hardspace_limit'].isdigit():
                total,used,free,usedPecent=SystemInfo.getdiskByPath(monitorDiskObject['hardspace_name'])
                saveToDBList.append((monitorDiskObject['hardspace_name'],str(total/1024),str(used/1024),str(free/1024),str(usedPecent),''))
                limitPercent=float(monitorDiskObject['hardspace_limit'])
                if usedPecent>=limitPercent:
                    log.info("���̿ռ�澯: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],str(round(usedPecent,2)))
                    warnStr=MONITOR_NAME+' ���̿ռ�澯:hardspace_name:'+monitorDiskObject['hardspace_name']+' limit_used_percent:'+monitorDiskObject['hardspace_limit']+' real_used_percent:'+str(round(usedPecent,2))
                    warnToPersonList.append(warnStr)
            else:
                log.info('���̸澯����,���̿ռ�%s�ķ�ֵ����ֵ=%s',monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'])
        except Exception:
            log.exception('��ȡ���̿ռ䱨������Ϊ:'+monitorDiskObject['hardspace_name'])

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
        if os.path.isdir(backupPath):
            for root,dirnames,filenames in os.walk(backupPath):
                for filename in filenames:
                    if filename.find('core')==-1 and filename.find('.log')==-1 and filename.find('nohup.out')==-1 and filename.find('.bak')==-1 and filename<>'.' and filename<>'..':
                        zipFileNameList.append(os.path.join(root,filename))
        elif os.path.isfile(backupPath):
            zipFileNameList.append(backupPath)
        else:
            log.info('�޷�ʶ��ı���·��:%s',backupPath)

    isCreateZipFileSucess=True
    if len(zipFileNameList)>0:
        strCurrDate=datetime.date.today().strftime('%Y%m%d')
        zipFileName=config_dir+strCurrDate+'.zip'
        zipFile=zipfile.ZipFile(zipFileName,'w')#tarfile.open(zipFileName,"w:gz")
        try:
            for filename in zipFileNameList:
                log.info('����'+filename)
                zipFile.write(filename)
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
            os.remove(zipFileName)
        except Exception:
            log.exception('�ϴ���־�����ļ������ļ���:%s',zipFileName)
        return
def sendToWarn(warnToPersonList):
    """
    ���͸澯��Ϣ����Ӧ����ϵ��Ա
    """
    global lastmonitorFileSmContent
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    currmonitorFileSmContent='\r\n'.join(warnToPersonList)
    if lastmonitorFileSmContent==currmonitorFileSmContent:
        log.info('�ظ��澯���Ų�����:%s',currmonitorFileSmContent)
        return True;

    outputParam=paramUtil.invoke("Monitor_machine_info", MONITOR_NAME, URL)
    planId=''
    if outputParam.is_success() :
       planId=outputParam.get_column_value(0,0,4)
    flag=''
    if planId!='':#����10000�ź������ͨ�õķ���������Է����ʼ���
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
     ����monitor_pt_alive_log����ʾ�������ڴ��״̬,ͨ���ű��ļƻ���أ���������������һ��
     ʱ����û�и��£���ʾ�����������쳣����Ҫ�澯����
    """
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_alive", MONITOR_NAME, URL)

def get_version():
    version ='1.1.0.2'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  monitorForWindow.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.08.12 modify time:2011.11.27')
    log.info(' ���ܵ�1.���windows�Ĵ��̿ռ�')
    log.info(' ���ܵ�2.��ָ����Ŀ¼���б���')
    log.info(' ���ܵ�3.����ϵͳ�Ƿ������ļ��,�������Զ�����')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'PT_MONITOR'+LinkConst.SPLIT_COLUMN+'WINPATCH', URL)
    if outputParam.is_success():
        tables=outputParam.get_tables()
        table=tables.get_first_table()
        for row in table.get_row_list():
            versionMsg[row.get_one_column(0).get_value()]=row.get_one_column(1).get_value()
    convertUnicodeToStr(versionMsg)
    log.info('���ݿ�İ汾����:'+str(versionMsg))
    needReloadProgram=False;
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
        needReloadProgram=True

    return (version,needReloadProgram)

def reloadProgram(path):
    """
      �Զ�����������
    """
    try:
        global isAleadyReload
        isAleadyReload=False
        log.info( '�������°汾������ϣ������Զ�������.........')
        time.sleep(2)#�ȴ�2s��
        win32api.ShellExecute(0,'open',path,'','',1)#��������.
        log.info( '......................�����Զ��������.......')
        h1.close()
    except Exception:
        log.exception('ϵͳ����')
        h1.close()


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
        global isAleadyReload
        isAleadyReload=False
        while IS_START=='1':
            (version,needReloadProgram)=get_version()
            if needReloadProgram:#�����и��£���Ҫ����������.
                thread.start_new_thread(reloadProgram,(sys.argv[0]))#tempPath��Ҫ�޸ĳɱ�����ĳ�����.
                break
            getCommonConfig()
            saveDBMsgDict={}
            sendToAlive()
            monitorFileList,monitorSystemInfo,monitorProcList,monitorNetstatObjectList=getMonitorService()
            warnToPersonList=monitorDisk(monitorSystemInfo,saveDBMsgDict)
            backupFile()
            saveSystemInfo(saveDBMsgDict)
            if len(warnToPersonList)==0:
                log.info( 'û�и澯��Ϣ')
            else:
                sendToWarn(warnToPersonList)
            time.sleep(RECYCLE_TIMES)
        log.info('IS_START value=:'+IS_START+' so exit!')
        if needReloadProgram==False: h1.close()# ���needReloadProgram==True�Ļ�������reloadProgram()�йرճ���
        else:
            for i in range(4):
                print '�ȴ�5s,�����Խ���'
                time.sleep(5)#�ȴ�5s��,�ȴ�����������رա�
                if isAleadyReload==True:break

    except Exception:
        log.exception('ϵͳ����')
        h1.close()

