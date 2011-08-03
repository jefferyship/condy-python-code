#!/usr/bin/env python
# -*- coding: GBK -*-
import sys
import telnetlib
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import time
import os
import ConfigParser
import re
import logging
import logging.handlers
import datetime
class AlarmObject:
    """
    告警对象
    """
    def __init__(self,seq_value=None,alarm_time=None,alarm_level=None,log_type=None,type_id=None,alarm_title=None):
        self.__itemMap={}
        self.set_seq(seq_value)
        self.set_time(alarm_time)
        self.set_level(alarm_level)
        self.set_log_type(log_type)
        self.set_type_id(type_id)
        self.set_title(alarm_title)

    def get_seq(self):
        return self.__seq
    def get_title(self):
        return self.__title
    def set_title(self,alarm_title):
        self.__title=alarm_title
    def set_seq(self,seq_value):
        self.__seq=seq_value
    def get_time(self):
        return self.__time
    def set_time(self,alarm_time):
        if alarm_time<>None and alarm_time<>'':
            tempTime=time.strptime(alarm_time,'%Y-%m-%d %H:%M:%S')
            self.__time=datetime.datetime(tempTime.tm_year,tempTime.tm_mon,tempTime.tm_mday,tempTime.tm_hour,tempTime.tm_min,tempTime.tm_sec)
        else:self.__time=None
    def get_time_str(self):
        if self.__time<>None:
            return self.__time.strftime('%Y-%m-%d %H:%M:%S')
        else: return ''
    def get_level(self):
        return self.__level
    def set_level(self,alarm_level):
        self.__level=alarm_level
    def set_log_type(self,log_type):
        self.__log_type=log_type
    def get_log_type(self):
        return self.__log_type
    def get_type_id(self):
        return self.__type_id
    def set_type_id(self,type_id):
        self.__type_id=type_id
    def add_item(self,item_name,item_value):
        self.__itemMap[item_name]=item_value
    def get_item(self,item_name):
        try:
            return self.__itemMap[item_name]
        except KeyError:
            return None
    def generateDetailLogUrcp(self,rowList):
        for key in self.__itemMap.keys():
            columnList=[]
            columnList.append(self.__seq)
            columnList.append(key)
            columnList.append(self.__itemMap[key])
            rowList.append(str(LinkConst.SPLIT_COLUMN).join(columnList))

    def generateLogUrcp(self,host_name,rowList):
        columnList=[]
        columnList.append(self.__seq)
        columnList.append(self.get_time_str())
        columnList.append(self.__type_id)
        columnList.append(self.__level)
        columnList.append(self.__log_type)
        columnList.append(host_name)
        if self.__log_type=='2':
            columnList.append(self.get_time_str())
        else:
            columnList.append('')
        columnList.append('')#备注.
        rowList.append(str(LinkConst.SPLIT_COLUMN).join(columnList))

def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global MONITOR_NAME
    global TELNET_IP
    global TELNET_PORT
    global IS_START
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'zx_monitor.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    TELNET_IP=config.get('common', 'TELNET_IP')
    TELNET_PORT=config.get('common', 'TELNET_PORT')
    IS_START=config.get('common', 'IS_START')
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

def convertUnicodeToStr(unicodeMap):
    for key in unicodeMap.keys():
        if isinstance(unicodeMap[key],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
            unicodeMap[key]=unicodeMap[key].encode('GBK')
def getAlaramConfigByService():
    global alarmConfig
    alarmConfig={}
    paramUtil=ParamUtil()
    outputParam=paramUtil.invoke("monitor_zx_getAlarmType", MONITOR_NAME, URL)
    if outputParam.is_success():
        table=outputParam.get_tables().get_first_table()
        for rowObject in table.get_row_list():
            alarmConfigObjectMap={}
            alarmConfigObjectMap['alarm_type_id']=rowObject.get_one_column(0).get_value()
            alarmConfigObjectMap['alarm_name']=rowObject.get_one_column(1).get_value()
            alarmConfigObjectMap['alarm_level']=rowObject.get_one_column(2).get_value()
            convertUnicodeToStr(alarmConfigObjectMap)
            #0是通知级别，但最严重的级别确实1，所以将0级别更改为5,有利于程序判断。
            if alarmConfigObjectMap['alarm_level']=='0':alarmConfigObjectMap['alarm_level']=5
            alarmConfig[alarmConfigObjectMap['alarm_type_id']]=alarmConfigObjectMap
        log.info(alarmConfig)
        return True
    else:
        return False


def parseAlarmRecoverData(alarmDataList):
    """
      告警恢复的串解析
START
2 591
2047650
2011-03-22 18:53:46
almpcm
IP = 134.132.34.3
mnode = 2
END
    """
    try:
        sOffinum=alarmDataList[1][1:].strip()#2 591
        sSerialno=alarmDataList[2].strip()#2047650
        sRestoreTime=alarmDataList[3].strip()#2011-03-22 18:53:46
        sAlarmType=alarmDataList[4].strip()#almpcm
        alarmObject=AlarmObject(sSerialno,sRestoreTime,'','2',sAlarmType)
        itemObjectList=alarmDataList[5:-1]#从第5位开始，去除最后的END标志.
        for itemObject in itemObjectList:#IP = 134.132.34.3,mnode = 2
        	try:
	           alarmObject.add_item(itemObject.split('=')[0].strip(),itemObject.split('=')[1].strip())
        	except IndexError:
        		log.warn('这个数据串解析异常:'+itemObject)
        return alarmObject
    except IndexError:
        log.warn('这个数据串解析异常:'+str(alarmDataList))
    return None

    #print 'ccc:'+alarmObject.generateUrcp()

def parseAlarmData(alarmDataList):
    """
      告警串解析
    """
    #print alarmDataList
    try:
        sOffinum=alarmDataList[1][1:].strip()#2 591 局号
        sSerialno=alarmDataList[2].split()[0]#2047650 告警流水号
        sALarmLevel='3'#默认显示3级别
        if len(alarmDataList[2].split())>1:
            sALarmLevel=alarmDataList[2].split()[1]# 1)严重, 2)重要, 3)普通, 4):轻微。0):通知消息(没有恢复) 告警级别
        sRestoreTime=alarmDataList[3].strip()#2011-03-22 18:53:46
        sAlarmType=alarmDataList[4].split()[0]#almpcm  告警类型
        sAlarmTitle=alarmDataList[4].split()[1]#  告警标题
        alarmObject=AlarmObject(sSerialno,sRestoreTime,sALarmLevel,'1',sAlarmType,sAlarmTitle)
        itemObjectList=alarmDataList[5:-1]#从第5位开始，去除最后的END标志.
        for itemObject in itemObjectList:#IP = 134.132.34.3,mnode = 2
        	try:
	           alarmObject.add_item(itemObject.split('=')[0].strip(),itemObject.split('=')[1].strip())
        	except IndexError:
        		log.warn('这个数据串解析异常:'+itemObject)
        return alarmObject
    except IndexError:
        log.warn('这个数据串解析异常:'+str(alarmDataList))
    return None
    #print 'ddd:'+alarmObject.generateUrcp()
def parseReadData(Str):
    """
      解析tims协议.
      字符串内容:'START\r\n2 591     \r\n2047650  \r\n2011-03-22 18:53:46\r\nalmpcm     \r\nIP = 134.132.34.3\r\nmnode = 2\r\nEND
    """
    dataList=re.findall('(START.+?END)',Str,re.S)
    alaramObjectList=[]
    for data in dataList:
        alarmDataList=data.splitlines()
        if alarmDataList[1].startswith('1'):#告警
            alaramObject=parseAlarmData(alarmDataList)
        elif alarmDataList[1].startswith('2'):#恢复告警
            alaramObject=parseAlarmRecoverData(alarmDataList)
        if alaramObject<>None:
            alaramObjectList.append(alaramObject)
    return alaramObjectList

def alarmToPerson(alaramObjectList):
    alarmToPersonList=[]
    paramUtil=ParamUtil()
    sFiveMiniBefore=datetime.datetime.now()-datetime.timedelta(minutes=5)
    for alarmObject in alaramObjectList:
        #5分钟之前的告警，就不发短信.

        if alarmObject.get_time()==None or alarmObject.get_time()<sFiveMiniBefore: continue
        try:
            currLevel=alarmObject.get_level()
            if currLevel=='0':currLevel='5'
            alaramConfigMap=alarmConfig[alarmObject.get_type_id()]
            if alarmObject.get_log_type()=='1':#告警类型
                if int(currLevel)<=alaramConfigMap['alarm_level']:
                    if alarmObject.get_type_id()=='almpcm' :
                        pcmInputList=[]
                        pcmInputList.append('0591')
                        pcmInputList.append(alarmObject.get_item('rack'))
                        pcmInputList.append(alarmObject.get_item('shelf'))
                        pcmInputList.append(alarmObject.get_item('card'))
                        pcmInputList.append(alarmObject.get_item('snode'))
                        try:#查询monitor_zx_pcm_config表，判断是否需要进行PCM告警
                            outputParam=paramUtil.invoke("monitor_zx_pcm_alarm_query", str(LinkConst.SPLIT_COLUMN).join(pcmInputList), URL)
                            if outputParam.is_success() and outputParam.get_first_column_value()=='1':#告警在5分钟内,需要告警.
                                alarmContent=alarmObject.get_title()
                                alarmContent+=':'+alarmObject.get_item('alarmcode')
                                alarmContent+=',PCM开始端口:'+outputParam.get_column_value(0,0,1).encode('GBK')
                                alarmContent+='后的30个电路,备注:'+outputParam.get_column_value(0,0,2).encode('GBK')
                                alarmContent+=' '
                                alarmToPersonList.append(alarmContent)
                        except Exception:
                            log.exception('调用服务错误.服务名:monitor_zx_pcm_alarm_query,输入参数:'+str(LinkConst.SPLIT_COLUMN).join(pcmInputList))
                    else:
                        alarmContent=alarmObject.get_title()
                        if alarmObject.get_item('alarmcode')<>None:
                            alarmContent+=':'+alarmObject.get_item('alarmcode')
                        elif alarmObject.get_item('text')<>None:
                            alarmContent+=':'+alarmObject.get_item('text')
                            alarmContent+=' '
                        alarmToPersonList.append(alarmContent)
                else:
                    log.info('告警类型:%s的告警级别:%s 小于配置的告警级别:%s',alarmObject.get_type_id(),currLevel,str(alaramConfigMap['alarm_level']))
            elif alarmObject.get_log_type()=='2':#恢复告警
                alarmToPersonList.append(alaramConfigMap['alarm_name']+'已恢复')

        except KeyError:
            log.warn('告警类型未配置:'+alarmObject.get_type_id())
            #log.exception('告警类型未配置:'+alarmObject.get_type_id())
    if len(alarmToPersonList)>0:
        isPcmAlarm=False
        for alarmToPerson in alarmToPersonList:
            if alarmToPerson.find('PCM')>-1:
                isPcmAlarm=True
                break
        smsContent=''
        if isPcmAlarm:
            smsContent=MONITOR_NAME+'_PCM'+str(LinkConst.SPLIT_COLUMN)+''.join(alarmToPersonList)
        else:
            smsContent=MONITOR_NAME+str(LinkConst.SPLIT_COLUMN)+''.join(alarmToPersonList)
        global lastSmsContent
        if smsContent==lastSmsContent:
            log.info('发送内容重复，不要发送:%s',smsContent)
        else:
            lastSmsContent=smsContent
            log.info('test:'+smsContent)
            outputParam=paramUtil.invoke("Monitor_Warn_To_Person", MONITOR_NAME+str(LinkConst.SPLIT_COLUMN)+''.join(alarmToPersonList), URL)

def saveToDB(alaramObjectList):
    """调用服务，将告警日志保存到数据库中."""
    paramUtil=ParamUtil()
    inputTable1StrList=[]
    inputTable2StrList=[]
    for alarmobject in alaramObjectList:
        alarmobject.generateLogUrcp(MONITOR_NAME,inputTable1StrList)
        if alarmobject.get_log_type()=='1':
            alarmobject.generateDetailLogUrcp(inputTable2StrList)

    inputStr=str(LinkConst.SPLIT_ROW).join(inputTable1StrList)+str(LinkConst.SPLIT_TABLE)+str(LinkConst.SPLIT_ROW).join(inputTable2StrList)
    log.info('保存到数据输入参数:'+inputStr)
    try:
        outputParam=paramUtil.invoke("monitor_zx_writeAlarmLog", inputStr, URL)
        if outputParam.is_success():
            return True
        else:
            return False
    except Exception:
        log.exception('系统报错')
        return False
def checkToWarn(alarmObjectMap,alarmObjectList):
    """
      判断是否需要告警，对于20s就自动回复的告警，就不要发给相关人员了.
    """
    alarmObjectToPersonList=[]
    for alarmObject in alarmObjectList:
        if alarmObject.get_log_type()=='2'and alarmObjectMap.has_key(alarmObject.get_seq()):
            log.info('condy:pop key=%s',alarmObject.get_seq())
            alarmObjectMap.pop(alarmObject.get_seq())
        elif alarmObject.get_log_type()=='1':
            log.info('condy:add key=%s',alarmObject.get_seq())
            alarmObjectMap[alarmObject.get_seq()]=alarmObject
        else:
            log.info('condy:add warn to Person key=%s',alarmObject.get_seq())
            alarmObjectToPersonList.append(alarmObject)

    currTime=datetime.datetime.now()
    #中兴交换机与告警机之间相差1分45s的时间，所以时间判断是要加上这个1分45s。
    tenSecBefore=datetime.timedelta(seconds=125)
    for seq,alarmObject in alarmObjectMap.copy().items():
        log.info('condy:key=%s,time=%s',seq,alarmObject.get_time_str())
        if alarmObject.get_time()+tenSecBefore<currTime:
            alarmObjectToPersonList.append(alarmObject)
            alarmObjectMap.pop(seq)
            log.info('condy:to warn person key=%s,time=%s',seq,alarmObject.get_time_str())
    return alarmObjectToPersonList






def get_version():
    version ='1.1.0.7'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  zx_monitor.py current version is %s               '%(version))
    log.info('  author:Condy create time:2011.07.12')
    log.info('  使用方法:启动方法1.确认zx_monitor.ini中的IS_START=1.启动 nohup ./zx_monitor.py &  ')
    log.info('           关闭:修改zx_monitor.ini中的IS_START参数更改为0.就会自动停止')
    log.info(' 功能点：收集中兴交换记得告警日志及相关告警')
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
    h1 = logging.handlers.RotatingFileHandler(config_dir+'zx_monitor.log',maxBytes=2097152,backupCount=5)
    #h1.setLevel(logging.INFO)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    getAlaramConfigByService()
    try:
        log.info('TELNET_IP:%s,TELNET_PORT:%s',TELNET_IP,TELNET_PORT)
        tn = telnetlib.Telnet(TELNET_IP,TELNET_PORT)
        while IS_START=='1':
            time.sleep(4)
            getCommonConfig()
            rawStr=tn.read_very_eager()
            log.debug('recieve data: %s',rawStr)
            alaramObjectList=parseReadData(rawStr)
            alarmToPersonList=checkToWarn(alarmObjectMap,alaramObjectList)
            if len(alarmToPersonList)>0:
                alarmToPerson(alarmToPersonList)
            if len(alaramObjectList)>0:
                saveToDB(alaramObjectList)
        tn.close()
        log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('系统报错')
