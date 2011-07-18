#!/usr/bin/env python
# -*- coding: GBK -*-
##################################################################
##    名称: SQLLOAD自动台的轨迹日志.
##    功能: 增加二次登入功能
##    编者：Condy
##    日期: 2010.12.18
##    用法: ./ivrtrack.py
##################################################################
import os
import sys
FILE_PATH='/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/log/ivrLog'
FILE_FORMAT='ivrtrack.log.20*'
LOG_PATH='/home/websphere/SQLLoad'
DB_USER=''
DB_PWD=''
ORACLE_HOME='/home/websphere/oracle/product/9.2.0'
def getPassword():
	      passwordFileName=LOG_PATH+'/password.ctl'
				passwordCtlFile=open(passwordFileName,'w')
        fileContent=[]
        fileContent.append('set heading off    ')
        fileContent.append('set pagesize 0')
        fileContent.append('set linesize 800    ')
        fileContent.append('set feedback off    ')
        fileContent.append('set tab off              ')
        fileContent.append("select dbuser,dbpwd from ecc_db_login where rownum<2; ")
        passwordCtlFile.write('\n'.join(fileContent))
        passwordCtlFile.close()
        columnResultList=os.popen('sqlplus -s '+oracleName+'<'+passwordFileName).readlines()
        if len(columnResultList)==1:
        	DB_USER=columnResultList[0].split()[0]
        	DB_PWD=columnResultList[0].split()[1]
        	
        	
def generateSqlplusConfigFile(fileName):
        newFile=open(fileName+'.ctl','w')
        fileContent=[]
        fileContent.append('set heading off    ')
        fileContent.append('set pagesize 0')
        fileContent.append('set linesize 800    ')
        fileContent.append('set feedback off    ')
        fileContent.append('set tab off              ')
        fileContent.append("select  column_name,data_type  from  user_tab_columns  where  lower(table_name)=lower('"+fileName+"')  order  by column_id; ")
        colFile=open(fileName+'.col','w')
        colFile.write('\n'.join(fileContent))
        colFile.close()
        columnResultList=os.popen('sqlplus -s '+oracleName+'<'+fileName+'.col').readlines()
        del fileContent[:]
        fileContent.append('load data infile \''+fileName+'.dat\'')
        fileContent.append('append into table '+tableName)
        fileContent.append("fields terminated by '|' optionally enclosed by '\"' ")
        fileContent.append('TRAILING NULLCOLS')
        fileContent.append('(')
        columnSqlList=[]
        for columnResult in columnResultList:
                if len(columnResult.split())==2 and columnResult.split()[1]=='DATE':
                        columnSqlList.append(columnResult.split()[0]+" DATE(14) \"yyyymmddhh24miss\" NULLIF "+columnResult.split()[0]+"=BLANKS")
                else:
                        columnSqlList.append(columnResult.split()[0])
        fileContent.append(',\n'.join(columnSqlList))
        fileContent.append(')')
        newFile.write('\n'.join(fileContent))
        newFile.close()


if len(sys.argv)<>3 :
        print " usage:  ./imp.py table_name oracle_username/oracle_pwd@tnsname"
else:
        tableName=sys.argv[1]
        oracleName=sys.argv[2]
        generateSqlplusConfigFile(tableName)
        print 'sqlldr userid='+oracleName+' control='+tableName+'.ctl log='+tableName+'.log bad='+tableName+'.bad'
        os.system('sqlldr userid='+oracleName+' control='+tableName+'.ctl log='+tableName+'.log bad='+tableName+'.bad')

