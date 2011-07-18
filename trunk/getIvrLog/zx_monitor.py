#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import telnetlib
from ServiceUtil import ParamUtil
from ServiceUtil import LinkConst
import re
class AlarmObject:
    """
    告警对象
    """
    def __init__(self,seq_value=None,alarm_time=None,alarm_level=None,log_type=None,type_id=None):
        self.__itemMap={}
        self.set_seq(seq_value)
        self.set_time(alarm_time)
        self.set_level(alarm_level)
        self.set_log_type(log_time)
        self.set_type_id(type_id)

    def get_seq(self):
        return self.__seq
    def set_seq(self,seq_value):
        self.__seq=seq_value
    def get_time(self):
        return self.__time
    def set_time(self,alarm_time):
        self.__time=alarm_time
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
    def generateUrcp(self):
        rowList=[]
        for key in self.__itemMap.keys():
            columnList=[]
            columnList.append(self.__seq)
            columnList.append(self.__time)
            columnList.append(self.__type_id)
            columnList.append(self.key)
            columnList.append(self.__level)
            columnList.append(self.__itemMap[key])
            columnList.append(self.__log_type)
            rowList.append(str(LinkConst.SPLIT_COLUMN).join(columnList))
        if len(rowList)>0:
            return str(LinkConst.SPLIT_ROW).join(rowList)
        else:
            return ''


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
    sOffinum=alarmDataList[1][1:].strip()#2 591
    sSerialno=alarmDataList[2].strip()#2047650
    sRestoreTime=alarmDataList[3].strip()#2011-03-22 18:53:46
    sAlarmType=alarmDataList[4].strip()#almpcm
    alarmObject=AlarmObject(sSerialno,sRestoreTime,'','2',sAlarmType)
    itemObjectList=alarmDataList[4:-1]#从第5位开始，去除最后的END标志.
    for itemObject in itemObjectList:#IP = 134.132.34.3,mnode = 2
        alarmObject.add_item(itemObject.split('=')[0].strip(),itemObject.split('=')[1].strip())
    print alarmObject.generateUrcp()

def parseAlarm(alarmDataList):
    """
      告警串解析
    """
    pass
def parseReadData(Str):
    """
      解析tims协议.
      字符串内容:'START\r\n2 591     \r\n2047650  \r\n2011-03-22 18:53:46\r\nalmpcm     \r\nIP = 134.132.34.3\r\nmnode = 2\r\nEND
    """
    dataList=re.findall('(START.+?END)',Str,re.S)
    for data in dataList:
        alarmDataList=data.splitlines()
        if alarmDataList[1].startswith('1'):#告警
            parseAlarmData(alarmDataList)
        elif alarmDataList[1].startswith('2'):#恢复告警
            parseAlarmRecoverData(alarmDataList)


    print len(fileList)
    print fileList[0]

if __name__ == '__main__':
    testStr="""START\r\n2 591     \r\n2047650  \r\n2011-03-22 18:53:46\r\nalmpcm     \r\nIP = 134.132.34.3\r\nmnode = 2\r\nEND\r\nSTART2047651  4\r\n2011-03-22 18:53:47\r\nalmpcm     \xca\xfd\xd7\xd6\xd6\xd0\xbc\xccPCM\xb8\xe6\xbe\xaf                         \r\nIP = 134.132.34.3\r\nmnode =  2\r\nsnode = 2\r\nrack = 1\r\nshelf = 6\r\ncard = 6\r\ncircuit = \r\nalarmcode = \xce\xbb\xd6\xc3:2-1-6-6(2\xd0\xd01\xc1\xd0)PCM\xd0\xf2\xba\xc5:2\xd4\xad\xd2\xf2:\xb6\xd4\xb6\xcb\xd6\xa1\xca\xa7\xb2\xbd\r\nEND"""
    parseReadData(testStr)
