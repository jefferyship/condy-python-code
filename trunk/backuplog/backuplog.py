#!/usr/bin/env python
# -*- coding: GBK -*-
import ConfigParser
import os
import os.path
import glob
import time
import sys
import socket
from ftplib import FTP
from zipfile import ZipFile
def get_ip_address():
    """
     ��ȡIP��ַ
    """
    platform=sys.platform
    ip=''
    if platform.find('linux')!=-1:
        import fcntl
        import struct
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip=socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', 'eth0'[:15]))[20:24])
    else:
        ip=socket.gethostbyname(socket.gethostname())
    return ip

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc.encode('ascii','ignore')

def readFTPConfig():
    """
     ��ftp.xml�����ļ��ж�ȡ��������Ϣ.
    """
    from xml.dom import minidom
    xmldoc = minidom.parse(configFilePath+'ftp.xml')
    ftpMsg={}
    ftpDoc= xmldoc
    ftpMsg['ip']=getText(ftpDoc.getElementsByTagName('ip')[0].childNodes)
    ftpMsg['user']=getText(ftpDoc.getElementsByTagName('user')[0].childNodes)
    ftpMsg['password']=getText(ftpDoc.getElementsByTagName('password')[0].childNodes)
    ftpMsg['basepath']=getText(ftpDoc.getElementsByTagName('basepath')[0].childNodes)    
    return ftpMsg

def readLogPathConfig():
    """
     ��logPath.xml�����ļ��ж�ȡ��������Ϣ.
    """
    from xml.dom import minidom
    xmldoc = minidom.parse(configFilePath+'logPath.xml')
    logPathMsg={}
    logPathList= xmldoc.getElementsByTagName('LOG_PATH')
    for logPathDoc in logPathList:
        if logPathDoc.nodeType==logPathDoc.ELEMENT_NODE:
            logPathMsg[getText(logPathDoc.getElementsByTagName('name')[0].childNodes)]=getText(logPathDoc.getElementsByTagName('value')[0].childNodes)
    return logPathMsg

def getDateStr(t,month=0,day=0):
    return str(t.tm_year)+str(t.tm_mon+month).zfill(2)+str(t.tm_mday+day).zfill(2)

def compressFile():
    """
        �����õ���־Ŀ¼����ѹ����ֻѹ��ǰһ�����־
        """
    logPathDict=readLogPathConfig()
    zipFileNamedict={}
    currTime=time.localtime()
    yestodayStr=getDateStr(currTime,day=-1) #ȡ�����ʱ��
    testTime=time.strptime(getDateStr(time.localtime(),day=-1),'%Y%m%d')
    for key in logPathDict.keys():
        print 'log name=%s and logpath=%s'%(key,logPathDict[key])
        fileList=os.listdir(logPathDict[key])
        #zipFileName=logPathDict[key]+os.sep+key+'_'+yestodayStr+'.zip'
        #zipFileNamelist.append((key,zipFileName))
        
        for filename in fileList:#ֻȡ������ʱ�����������־�ļ�����ѹ��.
            fileTime=time.localtime(os.stat(logPathDict[key]+os.sep+filename).st_mtime)
            fileTimeStr=getDateStr(fileTime)
            if yestodayStr==fileTimeStr:
                print 'backuplog:'+logPathDict[key]+os.sep+filename
                zipFileName=logPathDict[key]+os.sep+key+'_'+yestodayStr+time.strftime('%H',fileTime)+'.zip'
                if zipFileName not in zipFileNamedict:
                    zipFileNamedict[zipFileName]=(key,zipFileName)
                    zipFile=ZipFile(zipFileName,'w')
                    print 'create zipfile:%s'%(zipFileName)
                else:
                    zipFile=ZipFile(zipFileName,'a')
                
                try:
                    zipFile.write(logPathDict[key]+os.sep+filename)
                    zipFile.close()
                except Exception:
                    pass
            
        
    return zipFileNamedict.values()

def uploadarchiveFile(zipfileNameList):
    ftpConfigMsg=readFTPConfig()
    ftp=FTP(ftpConfigMsg['ip'],ftpConfigMsg['user'],ftpConfigMsg['password'])
    yestoday=time.strptime(getDateStr(time.localtime(),day=-1),'%Y%m%d')
    #����Ŀ¼�����Ŀ¼���������Զ��½�Ŀ¼.
    for zipFileNameTuple in zipfileNameList:
        ftpLogPath=ftpConfigMsg['basepath']
        ftpLogPathList=[ftpLogPath]
        ftpLogPath=ftpLogPath+'/'+get_ip_address()
        ftpLogPathList.append(ftpLogPath)
        ftpLogPath=ftpLogPath+'/'+zipFileNameTuple[0]
        ftpLogPathList.append(ftpLogPath)
        ftpLogPath=ftpLogPath+'/'+time.strftime('%Y',yestoday)
        ftpLogPathList.append(ftpLogPath)
        ftpLogPath=ftpLogPath+'/'+time.strftime('%m',yestoday)
        ftpLogPathList.append(ftpLogPath)
        ftpLogPath=ftpLogPath+'/'+time.strftime('%d',yestoday)
        ftpLogPathList.append(ftpLogPath)
        
        for ftpLogPath in ftpLogPathList:
            try:
                #print 'trying change directory '+ftpLogPath
                ftp.cwd(ftpLogPath)
            except Exception:
                print 'creating direcotry '+ ftp.mkd(ftpLogPath)
                ftp.cwd(ftpLogPath)
        try:
            zipFileObject=open(zipFileNameTuple[1])
            print 'upload file '+zipFileNameTuple[1]
            ftp.storbinary('STOR '+os.path.split(zipFileNameTuple[1])[1],zipFileObject)
            zipFileObject.close()
            os.remove(zipFileNameTuple[1])
        except Exception:
            raise 

def deleteExpireBacklog():
    
               
def checkPythonVersion():
    python_version=sys.version[:3]
    is_python=0
    if python_version<'2.5':
        print '========================================================================='
        print ' must run python version at least 2.5. current version is %s             '%(sys.version)
        print '========================================================================='
        is_python=0
    else:
        print '========================================================================='
        print '  current version is %s               '%(sys.version)
        print '========================================================================='
        is_pyhon=1
    return is_pyhon

configFilePath=os.getcwd()+os.sep
if len(sys.argv)==1 :
    tempPath=os.path.split(sys.argv[0])
    if tempPath[0]!='':
        configFilePath=tempPath[0]+os.sep

zipFileNameList=compressFile()
uploadarchiveFile(zipFileNameList)

        
#zipFileNameList=compressFile()
#print zipFileNameList[0][0]
#uploadarchiveFile(zipFileNameList)
#ftp=FTP(ftpConfigMsg['ip'],ftpConfigMsg['user'],ftpConfigMsg['passwor
