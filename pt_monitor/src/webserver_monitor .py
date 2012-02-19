#!/usr/bin/env python
# -*- coding: GBK -*-
import sys
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import urllib
import urllib2
import time
import os
import ConfigParser
import logging
import logging.handlers
import datetime
import random
import  socket
def getCommonConfig():
    """
      ��ȡivrtrack.ini�������ļ���Ϣ
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global MONITOR_NAME
    global IS_START
    global RECYCLE_TIMES
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'webserver_monitor.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def readLastmonitorFileSmContent():
    global lastmonitorFileSmContent
    try:
        lastmonitorFileSmContentFileObject=open(config_dir+'lastWebServerFileSmContent.log','rb+')
        lastmonitorFileSmContent=lastmonitorFileSmContentFileObject.read(2048)
        lastmonitorFileSmContentFileObject.close()
    except:
        lastmonitorFileSmContent=''

def writeLastmonitorFileSmContent(value):
    """
      д�ϴζ��ŵļ�¼���ļ���.
    """
    try:
        lastmonitorFileSmContentFileObject=open(config_dir+'lastWebServerFileSmContent.log','wb+')
        lastmonitorFileSmContentFileObject.write(value)
        lastmonitorFileSmContentFileObject.close()
    except:
        log.exception('д���ŷ������ݵ�,%s�ļ���ʧ��',config_dir+'lastWebServerFileSmContent.log')

def convertUnicodeToStr(unicodeMap):
    for key in unicodeMap.keys():
        if isinstance(unicodeMap[key],unicode):#�������Ĺؼ��֣�Ҫ��unicode����ת��Ϊstr����.
            unicodeMap[key]=unicodeMap[key].encode('GBK')
def checkSMGateBlock():
    """
     ��ѯһ�¶��������Ƿ������������������ͨ������ȶ��Žӿڷ��͡�
    """
    paramUtil=ParamUtil()
    log.info('�����������')
    outputParam=paramUtil.invoke("Monitor_webserver_sm_block", MONITOR_NAME, URL)
    if outputParam.is_success():
        smBlockCount=outputParam.get_first_column_value()
        if int(smBlockCount)>200:
            smContent=MONITOR_NAME+':�澯�������س���������Ŀǰ�Ѿ�������'+str(smBlockCount)+'����'
            log.info('�������ظ澯�����Ͷ��ŵ�18959130026:%s',smContent)
            serailNo=MONITOR_NAME+'_'+str(random.randint(1,100))+str(time.time())
            outputParam=paramUtil.invoke("SendZongHengWebService",
             '18959130026'+LinkConst.SPLIT_COLUMN+'3'+LinkConst.SPLIT_COLUMN+smContent+LinkConst.SPLIT_COLUMN+serailNo, URL)

def getWebServerByService():
    asServerList=[]
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("Monitor_webserver_config", MONITOR_NAME, URL)
    if outputParam.is_success():
        table=outputParam.get_tables().get_first_table()
        for rowObject in table.get_row_list():
            asServerObjectMap={}
            asServerObjectMap['seq']=rowObject.get_one_column(0).get_value()
            asServerObjectMap['monitor_name']=rowObject.get_one_column(1).get_value()
            asServerObjectMap['url']=rowObject.get_one_column(2).get_value()
            asServerObjectMap['param']=rowObject.get_one_column(3).get_value().replace('#',LinkConst.SPLIT_COLUMN)
            asServerObjectMap['about_system']=rowObject.get_one_column(4).get_value()
            asServerObjectMap['time_out']=rowObject.get_one_column(5).get_value()
            convertUnicodeToStr(asServerObjectMap)
            asServerList.append(asServerObjectMap)
    return asServerList



def httpPostAsServer(asServerList):
    """
     ����asServerList�е�as server��ַ�������жϷ����Ƿ���óɹ�.
     asServerObject��{'param':���÷���Ĳ���,
                      'url':���÷���ĵ�ַ,'monitor_name':������,
                      'about_system':���ϵͳ
                      'seq':Ψһ��ˮ��
                      'time_out':��ʱʱ��sΪ��λ.}
    """
    warnStrList=[]
    log.info('******************** ��ʼURL���� *****************************')
    for asServerObject in asServerList:
        warnStr=''
        timeOut=float(asServerObject['time_out'])
        socket.setdefaulttimeout(timeOut)
        startTimeSeconds=time.time()
        try:
            f=urllib2.urlopen(asServerObject['url'],asServerObject['param'])
            usedTimeSconds=round(time.time()-startTimeSeconds,2)
            if f.msg<>'OK':
                warnStr=asServerObject['monitor_name']+',URL��ַ����:'+str(f.msg)
                log.info('[>%s<]������:%s,����ϵͳ:%s,URL��ַ����,��ʱ:%ss',str(f.msg),asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
            else:
                asContentList=f.readlines()
                asContent=''.join(asContentList)
                asContent=asContent.strip()
                asServiceContentList=asContent.split(LinkConst.SPLIT_COLUMN)
                if len(asServiceContentList)>1:
                    resultCode=asServiceContentList[1]
                    if resultCode.strip()<>'0':
                        warnStr=asServerObject['monitor_name']+'����ϵͳ:'+asServerObject['about_system']+'���÷������'
                        log.info('[>%s<]������:%s,����ϵͳ:%s,���÷������,��ʱ:%ss',str(resultCode),asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
                    else:
                        log.info('[>OK<]������:%s,����ϵͳ:%s,��ʱ:%ss',asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
                else:
                    log.warn('URL:%s,param:%s,�������ݳ����쳣:%ss',asServerObject['url'],asServerObject['param'],asContent)

        except urllib2.URLError:
            warnStr='������:'+asServerObject['monitor_name']+',���ֳ�ʱ('+str(timeOut)+')s���ߵ�ַ������'
            log.info('[>TimeOut<]������:%s,����ϵͳ:%s,���ֳ�ʱ,��ʱʱ��:%ss',asServerObject['monitor_name'],asServerObject['about_system'],str(timeOut))
        if len(warnStr)>0:
            warnStrList.append(warnStr)
    return warnStrList

def sendToWarn(warnToPersonList):
    """
    ���͸澯��Ϣ����Ӧ����ϵ��Ա
    """
    global lastmonitorFileSmContent
    paramUtil=ParamUtil()
    inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
    currmonitorFileSmContent='.'.join(warnToPersonList)
    if lastmonitorFileSmContent==currmonitorFileSmContent:
        log.info('�ظ��澯���Ų�����:%s',currmonitorFileSmContent)
        return True;

    outputParam=paramUtil.invoke("Monitor_machine_info", MONITOR_NAME, URL)
    planId=''
    if outputParam.is_success() and outputParam.get_tables().get_first_table().has_row():
       planId=outputParam.get_column_value(0,0,4)
    else:
        log.error('����Monitor_machine_infoʧ�ܣ�������%s������û����monitor_pt_machine_name��������',MONITOR_NAME)
        return False
    flag=''
    if planId!='':#����10000�ź������ͨ�õķ���������Է����ʼ���
        inputStr=planId.encode('GBK')+LinkConst.SPLIT_COLUMN+'A'+LinkConst.SPLIT_COLUMN+'\r\n'.join(warnToPersonList)
        log.info('���Ͷ���:���÷���WarnToPerson,�������:%s',inputStr)
        outputParam=paramUtil.invoke("WarnToPerson", inputStr, URL)
    else:
        inputStr=MONITOR_NAME+LinkConst.SPLIT_COLUMN
        inputStr=inputStr+'\r\n'.join(warnToPersonList)
        log.info('���Ͷ���:���÷���Monitor_Warn_To_Person,�������:%s',inputStr)
        outputParam=paramUtil.invoke("Monitor_Warn_To_Person", inputStr, URL)
    if outputParam.is_success() :
        flag=outputParam.get_first_column_value()
    writeLastmonitorFileSmContent(currmonitorFileSmContent)
    return flag=='0'
def get_version():
    version ='1.0'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  webserver_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.02.11')
    log.info('  ʹ�÷���:��������1.ȷ��webserver_monitor.ini�е�IS_START=1.���� nohup ./webserver_monitor.py &  ')
    log.info('           �ر�:�޸�webserver_monitor.ini�е�IS_START��������Ϊ0.�ͻ��Զ�ֹͣ')
    log.info(' ���ܵ㣺���Ӧ�÷���������������')
    log.info( '=========================================================================')
    return version


if __name__ == '__main__':
    lastSmsContent='' #�¶���һֱ�ظ����ͣ����Խ���һ���Ķ������ݴ洢�����
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    alarmObjectMap={}
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'webserver_monitor.log',maxBytes=2097152,backupCount=5)
    #h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    lastmonitorFileSmContent='' #�ļ���صĶ��Ÿ澯
    try:
        while IS_START=='1':
            getCommonConfig()
            asServerList=[]
            readLastmonitorFileSmContent()
            asServerList=getWebServerByService()
##            asServerList.append({'seq':'11','monitor_name':'bbb','url':'http://134.128.51.148:9081/iserv/iserv/CallUrcp.jsp',
##            'param':'name=getRouteInfo&param=88203511100000591101001',
##            'about_system':'10000��Ⱥ��','time_out':'2'})
##            asServerList.append({'seq':'12','monitor_name':'cc','url':'http://134.128.196.10:9081/iservuc/iserv/CallUrcp.jsp',
##            'param':'name=MGR_QueryStaffInfo&param=595300',
##            'about_system':'10000��Ⱥ��','time_out':'2'})
            warnToPersonList=[]
            warnToPersonList=warnToPersonList+httpPostAsServer(asServerList)
            if len(warnToPersonList)>0:
                sendToWarn(warnToPersonList)
            checkSMGateBlock()
            time.sleep(RECYCLE_TIMES)
            if IS_START=='0':
                log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('ϵͳ����')
    h1.close()
