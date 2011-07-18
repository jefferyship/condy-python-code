#!/usr/bin/env python
# -*- coding: GBK -*-
##################################################################
##    名称: unloadtable
##    功能:  本 shell 用于将表中数据记录导入
##                 导入为字段值用分隔符'|'分开的.dat文件
##    编者：Condy
##    日期: 2009.11.17
##    用法: ./imp.py table_name oracle_username/oracle_pwd@tnsname
##################################################################
import os
import sys
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

