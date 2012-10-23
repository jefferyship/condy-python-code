# -*- coding:UTF-8 -*-
#========================================================================
#   FileName: ebase.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 
# LastChange: 2012-09-12 21:43:57
#========================================================================
import pyvirmgr
import datetime 
import logging
import logging.handlers
import os,sys
import time
from suds.client import Client
import pika
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
log=None
IS_START='1'
RECYCLE_TIMES=20
EBASE_URL='http://117.27.135.241:9087/EbaseAccess/webservice/ZteEbaseAccess?wsdl'
def syn(notUsed):
    try:
         log.info('scanDB线程已启动')
         while IS_START=='1':
            try:
                global RECYCLE_TIMES
                syn_terminalInfo()
                if IS_START=='0':
                    log.info('IS_START value=:'+IS_START+' so scanDB exit!')
            except Exception:
                log.exception('系统错误')
            finally:
                __closeDB()
            time.sleep(RECYCLE_TIMES)
    except Exception:
        log.exception('系统报错')
def queryall_cc_moperstatus():
    client=Client(EBASE_URL)
    ebase_name='ebase.queryall_cc_moperstatus'
    queryxml='<variables><variable1>vcid,agentid,substatus,agentphone,starttime,mainstatus,skills</variable1><variable2>13</variable2></variables> '
    result=client.service.queryBySqlRequest('1','13',ebase_name,queryxml,'','','','','')
    if result.resultcode=='0':
        print result.resultinfo
    #if len(pyvirmgr.terminalInfoMap)==0:
def parsexml():
    pyvirmgr.terminalInfoMap['105']=pyvirmgr.terminalInfo()
    pyvirmgr.terminalInfoMap['105'].company_id='1'
    pyvirmgr.terminalInfoMap['105'].staff_id='105'
    pyvirmgr.terminalInfoMap['105'].staff_no='26'
    pyvirmgr.terminalInfoMap['105'].staff_name='林桦'
    tempxml='<records><record><skills>205,605,606,</skills><substatus>202</substatus><starttime>2012-09-12 21:59:07.0</starttime><agentphone>1206</agentphone><vcid>13</vcid> <mainstatus>2</mainstatus><agentid>105</agentid></record></records>'
    recordsTree=ET.fromstring(tempxml)
    print dir(recordsTree)
    scan_tag=time.time()#更新的标签，对于有更新状态的打上这个标签，如果标签不相等，就认为是该台席退出.
    for recordElement in recordsTree:
        agent_id=recordElement.find('agentid').text
        tTerminalInfo=pyvirmgr.terminalInfoMap[agent_id]
        if tTerminalInfo==None:
            log.warn('ebase:获取不到staff_id:%s,tTerminalInfo的数据,',agent_id)
            continue
        #将最新数据放到全量的终端表中
        if pyvirmgr.fullTerminalInfoMap.has_key(tTerminalInfo.company_id):
            companyTerminalMap=pyvirmgr.fullTerminalInfoMap[tTerminalInfo.company_id]
            if companyTerminalMap.has_key(tTerminalInfo.staff_id)==False:
                companyTerminalMap[tTerminalInfo.staff_id]=tTerminalInfo
        else:
            pyvirmgr.fullTerminalInfoMap[tTerminalInfo.company_id]={}
            pyvirmgr.fullTerminalInfoMap[tTerminalInfo.company_id][tTerminalInfo.staff_id]=tTerminalInfo

        #将最新数据放到增量的终端表中
        if pyvirmgr.incrementTerminalInfoMap.has_key(tTerminalInfo.company_id):
            companyTerminalMap=pyvirmgr.incrementTerminalInfoMap[tTerminalInfo.company_id]
            if companyTerminalMap.has_key(tTerminalInfo.staff_id)==False:
                companyTerminalMap[tTerminalInfo.staff_id]=tTerminalInfo
        else:
            pyvirmgr.incrementTerminalInfoMap[tTerminalInfo.company_id]={}
            pyvirmgr.incrementTerminalInfoMap[tTerminalInfo.company_id][tTerminalInfo.staff_id]=tTerminalInfo

        tTerminalInfo.starttime=recordElement.find('starttime').text
        tTerminalInfo.skills=recordElement.find('skills').text
        tTerminalInfo.agentphone=recordElement.find('skills').text
        sub_status=recordElement.find('substatus').text
        main_status=recordElement.find('mainstatus').text
        print tTerminalInfo.skills
        print tTerminalInfo.skill_names
        tTerminalInfo.set_status(main_status,sub_status,scan_tag)
    print len(pyvirmgr.fullTerminalInfoMap)
    print len(pyvirmgr.incrementTerminalInfoMap)
def rabbitrecieve():
     connection = pika.BlockingConnection(pika.ConnectionParameters(host='117.27.135.204',port=30038))
     channel = connection.channel()
     channel.queue_declare(queue='hello')
     print ' [*] Waiting for messages. To exit press CTRL+C'
     channel.basic_consume(callback, queue='hello', no_ack=True)
     channel.start_consuming()
def callback(ch, method, properties, body):
     print " [x] Received %r" % (body,)


     
    
if __name__ == '__main__':
    #tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    #if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        #config_dir=os.getcwd()+os.sep
    #else:
        #config_dir=tempPath[0]+os.sep
    #log = logging.getLogger()
    #log.setLevel(logging.DEBUG)
    #h1 = logging.handlers.RotatingFileHandler(config_dir+'pyvirmgr.log',maxBytes=2097152,backupCount=5)
    #f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    #h1.setFormatter(f)
    #log.addHandler(h1)
    #syn('aa')
    #log.close()
    #queryall_cc_moperstatus()
    #parsexml()
    rabbitrecieve()
