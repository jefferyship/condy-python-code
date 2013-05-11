# -*- coding:GBK -*-
 #========================================================================
#   FileName: rabbitMQ.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 
# LastChange: 2012-09-16 16:51:05
#========================================================================
import pika 
import pyvirmgr
import simplejson as json
from ServiceUtil import LinkConst
from ServiceUtil import OutputParam
from ServiceUtil import ParamUtil
RABBITMQ_HOST='117.27.135.204'
RABBITMQ_PORT='30038'
log=None
connection = None
channel = None
def productor_increment_terminal_mq():
     exchange_name='increment_terminal'
     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,port=int(RABBITMQ_PORT)))
     channel = connection.channel()
     channel.exchange_declare(exchange=exchange_name,type='direct')
     incrementTerminalInfoMap=pyvirmgr.incrementTerminalInfoMap
     for company_id,companyTerminalMap in incrementTerminalInfoMap.items():
         #json_str=generate_incrementTerminalMap_Json(companyTerminalMap)
         json_str=generate_terminalMap_Xml(companyTerminalMap,'increment_terminal')
         log.debug('increment_terminal_json_str:%s',str(json_str))
         channel.basic_publish(exchange=exchange_name,routing_key=exchange_name+'_'+company_id, body=json_str)
         log.debug(" [%s] Sent %s",exchange_name+'_'+company_id,str(json_str))
     connection.close()
     incrementTerminalInfoMap.clear()#清空incrementTerminalInfoMap的数据
     return True
def generate_incrementTerminalMap_Json(companyTerminalMap):
    """根据parsexml的结果，生成增量的终端状态的数据"""
    terminalInfoList=[]
    jsonMap={'result':'0','resultMsg':'','serviceName':'increment_terminal','data':terminalInfoList}
    for tTerminalInfo in companyTerminalMap.itervalues():
        terminalInfoList.append(tTerminalInfo.get_json_map())
    json_str=json.dumps(jsonMap,encoding='GBK')
    return json_str
def generate_terminalMap_Xml(companyTerminalMap,serviceName):
    """根据parsexml的结果，已xml输出的形式生成终端状态"""
    paramUtil=ParamUtil()
    outputParam=OutputParam()
    outputParam.set_request_serial('')
    outputParam.set_result_code('0')
    outputParam.set_result_message('')
    outputParam.set_service_name('increment_terminal')
    rowList=[]
    for tTerminalInfo in companyTerminalMap.itervalues():
        columnList=[]
        columnList.append(str(tTerminalInfo.staff_id))
        columnList.append(str(tTerminalInfo.staff_name))
        columnList.append(str(tTerminalInfo.staff_no))
        columnList.append(str(tTerminalInfo.dept_id))
        columnList.append(str(tTerminalInfo.dept_name))
        columnList.append(str(tTerminalInfo.tel_role_id))
        columnList.append(str(tTerminalInfo.tel_role_name))
        columnList.append(str(tTerminalInfo.right_role_id))
        columnList.append(str(tTerminalInfo.right_role_name))
        columnList.append(str(tTerminalInfo.skills))
        columnList.append(str(tTerminalInfo.main_status))
        columnList.append(str(tTerminalInfo.sub_status))
        columnList.append(str(tTerminalInfo.agentphone))
        columnList.append(str(tTerminalInfo.terminal_id))
        columnList.append(str(tTerminalInfo.starttime))
        columnList.append(str(tTerminalInfo.terminal_ip))
        rowList.append(str(LinkConst.SPLIT_COLUMN).join(columnList))
    tableStr=str(LinkConst.SPLIT_ROW).join(rowList)
    tables=paramUtil.strToTables(tableStr)
    outputParam.set_tables(tables)
    outputXml=paramUtil.output_param_to_xml(outputParam)
    log.debug(outputXml)
    return outputXml

def generate_fullTerminalMap_Xml(company_id):
    paramUtil=ParamUtil()
    outputParam=OutputParam()
    outputParam.set_request_serial('')
    outputParam.set_service_name('fullcrement_terminal')
    if pyvirmgr.fullTerminalInfoMap.has_key(company_id)==False:
        outputParam.set_result_code('-1')
        outputParam.set_result_message('no data')
        outputXml=paramUtil.output_param_to_xml(outputParam)
    else:
        companyTerminalMap=pyvirmgr.fullTerminalInfoMap[company_id]#该公司的在线状态信息
        outputXml=generate_terminalMap_Xml(companyTerminalMap,'fullcrement_terminal')
    log.debug(outputXml)
    return outputXml


def generate_fullTerminalMap_Json(company_id):
    """将pyvirmgr.fullTerminalInfoMap的数据，根据公司ID，生成对应的Json"""
    terminalInfoList=[]
    jsonMap={'result':'0','resultMsg':'','serviceName':'fullcrement_terminal','data':terminalInfoList}
    if pyvirmgr.fullTerminalInfoMap.has_key(company_id)==False:
        jsonMap={'result':'-1','resultMsg':'no data','serviceName':'full_terminal','data':[]}
    else:
        companyTerminalMap=pyvirmgr.fullTerminalInfoMap[company_id]#该公司的在线状态信息
        for tTerminalInfo in companyTerminalMap.itervalues():
            terminalInfoList.append(tTerminalInfo.get_json_map())
    json_str=json.dumps(jsonMap,encoding='GBK')
    return json_str
def consumer_increment_terminal_mq():
     global channel,connection
     exchange_name='increment_terminal'
     company_id='1'
     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,port=int(RABBITMQ_PORT)))
     channel = connection.channel()
     channel.exchange_declare(exchange=exchange_name,type='direct')
     result = channel.queue_declare(exclusive=True)
     queue_name = result.method.queue
     channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=exchange_name+'_'+company_id)
     channel.basic_consume(consumer_increment_callback, queue=queue_name, no_ack=True)
     channel.start_consuming()
     
def consumer_increment_callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)
def rpc_full_terminal_mq(noUsed):
     """rpc方式调用full_terminal的测试"""
     global channel,connection
     exchange_name='fullcrement_terminal'
     #pyvirmgr.terminalInfoMap['105']=pyvirmgr.terminalInfo()
     #pyvirmgr.terminalInfoMap['105'].company_id='1'
     #pyvirmgr.terminalInfoMap['105'].staff_id='105'
     #pyvirmgr.terminalInfoMap['105'].staff_no='26'
     #pyvirmgr.terminalInfoMap['105'].staff_name='林桦'
     #pyvirmgr.terminalInfoMap['107']=pyvirmgr.terminalInfo()
     #pyvirmgr.terminalInfoMap['107'].company_id='1'
     #pyvirmgr.terminalInfoMap['107'].staff_id='107'
     #pyvirmgr.terminalInfoMap['107'].staff_no='08'
     #pyvirmgr.terminalInfoMap['107'].staff_name='周德标'
     #pyvirmgr.fullTerminalInfoMap['1']={'105':pyvirmgr.terminalInfoMap['105']}
     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,port=int(RABBITMQ_PORT)))
     channel = connection.channel()
     channel.queue_declare(queue=exchange_name)
     channel.basic_qos(prefetch_count=1)
     channel.basic_consume(rpc_full_on_request, queue=exchange_name)
     log.info('rpc service get full terminal info is listening ..............')
     channel.start_consuming()
def close_rpc_full_terminal_mq(noUsed):
    global connection,channel
    if connection:
        channel.stop_consuming()
        connection.close()
        return True
    else:
        return False


def rpc_full_on_request(ch,method,props,body):
    company_id=str(body)
    log.info('get full terminal info:company_id:'+company_id)
    #full_terminal_json=generate_fullTerminalMap_Json(company_id)
    full_terminal_json=generate_fullTerminalMap_Xml(company_id)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(full_terminal_json))
    ch.basic_ack(delivery_tag = method.delivery_tag)
     
if __name__ == '__main__':
   consumer_increment_terminal_mq() 
   #rpc_full_terminal_mq()
