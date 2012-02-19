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
      读取ivrtrack.ini的配置文件信息
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
      写上次短信的记录到文件中.
    """
    try:
        lastmonitorFileSmContentFileObject=open(config_dir+'lastWebServerFileSmContent.log','wb+')
        lastmonitorFileSmContentFileObject.write(value)
        lastmonitorFileSmContentFileObject.close()
    except:
        log.exception('写短信发送内容到,%s文件中失败',config_dir+'lastWebServerFileSmContent.log')

def convertUnicodeToStr(unicodeMap):
    for key in unicodeMap.keys():
        if isinstance(unicodeMap[key],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
            unicodeMap[key]=unicodeMap[key].encode('GBK')
def checkSMGateBlock():
    """
     查询一下短信网关是否阻塞，如果阻塞，最通过满意度短信接口发送。
    """
    paramUtil=ParamUtil()
    log.info('短信阻塞监控')
    outputParam=paramUtil.invoke("Monitor_webserver_sm_block", MONITOR_NAME, URL)
    if outputParam.is_success():
        smBlockCount=outputParam.get_first_column_value()
        if int(smBlockCount)>200:
            smContent=MONITOR_NAME+':告警短信网关出现阻塞，目前已经阻塞了'+str(smBlockCount)+'短信'
            log.info('短信网关告警，发送短信到18959130026:%s',smContent)
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
     根据asServerList中的as server地址，调用判断服务是否调用成功.
     asServerObject：{'param':调用服务的参数,
                      'url':调用服务的地址,'monitor_name':机器名,
                      'about_system':相关系统
                      'seq':唯一流水号
                      'time_out':超时时长s为单位.}
    """
    warnStrList=[]
    log.info('******************** 开始URL调用 *****************************')
    for asServerObject in asServerList:
        warnStr=''
        timeOut=float(asServerObject['time_out'])
        socket.setdefaulttimeout(timeOut)
        startTimeSeconds=time.time()
        try:
            f=urllib2.urlopen(asServerObject['url'],asServerObject['param'])
            usedTimeSconds=round(time.time()-startTimeSeconds,2)
            if f.msg<>'OK':
                warnStr=asServerObject['monitor_name']+',URL地址报错:'+str(f.msg)
                log.info('[>%s<]服务器:%s,关联系统:%s,URL地址报错,用时:%ss',str(f.msg),asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
            else:
                asContentList=f.readlines()
                asContent=''.join(asContentList)
                asContent=asContent.strip()
                asServiceContentList=asContent.split(LinkConst.SPLIT_COLUMN)
                if len(asServiceContentList)>1:
                    resultCode=asServiceContentList[1]
                    if resultCode.strip()<>'0':
                        warnStr=asServerObject['monitor_name']+'关联系统:'+asServerObject['about_system']+'调用服务错误'
                        log.info('[>%s<]服务器:%s,关联系统:%s,调用服务错误,用时:%ss',str(resultCode),asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
                    else:
                        log.info('[>OK<]服务器:%s,关联系统:%s,用时:%ss',asServerObject['monitor_name'],asServerObject['about_system'],str(usedTimeSconds))
                else:
                    log.warn('URL:%s,param:%s,返回内容出现异常:%ss',asServerObject['url'],asServerObject['param'],asContent)

        except urllib2.URLError:
            warnStr='服务器:'+asServerObject['monitor_name']+',出现超时('+str(timeOut)+')s或者地址不存在'
            log.info('[>TimeOut<]服务器:%s,关联系统:%s,出现超时,超时时长:%ss',asServerObject['monitor_name'],asServerObject['about_system'],str(timeOut))
        if len(warnStr)>0:
            warnStrList.append(warnStr)
    return warnStrList

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
def get_version():
    version ='1.0'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  webserver_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.02.11')
    log.info('  使用方法:启动方法1.确认webserver_monitor.ini中的IS_START=1.启动 nohup ./webserver_monitor.py &  ')
    log.info('           关闭:修改webserver_monitor.ini中的IS_START参数更改为0.就会自动停止')
    log.info(' 功能点：监控应用服务器服务调用情况')
    log.info( '=========================================================================')
    return version


if __name__ == '__main__':
    lastSmsContent='' #怕短信一直重复发送，所以将上一条的短信内容存储在这里。
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
    lastmonitorFileSmContent='' #文件监控的短信告警
    try:
        while IS_START=='1':
            getCommonConfig()
            asServerList=[]
            readLastmonitorFileSmContent()
            asServerList=getWebServerByService()
##            asServerList.append({'seq':'11','monitor_name':'bbb','url':'http://134.128.51.148:9081/iserv/iserv/CallUrcp.jsp',
##            'param':'name=getRouteInfo&param=88203511100000591101001',
##            'about_system':'10000号群集','time_out':'2'})
##            asServerList.append({'seq':'12','monitor_name':'cc','url':'http://134.128.196.10:9081/iservuc/iserv/CallUrcp.jsp',
##            'param':'name=MGR_QueryStaffInfo&param=595300',
##            'about_system':'10000号群集','time_out':'2'})
            warnToPersonList=[]
            warnToPersonList=warnToPersonList+httpPostAsServer(asServerList)
            if len(warnToPersonList)>0:
                sendToWarn(warnToPersonList)
            checkSMGateBlock()
            time.sleep(RECYCLE_TIMES)
            if IS_START=='0':
                log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('系统报错')
    h1.close()
