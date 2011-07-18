#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
##################################################################
##    ���: SQLLOAD�Զ�̨�Ĺ켣��־.
##    ����: ��Ӷ��ε��빦��
##    ���ߣ�Condy
##    ����: 2010.12.18
##    �÷�: ./ivrtrack.py
##################################################################
'''
import os
import time
import ConfigParser
import glob
import base64
FILE_PATH='/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/log/ivrLog'
FILE_FORMAT='ivrtrack.log.20*'
LOG_PATH='/home/websphere/SQLLoad'
ORACLE_HOME='/home/websphere/oracle/product/9.2.0'
SqlLog='sqlload_'+time.strftime('%Y%m%d%H')+'.log'

def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
    """
    #global URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    global URL
    global DB_PWD
    config=ConfigParser.ConfigParser()
    print os.getcwd()+os.sep+'ivrtrack.ini'
    ivrtrackFileObject=open(os.getcwd()+os.sep+'ivrtrack.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    DB_PWD=config.get('common', 'DB_PWD')
    if len(DB_PWD)>0:
        DB_PWD=base64.decodestring(DB_PWD)
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def getPassword():
        global DB_USER
        from ServiceUtil import ParamUtil
        paramUtil=ParamUtil()
        outputParam=paramUtil.invoke("GetSecondDBMsg", 'noUsed', URL)
        if outputParam.is_success() :
            DB_USER=outputParam.get_column_value(0, 0, 0)
            db_pwd=outputParam.get_column_value(0, 0, 1)#数据库用户名的明码
            if DB_PWD!=db_pwd:
                config=ConfigParser.ConfigParser()
                config.readfp(open(os.getcwd()+os.sep+'ivrtrack.ini'))
                print base64.encodestring(db_pwd)
                config.set('common', 'DB_PWD', base64.encodestring(db_pwd))
                config.write(open(os.getcwd()+os.sep+'ivrtrack.ini','r+'))
            return True
        else:
            return False
            
            
def generateSqlplusConfigFile(sqlloadCtlName,fileName):
        newFile=open(sqlloadCtlName,'w')
        sqlloadmonth=fileName[-6:-4]
        fileContent=[]
        fileContent.append("load data infile '"+fileName+"'")
        fileContent.append('append into table ucss_auto_log_'+sqlloadmonth)
        fileContent.append('fields terminated by "'+chr(1)+'''" optionally enclosed by '"' ''')
        fileContent.append('         TRAILING NULLCOLS')
        fileContent.append('(WORKDAY POSITION(3) DATE(14) "yyyymmddhh24miss" NULLIF WORKDAY=BLANKS,')
        fileContent.append("CALLSEQ,")
        fileContent.append("CALLERNBR,")
        fileContent.append("CALLEENBR,")
        fileContent.append('CALLTIME DATE(14) "yyyymmddhh24miss" NULLIF CALLTIME=BLANKS,')
        fileContent.append('OPTTIME DATE(14) "yyyymmddhh24miss" NULLIF OPTTIME=BLANKS,')
        fileContent.append("SERVNBR,")
        fileContent.append("SERVID,")
        fileContent.append("SERVSUBID,")
        fileContent.append("SERVCONTENT,")
        fileContent.append("REPLYTYPE,")
        fileContent.append("ACTIONTYPE,")
        fileContent.append("LEVEL_ID,")
        fileContent.append("CALLER_USER_TYPE,")
        fileContent.append("AREA_ID,")
        fileContent.append("PORT,")
        fileContent.append("CUSTOMER_BRAND,")
        fileContent.append("CUSTOMER_GROUP,")
        fileContent.append("TEL_TYPE,")
        fileContent.append("CALLER_USER_TYPE_NAME,")
        fileContent.append("CUSTOMER_BRAND_NAME,")
        fileContent.append("CUSTOMER_GROUP_NAME,")
        fileContent.append("TEL_TYPE_NAME)")
        newFile.write('\n'.join(fileContent))
        newFile.close()
getCommonConfig()
if getPassword() :
    filenameList=glob.glob(FILE_PATH+'/'+FILE_FORMAT)
    for filename in filenameList:
        generateSqlplusConfigFile(LOG_PATH+'/sqlload.ctl',filename)
        print ORACLE_HOME+'/bin/sqlldr userid='+DB_USER+'/'+DB_PWD+'@fjtccs'+' control='+LOG_PATH+'/sqlload.ctl log='+LOG_PATH+'/'+SqlLog+' bad='+LOG_PATH+'/sqlload.bad direct=yes >>'+LOG_PATH+'/imp.log'
        lastFileName=filename.split('/')[-1]
        os.rename(filename, FILE_PATH+'/complete/'+lastFileName)

#os.system('sqlldr userid='+oracleName+' control='+tableName+'.ctl log='+tableName+'.log bad='+tableName+'.bad')


