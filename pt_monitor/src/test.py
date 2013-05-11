#!/usr/bin/env python
# -*- coding: GBK -*-
import urllib2
import urllib
import logging
import logging.handlers
import os
import os.path
import sys
import shutil
import thread
import time
import re
import paramiko
import zipfile 

def connectCTIssh(host):
        """
          ����ssh��ʽ���ӵ���������
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print 'host'+host['ip'];
        client.connect(host['ip'], 22, username=host['user'], password=host['password'], timeout=4)
        stdoutStrList=[]
        tempStr='-1'
        stdout=None
        stderr=None
        commands=';'.join(host['commands'])
        print 'aaa:'+commands
        stdin, stdout, stderr =client.exec_command(commands)
        print stdout.readlines()
        print 'cccc'
        print stderr.readlines()
        client.close()
##        commandChanel = client.invoke_shell()
##        commandChanel.setblocking(0)
##        commandChanel.send(commands)
##        while commandChanel.recv_ready():
##            print commandChanel.recv(2048)
##        for st in stdout.readlines():
##            print st
##        commandChanel = client.invoke_shell()
##        for command in host['commands']:
##          print 'aaa'+command
##          commandChanel.send(command+'\n')
##          commandChanel.recv_exit_status()
##          while commandChanel.recv_ready():
##            strTemp=commandChanel.recv(2048)
##            print 'cccc:'+strTemp

        ctiStr=''.join(stdoutStrList)
        client.close()
        return ctiStr
def reloadProgram(path):
    """
      �Զ�����������
    """
    global isAleadyReload
    isAleadyReload=False
    log.info( '�������°汾������ϣ��Զ���������')
    time.sleep(2)#�ȴ�2s��
##    for count in range(1,10):
##        log.info('�³�������������,�ѵȴ�%ds',count)
##        time.sleep(1)#�ȴ�10s��
    win32api.ShellExecute(0,'open',path,'','',1)#��������.
    isAleadyReload=True
    h1.close()
def tailFile(lineLen,tailFileObject):
    POS_BUF_SIZE=100*1024 #50k��λ�ô�С.
    BUF_SIZE=100*1024 #50k������.
    try:
        filePos=-1 #�������ڵ�λ��
        tailcurrLine=lineLen#�Ӻ�����ǰ��Ŀǰ������λ��
        tailFileObject.seek(0,2)#�����ļ���ĩβ
        itertimes=0 #�����100��ѭ������ֹ������ѭ��.
        while itertimes<10 and filePos<>0:
            itertimes=itertimes+1
            currPosition=tailFileObject.tell()
            log.debug('currPosition:'+str(currPosition))
            if (currPosition-BUF_SIZE)<0:#���ļ�ͷ��ʼѭ��
                filePos=0
                tailFileObject.seek(0) #��ͷ��ʼ
            else:
                tailFileObject.seek(-BUF_SIZE,1)#����ƶ���BUF_SIZE��λ��
                currPosition=tailFileObject.tell()
                filePos=currPosition
            log.debug('filePos:'+str(filePos))
            strData=tailFileObject.read(BUF_SIZE)
            enterCount=strData.count('\n')
            log.debug('len(strDataList):'+str(enterCount))
            if (enterCount-tailcurrLine)>=0:#�Ѿ�������Ҫ������
                matchCount=enterCount-tailcurrLine
                findposition=len(strData)
                log.debug('len(strData):'+str(findposition))
                for i in range(tailcurrLine):
                    findTempPosition=strData.rfind('\n',0,findposition)
                    log.debug('findTempPosition:'+str(findTempPosition))
                    if findTempPosition==-1: break
                    else:findposition=findTempPosition

    ##            tempList=strDataList[0:-tailcurrLine]
    ##            print ';'.join(tempList)
    ##            tempStr='\r\n'.join(tempList)
                filePos=filePos+findposition
                log.debug('filePos:'+str(filePos))
                break
            else:
                tailcurrLine=tailcurrLine-enterCount #��û�е���Ҫ������������ѭ��
                tailFileObject.seek(-len(strData),1)
        tailFileObject.seek(filePos)
        return True
    except Exception:
        log.exception('��λ��־�ļ���λ�ñ���')
        return False



def getNohupVersion(monitorList):
    """
     ��д��nohup.out�ļ��г���İ汾����ȡ����д�����ݿ��С�nohup.out�е��ļ���ʽһ��Ϊ:
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
����Ϊ:
******************************************************
*       RESMGR FOR NMS  1.2 (no for tts and asr)     *
*       RESMGR_LIB      Version=1.0                  *
******************************************************
******************************************************
*       RESMGR FOR NMS  1.2 (no for tts and asr)     *
*       RESMGR_LIB      Version=1.0                  *
******************************************************
******************************************************
*       RESMGR FOR NMS  1.2 (no for tts and asr)     *
*       RESMGR_LIB      Version=1.0                  *
******************************************************
******************************************************
*       RESMGR FOR NMS  1.2 (no for tts and asr)     *
*       RESMGR_LIB      Version=1.0                  *
******************************************************
    """
    if len(monitorList)==0:
        return
    #ctserver,websphere,��Ҫ��ȡ�汾
    if monitorList[0]['log_type'] in ['websphere','ctserver']:
        return
    nohupFilePath=os.path.split(monitorList[0]['monitorFile'])[0]
    nohupFilePath=nohupFilePath+'/../../bin'+os.sep+'nohup.out'
    if os.path.isfile(nohupFilePath)==False:
        log.info('��nohup�л�ȡ����汾:�Ҳ���:%s�ļ�',nohupFilePath)
        return
    commondStr='tail -4 '+nohupFilePath
    searchLogStd=os.popen(commondStr)
    lineLogList=searchLogStd.readlines()
    #û��ֵ�����߲���**********��ͷ��.
    if len(lineLogList)==0 or len(lineLogList)<>4 or lineLogList[0].find('**********')==-1 :
        return
    versionMsg=lineLogList[1].replace('*','').strip()+' '+lineLogList[2].replace('*','').strip()
    log.info('����İ汾��Ϊ:%s',versionMsg)


def writeZipFile():
    f = zipfile.ZipFile('filename.zip', 'w' ,zipfile.ZIP_DEFLATED)
    f.write('G:\python_code\pt_monitor\src\sendSM.py')
    f.close()
    


def getHardSpace():
    """
    ��ȡ�ļ�ϵͳ�Ĵ��̿ռ�
    ����ֵ:list���󡣰���:tuple����(�ļ�ϵͳ,���ÿռ�,���ÿռ�,����%,���ص�)��
  �ռ�ĵ�λ��KB
     �ļ�ϵͳ                                        1K-��        ����                          ����   ����% ���ص�
/dev/sda3            123887420  23195148  94297600  20% /
/dev/sda1              2030736     43240   1882676   3% /boot
tmpfs                  8202300         0   8202300   0% /dev/shm
    """
    hardSpaceStd=open('d:\\temp\\1.txt')
    hardSpaceList=[]
    lastHarsSpaceLine=''
    for hardSpaceLine in hardSpaceStd.readlines():
        hardSpaceLineList=hardSpaceLine.split()
       #������Ӧ���Ƕ�len(hardSpaceLineList)<6���жϣ����п��ܴ��ڿ��е�����len(hardSpaceLineList)<5���ж�
        if len(hardSpaceLineList)<5 or hardSpaceLineList[0] in ['tmpfs','none']:
            lastHarsSpaceLine=hardSpaceLine
            continue
        #�������ֿ��е��ַ������⴦��
        #192.168.91.15:/data39
        #               1099538656 757823808 284960416  73% /data15guazai
        if len(lastHarsSpaceLine.split())==1 and len(hardSpaceLineList)==5:
            hardSpaceList.append((lastHarsSpaceLine.split()[0],hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3][:-1],hardSpaceLineList[4]))
        elif len(hardSpaceLineList)==6:#�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�
            hardSpaceList.append((hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3],hardSpaceLineList[4][:-1],hardSpaceLineList[5]))
        lastHarsSpaceLine=hardSpaceLine
    if len(hardSpaceList)>0: #ɾ����һ���Ǳ��⣬��ʹ��
        del hardSpaceList[0]
    return hardSpaceList


def monitorFile(monitorList):
    """
     �����־�ļ�.������Ҫ�澯����־��
    """
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
        lineLen=int(monitorObject['tailRowNum'])
        tailFileObject=open(monitorObject['monitorFile'],'rb')
        if len(keyList)>0:
            if tailFile(lineLen,tailFileObject):
                for lineLog in tailFileObject.readlines():#�Ƿ��йؼ�������
                    for key in keyList:
                        if re.search(key,lineLog):appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
        for key in keyList:
            log.info( 'key:%s,realLimit:%d,warnLimit:%s'%(key,appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if  appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#����澯������д�澯����
                warnStr=MONITOR_NAME+' �澯,��־�ļ�:'+monitorObject['monitorFile']+' �ؼ���:'+key+' ���ִ���:'+str(appearCountOfKeyMap[key])
                lastmonitorFileSmContent=warnStr
                log.info(warnStr)
                warnToPersonList.append(warnStr)
        tailFileObject.close()
    return warnToPersonList
if __name__ == '__main__':
     host={}
     host['ip']='134.128.196.10'
     host['user']='websphere'
     host['password']='0590tnstns'
     host['connecttype']='ssh'
     host['log_time']='201204191810'
     host['commands']=['cd /home/websphere/LOG/ctserver/','grep '+'13328845588 '+'ctserver'+'04191810'+'.log']
     writeZipFile()
    # host['commands']=['cd /home/websphere/LOG/'+'ctserver','pwd']
     #print connectCTIssh(host)
##    a='condy hardspaceWarning:hardspace_name:d:\ limit_used_percent:40 real_used_percent:75.5\r\ncondy hardspaceWarning:hardspace_name:e:\ limit_used_percent:20 real_used_percent:76.9'
##    import ConfigParser
##    config=ConfigParser.ConfigParser()
##    ivrtrackFileObject=open('monitorForWindow.ini')
##    config.readfp(ivrtrackFileObject)
##    b=config.get('common', 'lastmonitorFileSmContent')
##    print a
##    print b
##    print a==b
##    print sys.argv[0]
##    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
##    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
##    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
##        config_dir=os.getcwd()+os.sep
##    else:
##        config_dir=tempPath[0]+os.sep
##    log = logging.getLogger()
##    log.setLevel(logging.DEBUG)
##    h1 = logging.handlers.RotatingFileHandler(config_dir+'test.log',maxBytes=2097152,backupCount=5)
##    h1.setLevel(logging.INFO)
##    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
##    h1.setFormatter(f)
##    log.addHandler(h1)
##    monitorFileList=[{'tailRowNum':2000,'monitorFile':'C:\\Ecc10000\\log\\App20111202.log','countMonitor':40,'keys':'IMRIOpenImr()'}]
##
##    warnToPersonList=monitorFile(monitorFileList)
##    print warnToPersonList
##    h1.close()

##
##    global isAleadyReload
##    isAleadyReload=False
##    answer = raw_input("Do you want to restart this program ? ")
##    if answer.strip() in "y Y yes Yes YES".split():
##        thread.start_new_thread(reloadProgram,(sys.argv[0],))#tempPath��Ҫ�޸ĳɱ�����ĳ�����.
##    for i in range(5):
##        print isAleadyReload
##        if isAleadyReload==True:break
##        print "3���,���򽫽���..."
##        time.sleep(3)#�ȴ�5s��,�ȴ�����������رա�


