#!/usr/bin/env python
# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_dm
# Purpose:#   1.ͬ��ƽ̨���м�¼
#
# Author:      ����
#
# Created:     18/08/2012
# Copyright:   (c) ���� 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cx_Oracle
import os
import sys
import logging
import logging.handlers
import ConfigParser
import time
import dm.dm_call_log
import dm.dm_term_call_log
import dm.dm_queue_log
import dm.dm_staff_action_log
import dm.staff_on_duty_info
from zx.cc_calldetail import cc_calldetail
from zx.cc_agentcalldetail import cc_agentcalldetail
from zx.cc_queuedetail import cc_queuedetail 
from zx.cc_logonoffdetail import cc_logonoffdetail
from zx.cc_agentonbusystat import cc_agentonbusystat
from sqlalchemy import MetaData, Table, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
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
    global sNGCCzxStaffPassword
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'zx_dm.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    sNGCCzxStaffPassword=config.get('common', 'sNGCCzxStaffPassword')
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10
    try:
        ECCUC_DB_USER_PWD=config.get('database', 'ECCUC_DB_USER_PWD')
        NGCC_DB_USER_PWD=config.get('database', 'NGCC_DB_USER_PWD')
    except TypeError:
        log.error('��ȡECCUC�����ݿ����ӳ�ʧ��,��ȷ��zxTransform.ini����ECCUC_DB_USER_PWD������')

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

def get_version():
    version ='1.0.0'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  zx_dm.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.08.19 ')
    log.info('  ʹ�÷���:��������1.ȷ��zx_dm.ini�е�IS_START=1.���� nohup ./zx_dm.py &  ')
    log.info('           �ر�:zx_dm.ini�е�IS_START��������Ϊ0.�ͻ��Զ�ֹͣ')
    log.info('  ���ܵ㣺ͬ��dm_call_log,dm_term_call_log,dm_queue_log')
    log.info( '=========================================================================')
    return version
def getLastTime(paramCode):
    """��ȡdm_call_log�ĸ���ʱ��"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from eccuc.ecc_parameters t where t.param_code='"+paramCode+"' and param_owner='ZX_CLOUD'"
    updatetime=None
    try:
        updatetimeResult=__eccdm.execute(sql).first()
        if(updatetimeResult<>None):
           updatetime=updatetimeResult[0]
           log.debug('��ȡ������ֵΪ:'+str(updatetime))
        else:
            log.warn('��ȡ������ֵΪ�գ�������ecc_parameter��û�����ø���Ϣ')
        log.debug(sql)
    except:
        log.exception('ִ��SQL������:%s',sql)
    return updatetime

def setLastTime(paramCode,updatetime):
    """�����ϴ�¼���ĸ���ʱ��"""
    sql="update eccuc.ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='"+paramCode+"' and param_owner='ZX_CLOUD'"
    bResult=False
    try:
        log.info('���¸��µ�ʱ��Ϊ:'+str(updatetime))
        __eccdm.execute(sql,{'updatetime':updatetime})
        __eccdm.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('ִ��SQL������:%s',sql)
    return bResult

def synDmCallLog():
    """
    ����dm_call_Log�� 
    """
    updatetime=getLastTime('DM_CALL_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_calldetailList=__zxdbkf.query(cc_calldetail).filter(cc_calldetail.callendtime>orialupdatetime).order_by(cc_calldetail.callendtime)[:1000]
        calldetail=None
        for index,calldetail in enumerate(cc_calldetailList):
            try:
               call_log=dm.dm_call_log.get_dm_call_log(calldetail)
               __eccdm.add(call_log)
               __eccdm.flush()
               if(index%20==0):
                   __eccdm.commit()
                   updatetime=calldetail.callendtime
            except:
               __eccdm.rollback()
               calldetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
               log.exception('ִ��SQL������')
        __eccdm.flush()
        __eccdm.commit()
        if (calldetail<>None):
          updatetime=calldetail.callendtime
    except:
        __eccdm.rollback()
        calldetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
        log.exception('ִ��SQL������')
    if orialupdatetime<>updatetime:
        setLastTime('DM_CALL_LOG',updatetime)
    log.info('����dm_call_log���ϴθ���ʱ���Ϊ:%s,����ʱ���Ϊ:%s,�ܹ�����:%s��¼',str(orialupdatetime),str(updatetime),str(index))
def synDmQueueLog():
    """
    ����dm_queue_merge,dm_queue_log�� 
    """
    updatetime=getLastTime('DM_QUEUE_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_queuedetailList=__zxdbkf.query(cc_queuedetail,cc_calldetail)\
                .outerjoin(cc_calldetail,cc_calldetail.connectionid==cc_queuedetail.connectionid)\
                .filter(cc_queuedetail.updatetime>orialupdatetime).order_by(cc_queuedetail.updatetime)[:1000]
        queuedetail=None
        for index,(queuedetail,calldetail) in enumerate(cc_queuedetailList):
            try:
               dm_call_log=None
               if calldetail<>None:
                   dm_call_log=dm.dm_call_log.get_dm_call_log(calldetail)
               queue_log=dm.dm_queue_log.get_dm_queue_log(queuedetail,dm_call_log)
               __eccdm.add(queue_log)
               __eccdm.flush()
               if(index%20==0):
                   __eccdm.commit()
            except:
               __eccdm.rollback()
               queuedetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
               log.exception('ִ��SQL������')
        __eccdm.flush()
        __eccdm.commit()
        if (queuedetail<>None):
          updatetime=queuedetail.updatetime
    except:
        __eccdm.rollback()
        queuedetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
        log.exception('ִ��SQL������')
    if orialupdatetime<>updatetime:
        setLastTime('DM_QUEUE_LOG',updatetime)
    log.info('����dm_queue_log���ϴθ���ʱ���Ϊ:%s,����ʱ���Ϊ:%s,�ܹ�����:%s��¼',str(orialupdatetime),str(updatetime),str(index))
def synStaffOnDutyInfo():
    """
    ����staff_on_duty_info�� 
    """
    updatetime=getLastTime('STAFF_ON_DUTY_INFO')
    orialupdatetime=updatetime
    index=0
    try:
        cc_logonoffdetailList=__zxdbkf.query(cc_logonoffdetail).filter(cc_logonoffdetail.endtime>orialupdatetime).order_by(cc_logonoffdetail.endtime)[:1000]
        logonoffdetail=None
        for index,logonoffdetail in enumerate(cc_logonoffdetailList):
            try:
               on_duty_info=dm.staff_on_duty_info.get_staff_on_duty_info(logonoffdetail)
               __eccdm.add(on_duty_info)
               __eccdm.flush()
               if(index%20==0):
                   __eccdm.commit()
            except:
               __eccdm.rollback()
               logonoffdetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
               log.exception('ִ��SQL������')
        __eccdm.flush()
        __eccdm.commit()
        if (logonoffdetail<>None):
          updatetime=logonoffdetail.endtime
    except:
        __eccdm.rollback()
        logonoffdetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
        log.exception('ִ��SQL������')
    if orialupdatetime<>updatetime:
        setLastTime('STAFF_ON_DUTY_INFO',updatetime)
    log.info('����staff_on_duty_info���ϴθ���ʱ���Ϊ:%s,����ʱ���Ϊ:%s,�ܹ�����:%s��¼',str(orialupdatetime),str(updatetime),str(index))
def synDmStaffActionLog():
    """
    ����dm_staff_action_Log�� 
    """
    updatetime=getLastTime('DM_STAFF_ACTION_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_agentonbusystatList=__zxdbkf.query(cc_agentonbusystat).filter(cc_agentonbusystat.end_time>orialupdatetime).order_by(cc_agentonbusystat.end_time)[:1000]
        agentonbusystat=None
        for index,agentonbusystat in enumerate(cc_agentonbusystatList):
            try:
               staff_action_log=dm.dm_staff_action_log.get_dm_staff_action_log(agentonbusystat)
               __eccdm.add(staff_action_log)
               __eccdm.flush()
               if(index%20==0):
                   __eccdm.commit()
            except:
               __eccdm.rollback()
               agentonbusystat=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
               log.exception('ִ��SQL������')
        __eccdm.flush()
        __eccdm.commit()
        if (agentonbusystat<>None):
          updatetime=agentonbusystat.end_time
    except:
        __eccdm.rollback()
        agentonbusystat=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
        log.exception('ִ��SQL������')
    if orialupdatetime<>updatetime:
        setLastTime('DM_STAFF_ACTION_LOG',updatetime)
    log.info('����dm_staff_action_log���ϴθ���ʱ���Ϊ:%s,����ʱ���Ϊ:%s,�ܹ�����:%s��¼',str(orialupdatetime),str(updatetime),str(index))
def synDmTermCallLog():
    """
    ����dm_term_call_Log�� 
    """
    updatetime=getLastTime('DM_TERM_CALL_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_agentcalldetailList=__zxdbkf.query(cc_agentcalldetail).filter(cc_agentcalldetail.updatetime>orialupdatetime).order_by(cc_agentcalldetail.updatetime)[:1000]
        agentcalldetail=None
        for index,agentcalldetail in enumerate(cc_agentcalldetailList):
            try:
               term_call_log=dm.dm_term_call_log.get_dm_term_call_log(agentcalldetail)
               __eccdm.add(term_call_log)
               __eccdm.flush()
               if(index%20==0):
                   __eccdm.commit()
            except:
               __eccdm.rollback()
               agentcalldetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
               log.exception('ִ��SQL������')
        __eccdm.flush()
        __eccdm.commit()
        if (agentcalldetail<>None):
          updatetime=agentcalldetail.updatetime
    except:
        __eccdm.rollback()
        agentcalldetail=None#�ó�None���Ա�֤���������ʧ��updatetime���ᱻ����.
        log.exception('ִ��SQL������')
    if orialupdatetime<>updatetime:
        setLastTime('DM_TERM_CALL_LOG',updatetime)
    log.info('����dm_term_call_log���ϴθ���ʱ���Ϊ:%s,����ʱ���Ϊ:%s,�ܹ�����:%s��¼',str(orialupdatetime),str(updatetime),str(index))
def syn(notUsed):
    try:
         log.info('zx_dm  �߳�������')
         while IS_START=='1':
            try:
                global __eccdm,__zxdbkf
                eccdmengine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000')
                ECCDMSession= sessionmaker(bind=eccdmengine)
                __eccdm= ECCDMSession()
                zxdbkfdmengine = create_engine('oracle+cx_oracle://zxdb_kf:zxdb_kf@zxngccdb')
                ZXDBKFSession= sessionmaker(bind=zxdbkfdmengine)
                __zxdbkf= ZXDBKFSession()
                syndm()
                time.sleep(RECYCLE_TIMES)
                if IS_START=='0':
                    log.info('IS_START value=:'+REC_IS_START+' so zx_dm exit!')
            except Exception:
                log.exception('ϵͳ����')
            finally:
                __closeDB()
    except Exception:
        log.exception('ϵͳ����')
##    try:
##        while IS_START=='1':
##            try:
##                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
##                synZxGroup(eccucDB,zxDB)#ͬ��������Ϣ
##                synZxoperator(eccucDB,zxDB) #ͬ��Ա����Ϣ
##                synZxSkill(eccucDB,zxDB)#ͬ����������Ϣ
##                time.sleep(RECYCLE_TIMES)
##                if IS_START=='0':
##                    log.info('IS_START value=:'+IS_START+' so exit!')
##            except Exception:
##                log.exception('ϵͳ����')
##            finally:
##                closeDB()
##    except Exception:
##        log.exception('ϵͳ����')
def __closeDB():
   if __eccdm<>None:
        __eccdm.close()
        log.info('eccucDB oracle connect success close()')
   if __zxdbkf<>None:
        __zxdbkf.close()
        log.info('zxDB oracle connect success close()')
if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'zx_dm.log',maxBytes=2097152,backupCount=5)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    while IS_START=='1':
       try:
           getCommonConfig()
           #eccdmengine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000',echo=True)
           eccdmengine = create_engine('oracle+cx_oracle://'+ECCUC_DB_USER_PWD,echo=False,poolclass=NullPool)#��Ҫ���ӳأ�Ĭ��������5�����ӵ����ӳ�
           ECCDMSession= sessionmaker(bind=eccdmengine)
           zxdbkfdmengine = create_engine('oracle+cx_oracle://'+NGCC_DB_USER_PWD,echo=False,poolclass=NullPool)
           ZXDBKFSession= sessionmaker(bind=zxdbkfdmengine)
           global __eccdm,__zxdbkf
           __eccdm= ECCDMSession()
           __zxdbkf= ZXDBKFSession()
           synDmCallLog()
           synDmQueueLog()
           synDmTermCallLog()
           synDmStaffActionLog()
           synStaffOnDutyInfo()
           if IS_START=='0':
               log.info('IS_START value=:'+IS_START+' so zx_dm exit!')
       except Exception:
           log.exception('ϵͳ����')
       finally:
           __closeDB()
       time.sleep(RECYCLE_TIMES)
    h1.close()
