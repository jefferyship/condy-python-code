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

def getCommonConfig():
    """
      ��ȡivrtrack.ini�������ļ���Ϣ
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


def get_version():
    version ='1.1.0.0'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  monitorForWindow.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.08.12 modify time:2011.08.05')
    log.info(' ���ܵ�1.���windows�Ĵ��̿ռ�')
    paramUtil=ParamUtil()
    versionMsg={}
    outputParam=paramUtil.invoke("MGR_GetEccCodeDict", '-1'+LinkConst.SPLIT_COLUMN+'monitorForWindow'+LinkConst.SPLIT_COLUMN+'PATCH', URL)
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
def monitorDisk(monitorDiskObjectList,saveDbMsgDict):
    """
    windows �汾�Ĵ��̿ռ���,monitorDiskOjectList [{'hardspace_name':hardspace_name,'hardspace_limit':hardspace_limit}]
    """
    warnToPersonList=[]
    saveToDBList=[]#[(�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�)]
    saveDbMsgDict['hardSpace']=saveToDBList
    for monitorDiskObject in monitorDiskObjectList:
        try:
            total,used,free,usedPecent=SystemInfo.getdiskByPath(monitorDiskObject['hardspace_name'])
            saveToDBList.append((monitorDiskObject['hardspace_name'],total/1024,used/1024,free/1024,usedPecent,''))
            limitPercent=float(monitorDiskObject['hardspace_limit'])
            if usedPecent>=limitPercent:
                log.info("���̿ռ�澯: hardspace_name:%s,limit_used_percent:%s,real_used_percent:%s",monitorDiskObject['hardspace_name'],monitorDiskObject['hardspace_limit'],str(round(usedPecent,2)))
                warnStr=MONITOR_NAME+' ���̿ռ�澯:hardspace_name:'+monitorDiskObject['hardspace_name']+' limit_used_percent:'+monitorDiskObject['hardspace_limit']+' real_used_percent:'+str(round(usedPecent,2))
                warnToPersonList.append(warnStr)
        except Exception:
            log.exception('��ȡ���̿ռ䱨������Ϊ:'+monitorDiskObject['hardspace_name'])

    return warnToPersonList




if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
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
        log.exception('ϵͳ����')

