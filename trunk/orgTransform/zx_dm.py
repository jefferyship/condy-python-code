#!/usr/bin/env python
# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_dm
# Purpose:#   1.同步平台呼叫记录
#
# Author:      林桦
#
# Created:     18/08/2012
# Copyright:   (c) 林桦 2012
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
from zx.cc_calldetail import cc_calldetail
from zx.cc_agentcalldetail import cc_agentcalldetail
from sqlalchemy import MetaData, Table, Column, create_engine
from sqlalchemy.orm import sessionmaker
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
        log.error('获取ECCUC的数据库连接池失败,请确认zxTransform.ini中有ECCUC_DB_USER_PWD的配置')

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

def get_version():
    version ='1.0.0'
    """
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  zx_dm.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.08.19 ')
    log.info('  使用方法:启动方法1.确认zx_dm.ini中的IS_START=1.启动 nohup ./zx_dm.py &  ')
    log.info('           关闭:zx_dm.ini中的IS_START参数更改为0.就会自动停止')
    log.info('  功能点：同步dm_call_log,dm_term_call_log,dm_queue_log')
    log.info( '=========================================================================')
    return version
def getLastTime(paramCode):
    """获取dm_call_log的更新时间"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from eccuc.ecc_parameters t where t.param_code='"+paramCode+"' and param_owner='ZX_CLOUD'"
    updatetime=None
    try:
        updatetimeResult=__eccdm.execute(sql).first()
        if(updatetimeResult<>None):
           updatetime=updatetimeResult[0]
           log.debug('获取的日期值为:'+str(updatetime))
        else:
            log.warn('获取的日期值为空，可能在ecc_parameter表没有配置该信息')
        log.debug(sql)
    except:
        log.exception('执行SQL语句错误:%s',sql)
    return updatetime

def setLastTime(paramCode,updatetime):
    """设置上次录音的更新时间"""
    sql="update eccuc.ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='"+paramCode+"' and param_owner='ZX_CLOUD'"
    bResult=False
    try:
        log.info('最新更新的时间为:'+str(updatetime))
        __eccdm.execute(sql,{'updatetime':updatetime})
        __eccdm.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('执行SQL语句错误:%s',sql)
    return bResult

def synDmCallLog():
    """
    更新dm_call_Log表 
    """
    updatetime=getLastTime('DM_CALL_LOG')
    orialupdatetime=updatetime
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
               calldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (calldetail<>None):
          updatetime=calldetail.callendtime
    except:
        __eccdm.rollback()
        calldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_CALL_LOG',updatetime)
def synDmQueueLog():
    """
    更新dm_queue_merge,dm_queue_log表 
    """
    updatetime=getLastTime('DM_QUEUE_LOG')
    orialupdatetime=updatetime
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
               agentcalldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (agentcalldetail<>None):
          updatetime=agentcalldetail.updatetime
    except:
        __eccdm.rollback()
        agentcalldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_TERM_CALL_LOG',updatetime)
def synDmTermCallLog():
    """
    更新dm_term_call_Log表 
    """
    updatetime=getLastTime('DM_TERM_CALL_LOG')
    orialupdatetime=updatetime
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
               agentcalldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (agentcalldetail<>None):
          updatetime=agentcalldetail.updatetime
    except:
        __eccdm.rollback()
        agentcalldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_TERM_CALL_LOG',updatetime)
def syn(notUsed):
    try:
         log.info('zx_dm  线程已启动')
         while REC_IS_START=='1':
            try:
                global __eccdm,__zxdbkf,REC_RECYCLE_TIMES
                eccdmengine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000')
                ECCDMSession= sessionmaker(bind=eccdmengine)
                __eccdm= ECCDMSession()
                zxdbkfdmengine = create_engine('oracle+cx_oracle://zxdb_kf:zxdb_kf@zxngccdb')
                ZXDBKFSession= sessionmaker(bind=zxdbkfdmengine)
                __zxdbkf= ZXDBKFSession()
                syndm()
                time.sleep(REC_RECYCLE_TIMES)
                if REC_IS_START=='0':
                    log.info('IS_START value=:'+REC_IS_START+' so zx_dm exit!')
            except Exception:
                log.exception('系统错误')
            finally:
                __closeDB()
    except Exception:
        log.exception('系统报错')
##    try:
##        while IS_START=='1':
##            try:
##                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
##                synZxGroup(eccucDB,zxDB)#同步班组信息
##                synZxoperator(eccucDB,zxDB) #同步员工信息
##                synZxSkill(eccucDB,zxDB)#同步技能组信息
##                time.sleep(RECYCLE_TIMES)
##                if IS_START=='0':
##                    log.info('IS_START value=:'+IS_START+' so exit!')
##            except Exception:
##                log.exception('系统错误')
##            finally:
##                closeDB()
##    except Exception:
##        log.exception('系统报错')
def __closeDB():
   if __eccdm<>None:
        __eccdm.close()
        log.info('zx_record eccucDB oracle connect success close()')
   if __zxdbkf<>None:
        __zxdbkf.close()
        log.info('zx_record zxDB oracle connect success close()')
if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'zx_dm.log',maxBytes=2097152,backupCount=5)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    try:
        eccdmengine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000',echo=True)
        ECCDMSession= sessionmaker(bind=eccdmengine)
        global __eccdm,__zxdbkf
        __eccdm= ECCDMSession()
        zxdbkfdmengine = create_engine('oracle+cx_oracle://zxdb_kf:zxdb_kf@zxngccdb',echo=True)
        ZXDBKFSession= sessionmaker(bind=zxdbkfdmengine)
        __zxdbkf= ZXDBKFSession()
        synDmCallLog()
        synDmTermCallLog()
        #time.sleep(REC_RECYCLE_TIMES)
        if RECYCLE_TIMES=='0':
            log.info('IS_START value=:'+RECYCLE_TIMES+' so zx_dm exit!')
    except Exception:
        log.exception('系统错误')
    finally:
        __closeDB()
