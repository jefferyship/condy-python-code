#-------------------------------------------------------------------------------
# Purpose:获取IVR的日志文件
#
# Author:      林桦
#
# Created:     04/03/2011
# Copyright:   (c) 林桦 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: GBK -*-
import urllib2
import telnetlib
import re
from ftplib import FTP
import os,sys
host={}
def getCallObject(cti_ip,log_time,serv_nbr):
    """
     从CTI获取IVR的地址，及呼叫的记录
    """
    callObjectList=[]
    host['ip']=cti_ip
    host['user']='tnsmcc'
    host['password']='tnsmcc'
    host['commands']=['cd /home/tnsmcc/LOG/ctserver', "grep '"+serv_nbr+"' ctserver"+log_time+".log"]
    tn = telnetlib.Telnet(host['ip'])
    tn.set_debuglevel(0)

    tn.read_until("login: ")
    tn.write(host['user'] + "\n")
    tn.read_until("Password for "+host['user']+": ")
    tn.write(host['password'] + "\n")

    for command in host['commands']:
        tn.write(command+'\n')

    tn.write("exit\n")
    ctiStr= tn.read_all()
    callObject={}
    for str in ctiStr.split('\r'):
        if str.find('UNCC_IAI')<>-1:
            print str
            callObject['ivr_ip']=re.findall('(\d+\.\d+\.\d+\.\d+)',str)[0]
            callObject['ivr_port']=re.findall('(/\d+)',str)[0].replace('/','')
            callObject['call_time']=re.findall('(\d\d:\d\d)',str)[0]
            callObject['sessionNo']=re.findall('(SessionNo=\d+)',str)[0].replace('SessionNo=','')
            callObject['log_time']=log_time
            callObjectList.append(callObject)
            print callObject
    return callObjectList

def getIvrLog(callObject):
    """
    根据呼叫记录，获取IVR上的日志文件。

    """
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    logPath='/home/tnsmcc/LOG/svcsmgr/'
    tn = telnetlib.Telnet(callObject['ivr_ip'])
    tn.set_debuglevel(0)
    tn.read_until("login: ")
    tn.write('tnsmcc' + "\n")
    tn.read_until("Password for tnsmcc: ")
    tn.write('tnstns' + "\n")
    commands=['cd '+logPath,"grep '>"+callObject['ivr_port']+"<' svcsmgr"+callObject['log_time']+".log >"+callObject['sessionNo']+'.log']
    for command in commands:
        tn.write(command+'\n')
    tn.write("exit\n")
    ctiStr= tn.read_all()
    print ctiStr
    ftp=FTP(callObject['ivr_ip'],'tnsmcc','tnstns')
    fileName=logPath+callObject['sessionNo']+'.log'
    print config_dir+os.path.split(fileName)[1]
    ftp.retrbinary('RETR '+fileName,open(config_dir+os.path.split(fileName)[1],'wb').writelines)
    ftp.delete(fileName)
    ftp.quit()


def main():
    #getCallObject('134.132.34.11','','')
    callObject={}
    callObject['ivr_ip']='134.132.34.15'
    callObject['ivr_port']='6936'
    callObject['call_time']='40:02'
    callObject['sessionNo']='00110307054002191757'
    callObject['log_time']='03070540'
    getIvrLog(callObject)

##    xml='<?xml version="1.0" encoding="UTF-8"?><input_params><service_name>MH_GetSMHistory</service_name>	<params>		<tables table_num="1">			<table table_index="1" row_num="1">				<row row_index="1" column_num="3">					<column column_index="1">						<column_name>area_code</column_name>						<column_value>0591</column_value>					</column>					<column column_index="2">						<column_name>tel_no</column_name>						<column_value>18959130026</column_value>					</column>					<column column_index="3">						<column_name>chanel</column_name>						<column_value>MH</column_value>					</column>				</row>			</table>		</tables>	</params></input_params>'
##    paramUtil=ParamUtil()
##    URL='http://134.128.196.24/iservuc/iserv/callService.jsp'
##    f=urllib2.urlopen(URL,xml)
##    outputXML=f.read()
##    outputXML=outputXML.lstrip()
##    print outputXML




if __name__ == '__main__':
    main()
