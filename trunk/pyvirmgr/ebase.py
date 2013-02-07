# -*- coding:GBK -*-
#========================================================================
#   FileName: ebase.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 
# LastChange: 2012-09-12 21:43:57
#========================================================================
import pyvirmgr
import logging
import logging.handlers
import time
import rabbitMQ
import cx_Oracle
from suds.client import Client
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
log=None
IS_START='1'
RECYCLE_TIMES=0.2#0.2秒
ECCUC_DB_USER_PWD='eccuc/eccuc@ecc10000'
EBASE_URL='http://117.27.135.241:9087/EbaseAccess/webservice/ZteEbaseAccess?wsdl'
__eccucDB=None
def syn(notUsed):
    try:
         log.info('ebase:线程已启动')
         __eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
         while IS_START=='1':
            try:
                global RECYCLE_TIMES,__eccucDB
                vcidList=pyvirmgr.vcidList
                for vcid in vcidList:
                   synResult=syn_terminalInfo(vcid)
                try:
                    insert_mointor()
                except Exception:
                    log.exception('ebase.py:插入到大屏幕表数据异常')
                if IS_START=='0':
                    log.info('ebase.py:IS_START value=:'+IS_START+' so scanDB exit!')
                    break
            except Exception:
                log.exception('ebase.py:系统错误')
            time.sleep(float(RECYCLE_TIMES))
    except Exception:
        log.exception('ebase.py:系统报错')
    finally:
        __closeDB()
def __closeDB():
   if __eccucDB:
        __eccucDB.close()
        log.info('ebase.py:eccucDB oracle connect success close()')
def insert_mointor():
    """插入数据到监控的相关表"""
    monitorskillMap={}#技能组监控状态表.{key:skill_no+','+node_id,(agent_busy,agent_working,agent_idle)}
    #pyvirmgr.terminalInfoMap['105']=pyvirmgr.terminalInfo()
    #pyvirmgr.terminalInfoMap['105'].company_id='1'
    #pyvirmgr.terminalInfoMap['105'].staff_id='105'
    #pyvirmgr.terminalInfoMap['105'].staff_no='26'
    #pyvirmgr.terminalInfoMap['105'].staff_name='林桦'
    #pyvirmgr.terminalInfoMap['105'].main_status='3'
    #pyvirmgr.terminalInfoMap['105'].skills='205,'
    #pyvirmgr.terminalInfoMap['105'].node_id='13'
    #pyvirmgr.terminalInfoMap['107']=pyvirmgr.terminalInfo()
    #pyvirmgr.terminalInfoMap['107'].company_id='1'
    #pyvirmgr.terminalInfoMap['107'].staff_id='107'
    #pyvirmgr.terminalInfoMap['107'].staff_no='08'
    #pyvirmgr.terminalInfoMap['107'].staff_name='周德标'
    #pyvirmgr.terminalInfoMap['107'].main_status='3'
    #pyvirmgr.terminalInfoMap['107'].skills='206,'
    #pyvirmgr.terminalInfoMap['107'].node_id='13'
    #pyvirmgr.fullTerminalInfoMap={'1':pyvirmgr.terminalInfoMap}
    fullTerminalInfoMap=pyvirmgr.fullTerminalInfoMap
    key=None
    for company_id,companyTerminialInfoMap in fullTerminalInfoMap.items():
        for staff_id,terminalInfo in companyTerminialInfoMap.items():
            if not terminalInfo.skills:# terminalInfo==None,go to next iteror
                continue
            skill_nos=terminalInfo.skills.split(',')
            for skill_no in skill_nos:
               if skill_no=='' or skill_no==None:
                    continue
               key=skill_no+','+terminalInfo.node_id
               skill_monitor_object=None
               if monitorskillMap.has_key(key):
                   skill_monitor_object=monitorskillMap[key]
               else:
                   skill_monitor_object={'agent_busy':0,
                                         'agent_working':0,
                                         'agent_idle':0,
                                         'node_id':terminalInfo.node_id,
                                         'agent_total':0,
                                         'machineip':'127.0.0.1',
                                         'agentid':'0591',
                                         'skill_queue':skill_no,
                                         'busy_rate':0,
                                         'queued_call':0,
                                         'queue_in_call':0,
                                         'queue_out_call':0,
                                         'success_rate':0,
                                         'skill_domain':terminalInfo.node_id
                                         }
                   monitorskillMap[key]=skill_monitor_object
               #3,302:外呼 3,300:呼入 1,105:示忙 2,202:空闲
               if terminalInfo.main_status=='1' and terminalInfo.sub_status=='105':#示忙
                   skill_monitor_object['agent_busy']+=1
               elif terminalInfo.main_status=='2':#空闲
                   skill_monitor_object['agent_idle']+=1
               elif terminalInfo.main_status=='3':#通话中
                   log.info("staff_id:%s,main_status:%s",terminalInfo.staff_id,str(terminalInfo.main_status))
                   skill_monitor_object['agent_working']+=1
               skill_monitor_object['agent_total']+=1
    sql="""
MERGE INTO obj_skill_queue_performance D
   USING (SELECT :machineip machineip,:agentid agentid,:skill_queue skill_queue,sysdate sample_time,
   :agent_total agent_total,:agent_busy agent_busy,
   :agent_working agent_working,:agent_idle agent_idle,
   :busy_rate busy_rate,:queued_call queued_call,
   :queue_in_call queue_in_call,:queue_out_call queue_out_call,:success_rate success_rate,:skill_domain skill_domain,:node_id node_id FROM dual ) S
   ON (D.skill_domain = S.skill_domain and D.node_id = S.node_id and D.skill_queue = S.skill_queue)
   WHEN MATCHED THEN UPDATE SET D.machineip = s.machineip,
     d.agentid=s.agentid,
     d.sample_time=s.sample_time,
     d.agent_total=s.agent_total,
     d.agent_busy=s.agent_busy,
     d.agent_working=s.agent_working,
     d.agent_idle=s.agent_idle,
     d.busy_rate=s.busy_rate,
     d.queued_call=s.queued_call,
     d.queue_in_call=s.queue_in_call,
     d.queue_out_call=s.queue_out_call,
     d.success_rate=s.success_rate
   WHEN NOT MATCHED THEN INSERT(machineip,agentid,skill_queue,sample_time,agent_total,agent_busy,agent_working,agent_idle,busy_rate,queued_call,queue_in_call,queue_out_call,success_rate,skill_domain,node_id)
   VALUES (s.machineip,s.agentid,s.skill_queue,s.sample_time,s.agent_total,s.agent_busy,s.agent_working,s.agent_idle,s.busy_rate,s.queued_call,s.queue_in_call,s.queue_out_call,s.success_rate,s.skill_domain,s.node_id)
    """
    cursor=__eccucDB.cursor()
    skill_monitor_objectList=[]
    try:
        for skill_monitor_object in monitorskillMap.values():
            skill_monitor_objectList.append(skill_monitor_object)
        log.info('ebase.py obj_skill_queue_performance,总共更新:%s条记录',len(skill_monitor_objectList))
        if len(skill_monitor_objectList)>0:
           cursor.executemany(sql,skill_monitor_objectList)
           __eccucDB.commit()
    except:
        log.exception('执行SQL语句错误:%s,输入参数为:%s',sql,str(skill_monitor_objectList))
        __eccucDB.rollback()
    finally:
        cursor.close()


def syn_terminalInfo(vcid):
    """1.取最新的ebase数据的终端状态的数据
       2.解析xml，将xml的数据更新到pyvirmgr的incrementTerminalInfoMap和fullTerminalInfoMap的全局Map中.
       3.根据incrementTerminalInfoMap生成对应的json格式数据
       4.将json格式呼叫推送的RabbitMQ服务器上，由各客户端获取
    """
    terminalInfoMap=pyvirmgr.terminalInfoMap
    fullTerminalInfoMap=pyvirmgr.fullTerminalInfoMap
    incrementTerminalInfoMap=pyvirmgr.incrementTerminalInfoMap
    resultxml=queryall_cc_moperstatus(vcid)
    if resultxml==None:
        return False
    log.debug(resultxml)
    parsexmlResult=parsexml(resultxml,terminalInfoMap,fullTerminalInfoMap,incrementTerminalInfoMap)
    if parsexmlResult==True and len(incrementTerminalInfoMap)>0:
        starttime=time.time()
        rabbitMQ.productor_increment_terminal_mq()
        endtime=time.time()
        log.info('发布用户状态到rabbitMQ,消耗时间:%sms',str(round((endtime-starttime)*100)))
        return True
    else:
        return False

def queryall_cc_moperstatus(vcid):
    """返回调用中兴ebase的ebase.queryall_cc_moperstatus服务的结果。这个服务的数据时在中兴的ebase服务器上配置，
    返回值:None表示获取数据失败，有XML表示获取数据成功
    """
    resultinfo=None
    try:
       client=Client(EBASE_URL)
       ebase_name='ebase.queryall_cc_moperstatus'
       queryxml='<variables><variable1>vcid,agentid,substatus,agentphone,starttime,mainstatus,skills</variable1><variable2>'+vcid+'</variable2></variables> '
       starttime=time.time()
       result=client.service.queryBySqlRequest('1',vcid,ebase_name,queryxml,'','','','','')
       endtime=time.time()
       log.info('call webservice:%s,vcid:%s,used time:%sms',ebase_name,str(vcid),str(round((endtime-starttime)*100)))
       if result.resultcode=='0':
           log.debug(str(result.resultinfo))
           resultinfo=result.resultinfo
       else:
           log.warn('调用ebase.queryall_cc_moperstatus服务错误，输入xml:%s,输出resultcode:%s,resultinfo:%s',str(queryxml),str(result.resultcode),str(result.resultinfo))
    except Exception:
       log.exception('ebase.py:调用ebase接口错误,url地址为:%s',EBASE_URL)
    return resultinfo
def parsexml(tempxml,terminalInfoMap,fullTerminalInfoMap,incrementTerminalInfoMap):
    """解析的xml格式为:<records><record><skills>205,605,606,</skills><substatus>202</substatus><starttime>2012-09-12 21:59:07.0</starttime><agentphone>1206</agentphone><vcid>13</vcid> <mainstatus>2</mainstatus><agentid>105</agentid></record></records>
    """
    #tempxml='<records><record><skills>205,605,606,</skills><substatus>202</substatus><starttime>2012-09-12 21:59:07.0</starttime><agentphone>1206</agentphone><vcid>13</vcid> <mainstatus>2</mainstatus><agentid>105</agentid></record></records>'
    recordsTree=ET.fromstring(tempxml)
    scan_tag=time.time()#更新的标签，对于有更新状态的打上这个标签，如果标签不相等，就认为是该台席退出.
    for recordElement in recordsTree:
        agent_id=recordElement.find('agentid').text
        tTerminalInfo=None
        if terminalInfoMap.has_key(agent_id):
            tTerminalInfo=terminalInfoMap[agent_id]
        if tTerminalInfo==None:
            log.warn('ebase:获取不到staff_id:%s,tTerminalInfo的数据,',str(agent_id))
            continue
        #将最新数据放到全量的终端表中
        if fullTerminalInfoMap.has_key(tTerminalInfo.company_id):
            companyTerminalMap=fullTerminalInfoMap[tTerminalInfo.company_id]
            if companyTerminalMap.has_key(tTerminalInfo.staff_id)==False:
                companyTerminalMap[tTerminalInfo.staff_id]=tTerminalInfo
        else:
            fullTerminalInfoMap[tTerminalInfo.company_id]={}
            fullTerminalInfoMap[tTerminalInfo.company_id][tTerminalInfo.staff_id]=tTerminalInfo
        tTerminalInfo.starttime=recordElement.find('starttime').text
        tTerminalInfo.skills=recordElement.find('skills').text
        tTerminalInfo.agentphone=recordElement.find('agentphone').text
        sub_status=recordElement.find('substatus').text
        main_status=recordElement.find('mainstatus').text
        tTerminalInfo.node_id=recordElement.find('vcid').text
        log.debug('online status:staffid:%s,main_status:%s,sub_status:%s,scan_tag:%s',str(tTerminalInfo.staff_id),str(main_status),str(sub_status),str(scan_tag))
        tTerminalInfo.set_status(main_status,sub_status,scan_tag)
        add_incrementTerminalMap(tTerminalInfo,incrementTerminalInfoMap)
        #将最新数据放到增量的终端表中
    for company_id,companyTerminialInfoMap in fullTerminalInfoMap.items():
       for staff_id,tTerminalInfo in companyTerminialInfoMap.items():
           log.debug('check stat_id:%s,object:scan_tag:%s,used:scan_tag:%s',str(tTerminalInfo.staff_id),str(tTerminalInfo.scan_tag),str(scan_tag))
           if tTerminalInfo.scan_tag<>scan_tag:#说明已经迁出，将迁出的数据提交给增加量的推送Map
               del companyTerminialInfoMap[staff_id]
               add_incrementTerminalMap(tTerminalInfo,incrementTerminalInfoMap)
               log.debug('staff_id:%s 已经签出',staff_id)
    return True
def add_incrementTerminalMap(tTerminalInfo,incrementTerminalInfoMap):
    if tTerminalInfo.need_poll==True:
      if incrementTerminalInfoMap.has_key(tTerminalInfo.company_id):
          companyTerminalMap=incrementTerminalInfoMap[tTerminalInfo.company_id]
          if companyTerminalMap.has_key(tTerminalInfo.staff_id)==False:
              companyTerminalMap[tTerminalInfo.staff_id]=tTerminalInfo
      else:
          incrementTerminalInfoMap[tTerminalInfo.company_id]={}
          incrementTerminalInfoMap[tTerminalInfo.company_id][tTerminalInfo.staff_id]=tTerminalInfo


#if __name__ == '__main__':
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
    #rabbitMQ.log=log
    #__eccucDB=None
    ##syn('aa')
    ##log.close()
    ##queryall_cc_moperstatus()
    ##syn_terminalInfo()
    ##rabbitSend()
    #try:
        ##syn_terminalInfo()
        #__eccucDB=cx_Oracle.connect('eccuc/eccuc@ecc10000')
        #insert_mointor()
    #except Exception:
        #log.exception('ebase.py:系统错误')
    #finally:
        #__closeDB()


