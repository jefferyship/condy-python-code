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
terminalInfoMap={}#����Ա����Ϣ�ܱ������е���ģ�û�е����.���ݽṹ:{staff_id:terminalInfo}
fullTerminalInfoMap={}#��������Ա������Ϣ�����ݽṹ:{company_id:{staff_id:terminalInfo}}
incrementTerminalInfoMap={}#��Ҫ�������µ����ݣ��������͵�MQ�������Ϻ����Map����գ����ݽṹ:{company_id:{staff_id:terminalInfo}}
class terminalInfo:
    def __init__(self):
        self.staff_id=None#ecc_staff_manager���staff_id
        self.staff_name=None#Ա������
        self.dept_id=None#����ID
        self.dept_name=None#��������
        self.staff_no=None#Ա������
        self.company_id=None#��˾ID
        self.right_role_id=None
        self.right_role_name=None
        self.tel_role_id=None
        self.tel_role_name=None
        self.skill_names=None#���������ƴ�,�ö��ŷָ�
        self.skills=None  
        self.terminal_id=None#�ն�ID
        self.main_status=None#��״̬: ��ϯ��״̬ 0 AgentNull 2 AgentReady 1 AgentNotReady 3 AgentBusy 4 AgentWorkAfter(�º�����״̬��99:�˳�״̬
        self.sub_status=None#
        self.starttime=None#״̬��ʼʱ��
        self.scan_tag=None#����main_status,sub_status��ʱ��
        self.need_poll=False #�Ƿ���Ҫ����
        self.agentphone=None
        self.node_id=None # ������ID
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
      ��ȡivrtrack.ini�������ļ���Ϣ
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
    #���ݿ�����������Ϣ
    ECCUC_DB_USER_PWD=config.get('database', 'ECCUC_DB_USER_PWD')
    DATABASE_RECYLE_TIMES=float(config.get('database', 'DATABASE_RECYLE_TIMES'))
    #��ȡEbase����ز���
    EBASE_URL=config.get('ebase', 'EBASE_URL')
    EBASE_RECYLE_TIMES=float(config.get('ebase', 'EBASE_RECYLE_TIMES'))
    #��ȡRabbitMQ���������
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
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  pyvirmgr.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.09.10 ')
    log.info('  ʹ�÷���:��������1.ȷ��pyvirmgr.ini�е�IS_START=1.���� nohup ./pyvrimgr.py &  ')
    log.info('           �ر�:pyvrimgr.ini�е�IS_START��������Ϊ0.�ͻ��Զ�ֹͣ')
    log.info('  ���ܵ㣺ͬ��������ϵͳ�Ĺ���')
    log.info( '=========================================================================')
    return version

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
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
            log.info('pyvirmgr.ini���õ�IS_START==\'0\',�����Զ��˳�!')
        else:
            while IS_START=='1':
                try:
                    getCommonConfig()
                    print 'pyvirmgr:'+str(IS_START)
                    if scanDB_thread==None:
                        scanDB_thread=threading.Thread(target=scanDB.syn,args=('',))#�����߳�.
                        scanDB_thread.start()
                        log.info('scanDB,�ֳ�������ϣ��߳�IDΪ:%s',str(scanDB_thread))
                    if ebase_thread==None:
                        ebase_thread=threading.Thread(target=ebase.syn,args=('',))#�����߳�.
                        ebase_thread.start()
                        log.info('ebase,�ֳ�������ϣ��߳�IDΪ:%s',str(ebase_thread))
                    if rpcmq_thread==None:
                        rpcmq_thread=threading.Thread(target=rabbitMQ.rpc_full_terminal_mq,args=('',))#�����߳�.
                        rpcmq_thread.start()
                        log.info('rcpmq_thread,�ֳ�������ϣ��߳�IDΪ:%s',str(rpcmq_thread))
                    if IS_START=='0':
                        if(rabbitMQ.close_rpc_full_terminal_mq('')):
                            log.info('�˳�rcpmq_thread�ɹ�')
                        else:
                            log.info('�˳�rcpmq_threadʧ��')
                        log.info('IS_START value=:'+IS_START+' so pyvirmgr exit!')
                except Exception:
                    log.exception('ϵͳ����')
                time.sleep(RECYCLE_TIMES)
    except Exception:
        log.exception('ϵͳ����')
    finally:
        h1.close()
