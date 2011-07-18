#!/usr/bin/env python
# -*- coding: GBK -*-
##################################################################
##    名称: unloadtable
##    功能:  本 shell 用于将表中数据记录导出
##                 导出为字段值用分隔符'|'分开的.dat文件
##    编者：Condy
##    日期: 2009.11.14
##    用法: ./exp.py table_name oracle_username/oracle_pwd@tnsname
##################################################################
import os
import sys
def generateSqlplusConfigFile(fileName):
        newFile=open(fileName+'.sel','w')
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
        columnSqlList=[]
        for columnResult in columnResultList:
                if len(columnResult.split())==2 and columnResult.split()[1]=='DATE':
                        columnSqlList.append("to_char("+columnResult.split()[0]+",'yyyymmddhh24miss')")
                else:
                        columnSqlList.append(columnResult.split()[0])
        del fileContent[-1]
        fileContent.append("select "+"||'|'||".join(columnSqlList)+' from '+tableName+';')
        newFile.write('\n'.join(fileContent))
        newFile.close()

if len(sys.argv)<>3 :
        print " usage:  ./exp.py table_name oracle_username/oracle_pwd@tnsname"
else:
        tableName=sys.argv[1]
        oracleName=sys.argv[2]
        generateSqlplusConfigFile(tableName)
        os.system('sqlplus -s '+oracleName+' <'+tableName+'.sel >'+tableName+'.dat')
