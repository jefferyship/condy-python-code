#!/usr/bin/env python
# -*- coding:GBK -*-
#========================================================================
#   FileName: pyvirmgr.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 
# LastChange: 2012-09-11 19:04:00
#========================================================================
import scanDB
import os,sys
import logging
import logging.handlers
import ConfigParser
import time
import threading
import rabbitMQ
import ebase
terminalInfoMap={}#所以员工信息总表，包含有登入的，没有登入的.数据结构:{staff_id:terminalInfo}
fullTerminalInfoMap={}#所以在线员工的信息，数据结构:{company_id:{staff_id:terminalInfo}}
incrementTerminalInfoMap={}#需要增量更新的数据，数据推送到MQ服务器上后，这个Map就清空，数据结构:{company_id:{staff_id:terminalInfo}}
class terminalInfo:
    def __init__(self):
        self.staff_id=None#ecc_staff_manager表的staff_id
        self.staff_name=None#员工姓名
        self.dept_id=None#部门ID
        self.dept_name=None#部门名称
        self.staff_no=None#员工工号
        self.company_id=None#公司ID
        self.right_role_id=None
        self.right_role_name=None
        self.tel_role_id=None
        self.tel_role_name=None
        self.skill_names=None#技能组名称串,用逗号分隔
        self.skills=None  
        self.terminal_id=None#终端ID
        self.main_status=None#主状态: 座席主状态 0 AgentNull 2 AgentReady 1 AgentNotReady 3 AgentBusy 4 AgentWorkAfter(事后整理状态）99:退出状态
        self.sub_status=None#
        self.starttime=None#状态开始时间
        self.scan_tag=None#更新main_status,sub_status的时间
        self.need_poll=False #是否需要推送
        self.agentphone=None
        self.node_id=None # 虚中心ID
    def set_status(self,mainstatus,substatus,scan_tag):
        if self.main_status==mainstatus and self.sub_status==substatus:
            self.need_poll=False
        else:
            self.need_poll=True
        self.main_status=mainstatus
        self.sub_status=substatus
        self.scan_tag=scan_tag
    def get_json_map(self):
        _json_map={}
        _json_map['staff_id']=str(self.staff_id)
        _json_map['staff_name']=str(self.staff_name)
        _json_map['staff_no']=str(self.staff_no)
        _json_map['dept_name']=str(self.dept_name)
        _json_map['tel_role_id']=str(self.tel_role_id)
        _json_map['tel_role_name']=str(self.tel_role_name)
        _json_map['right_role_id']=str(self.right_role_id)
        _json_map['right_role_name']=str(self.right_role_name)
        _json_map['skills']=str(self.skills)
        _json_map['main_status']=str(self.main_status)
        _json_map['sub_status']=str(self.sub_status)
        _json_map['agentphone']=str(self.agentphone)
        return _json_map
def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
    """
    global URL
    global MONITOR_NAME
    global IS_START
    global RECYCLE_TIMES
    global ECCUC_DB_USER_PWD
    global NGCC_DB_USER_PWD
    global DATABASE_RECYLE_TIMES
    global EBASE_URL
    global EBASE_RECYLE_TIMES
    global EBASE_RECYLE_TIMES
    global RABBITMQ_HOST
    global RABBITMQ_PORT
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'pyvirmgr.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10
    #数据库的相关配置信息
    ECCUC_DB_USER_PWD=config.get('database', 'ECCUC_DB_USER_PWD')
    DATABASE_RECYLE_TIMES=float(config.get('database', 'DATABASE_RECYLE_TIMES'))
    #获取Ebase的相关参数
    EBASE_URL=config.get('ebase', 'EBASE_URL')
    EBASE_RECYLE_TIMES=float(config.get('ebase', 'EBASE_RECYLE_TIMES'))
    #获取RabbitMQ的相关配置
    RABBITMQ_HOST=config.get('rabbitMQ', 'RABBITMQ_HOST')
    RABBITMQ_PORT=config.get('rabbitMQ', 'RABBITMQ_PORT')
    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
    scanDB.RECYCLE_TIMES=DATABASE_RECYLE_TIMES
    scanDB.IS_START=IS_START
    scanDB.ECCUC_DB_USER_PWD=ECCUC_DB_USER_PWD
    ebase.RECYCLE_TIMES=EBASE_RECYLE_TIMES
    ebase.IS_START=IS_START
    ebase.EBASE_URL=EBASE_URL
    ebase.ECCUC_DB_USER_PWD=ECCUC_DB_USER_PWD
    rabbitMQ.RABBITMQ_HOST=RABBITMQ_HOST
    rabbitMQ.RABBITMQ_PORT=RABBITMQ_PORT
def get_version():
    version ='1.0.0'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  pyvirmgr.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.09.10 ')
    log.info('  使用方法:启动方法1.确认pyvirmgr.ini中的IS_START=1.启动 nohup ./pyvrimgr.py &  ')
    log.info('           关闭:pyvrimgr.ini中的IS_START参数更改为0.就会自动停止')
    log.info('  功能点：同步与中兴系统的工号')
    log.info( '=========================================================================')
    return version

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'pyvirmgr.log',maxBytes=2097152,backupCount=5)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    scanDB_thread=None
    ebase_thread=None
    rpcmq_thread=None
    rabbitMQ.log=log
    ebase.log=log
    scanDB.log=log
    
    try:
        if IS_START=='0':
            log.info('pyvirmgr.ini配置的IS_START==\'0\',程序自动退出!')
        else:
            while IS_START=='1':
                try:
                    getCommonConfig()
                    print 'pyvirmgr:'+str(IS_START)
                    if scanDB_thread==None:
                        scanDB_thread=threading.Thread(target=scanDB.syn,args=('',))#启动线程.
                        scanDB_thread.start()
                        log.info('scanDB,现场启动完毕，线程ID为:%s',str(scanDB_thread))
                    if ebase_thread==None:
                        ebase_thread=threading.Thread(target=ebase.syn,args=('',))#启动线程.
                        ebase_thread.start()
                        log.info('ebase,现场启动完毕，线程ID为:%s',str(ebase_thread))
                    if rpcmq_thread==None:
                        rpcmq_thread=threading.Thread(target=rabbitMQ.rpc_full_terminal_mq,args=('',))#启动线程.
                        rpcmq_thread.start()
                        log.info('rcpmq_thread,现场启动完毕，线程ID为:%s',str(rpcmq_thread))
                    if IS_START=='0':
                        if(rabbitMQ.close_rpc_full_terminal_mq('')):
                            log.info('退出rcpmq_thread成功')
                        else:
                            log.info('退出rcpmq_thread失败')
                        log.info('IS_START value=:'+IS_START+' so pyvirmgr exit!')
                except Exception:
                    log.exception('系统错误')
                time.sleep(RECYCLE_TIMES)
    except Exception:
        log.exception('系统报错')
    finally:
        h1.close()
