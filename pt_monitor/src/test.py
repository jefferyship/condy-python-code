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
          采用ssh方式连接到服务器。
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
      自动重启本程序
    """
    global isAleadyReload
    isAleadyReload=False
    log.info( '程序最新版本更新完毕，自动重启程序')
    time.sleep(2)#等待2s中
##    for count in range(1,10):
##        log.info('新程序重启过程中,已等待%ds',count)
##        time.sleep(1)#等待10s中
    win32api.ShellExecute(0,'open',path,'','',1)#重启程序.
    isAleadyReload=True
    h1.close()
def tailFile(lineLen,tailFileObject):
    POS_BUF_SIZE=100*1024 #50k的位置大小.
    BUF_SIZE=100*1024 #50k的内容.
    try:
        filePos=-1 #行数所在的位置
        tailcurrLine=lineLen#从后面往前的目前行数的位置
        tailFileObject.seek(0,2)#到达文件的末尾
        itertimes=0 #最多做100个循环，防止进入死循环.
        while itertimes<10 and filePos<>0:
            itertimes=itertimes+1
            currPosition=tailFileObject.tell()
            log.debug('currPosition:'+str(currPosition))
            if (currPosition-BUF_SIZE)<0:#从文件头开始循环
                filePos=0
                tailFileObject.seek(0) #从头开始
            else:
                tailFileObject.seek(-BUF_SIZE,1)#相对移动到BUF_SIZE的位置
                currPosition=tailFileObject.tell()
                filePos=currPosition
            log.debug('filePos:'+str(filePos))
            strData=tailFileObject.read(BUF_SIZE)
            enterCount=strData.count('\n')
            log.debug('len(strDataList):'+str(enterCount))
            if (enterCount-tailcurrLine)>=0:#已经到了需要的行数
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
                tailcurrLine=tailcurrLine-enterCount #还没有到需要的行数，继续循环
                tailFileObject.seek(-len(strData),1)
        tailFileObject.seek(filePos)
        return True
    except Exception:
        log.exception('定位日志文件的位置报错')
        return False



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
或者为:
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
    #ctserver,websphere,不要获取版本
    if monitorList[0]['log_type'] in ['websphere','ctserver']:
        return
    nohupFilePath=os.path.split(monitorList[0]['monitorFile'])[0]
    nohupFilePath=nohupFilePath+'/../../bin'+os.sep+'nohup.out'
    if os.path.isfile(nohupFilePath)==False:
        log.info('从nohup中获取程序版本:找不到:%s文件',nohupFilePath)
        return
    commondStr='tail -4 '+nohupFilePath
    searchLogStd=os.popen(commondStr)
    lineLogList=searchLogStd.readlines()
    #没有值，或者不是**********开头的.
    if len(lineLogList)==0 or len(lineLogList)<>4 or lineLogList[0].find('**********')==-1 :
        return
    versionMsg=lineLogList[1].replace('*','').strip()+' '+lineLogList[2].replace('*','').strip()
    log.info('程序的版本号为:%s',versionMsg)


def writeZipFile():
    f = zipfile.ZipFile('filename.zip', 'w' ,zipfile.ZIP_DEFLATED)
    f.write('G:\python_code\pt_monitor\src\sendSM.py')
    f.close()
    


def getHardSpace():
    """
    获取文件系统的磁盘空间
    返回值:list对象。包含:tuple类型(文件系统,已用空间,可用空间,已用%,挂载点)。
  空间的单位是KB
     文件系统                                        1K-块        已用                          可用   已用% 挂载点
/dev/sda3            123887420  23195148  94297600  20% /
/dev/sda1              2030736     43240   1882676   3% /boot
tmpfs                  8202300         0   8202300   0% /dev/shm
    """
    hardSpaceStd=open('d:\\temp\\1.txt')
    hardSpaceList=[]
    lastHarsSpaceLine=''
    for hardSpaceLine in hardSpaceStd.readlines():
        hardSpaceLineList=hardSpaceLine.split()
       #按道理应该是对len(hardSpaceLineList)<6做判断，但有可能存在跨行的现象。len(hardSpaceLineList)<5的判断
        if len(hardSpaceLineList)<5 or hardSpaceLineList[0] in ['tmpfs','none']:
            lastHarsSpaceLine=hardSpaceLine
            continue
        #曾对这种跨行的字符做特殊处理
        #192.168.91.15:/data39
        #               1099538656 757823808 284960416  73% /data15guazai
        if len(lastHarsSpaceLine.split())==1 and len(hardSpaceLineList)==5:
            hardSpaceList.append((lastHarsSpaceLine.split()[0],hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3][:-1],hardSpaceLineList[4]))
        elif len(hardSpaceLineList)==6:#文件系统,总计大小,已用空间,可用空间,已用%,挂载点
            hardSpaceList.append((hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3],hardSpaceLineList[4][:-1],hardSpaceLineList[5]))
        lastHarsSpaceLine=hardSpaceLine
    if len(hardSpaceList)>0: #删除第一行是标题，不使用
        del hardSpaceList[0]
    return hardSpaceList


def monitorFile(monitorList):
    """
     监控日志文件.返回需要告警的日志表。
    """
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
        lineLen=int(monitorObject['tailRowNum'])
        tailFileObject=open(monitorObject['monitorFile'],'rb')
        if len(keyList)>0:
            if tailFile(lineLen,tailFileObject):
                for lineLog in tailFileObject.readlines():#是否有关键字内容
                    for key in keyList:
                        if re.search(key,lineLog):appearCountOfKeyMap[key]=appearCountOfKeyMap[key]+1
        for key in keyList:
            log.info( 'key:%s,realLimit:%d,warnLimit:%s'%(key,appearCountOfKeyMap[key],monitorObject['countMonitor']))
            if  appearCountOfKeyMap[key]>=int(monitorObject['countMonitor']):#到达告警条件，写告警内容
                warnStr=MONITOR_NAME+' 告警,日志文件:'+monitorObject['monitorFile']+' 关键字:'+key+' 出现次数:'+str(appearCountOfKeyMap[key])
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
##    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
##    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
##    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
##        thread.start_new_thread(reloadProgram,(sys.argv[0],))#tempPath需要修改成本程序的程序名.
##    for i in range(5):
##        print isAleadyReload
##        if isAleadyReload==True:break
##        print "3秒后,程序将结束..."
##        time.sleep(3)#等待5s中,等待程序重启后关闭。


