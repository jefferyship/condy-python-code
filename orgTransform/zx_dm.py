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
import datetime
import dm.dm_call_log
import dm.dm_term_call_log
import dm.dm_queue_log
import dm.dm_staff_action_log
import dm.staff_on_duty_info
import dm.dm_queue_merge
from zx.cc_calldetail import cc_calldetail
from zx.cc_agentcalldetail import cc_agentcalldetail
from zx.cc_queuedetail import cc_queuedetail 
from zx.cc_logonoffdetail import cc_logonoffdetail
from zx.cc_agentonbusystat import cc_agentonbusystat
from zx.cc_recorddetail import cc_recorddetail
from sqlalchemy import MetaData, Table, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.expression import  func
import sqlalchemy.exc

class dm_queue_cache:
    """缓存静态类"""
    queue_map={}
    @staticmethod
    def has_cache(calldetail):
        """返回一个cache_object的List对象表"""
        if dm_queue_cache.queue_map.has_key(calldetail.connectionid):
            return dm_queue_cache.queue_map.pop(calldetail.connectionid)
        else:
            return False
    @staticmethod
    def set_cache(cache_object):
        if len(dm_queue_cache.queue_map)>7000:
            log.warn('排队缓存，超过系统的阀值:%s,可能是cc_call_detail表的数据有异常',str(7000))
            dm_queue_cache.clear_expire_data()
        if not dm_queue_cache.queue_map.has_key(cache_object.connectionid):
            dm_queue_cache.queue_map[cache_object.connectionid]=[]
        dm_queue_cache.queue_map[cache_object.connectionid].insert(0,cache_object)
        return True
    @staticmethod
    def clear_expire_data():
        curr_datetime=datetime.datetime.now()
        expire_time=datetime.timedelta(hours=2)#2个小时过期
        for key,value in dm_queue_cache.queue_map.items():
            cache_object=value[0]
            if isinstance(cache_object,cc_queuedetail):
                if (cache_object.queuestarttime+expire_time)<curr_datetime:
                    log.info('cc_queue_detail表的数据:connectionid:%s,queuestarttime:%s,被清除缓存',str(cache_object.connectionid),str(cache_object.queuestarttime))
                    
                    del dm_queue_cache.queue_map[key]
            else:
                log.info('未知类被清除缓存:%s',str(cache_object))
                del dm_queue_cache.queue_map[key]

class dm_cache:
    """缓存静态类"""
    cache_map={}
    @staticmethod
    def has_cache(calldetail):
        """返回一个cache_object的List对象表"""
        if dm_cache.cache_map.has_key(calldetail.connectionid):
            return dm_cache.cache_map.pop(calldetail.connectionid)
        else:
            return False
    @staticmethod
    def set_cache(cache_object):
        if len(dm_cache.cache_map)>7000:
            log.warn('排队缓存，超过系统的阀值:%s,可能是cc_call_detail表的数据有异常',str(7000))
            dm_cache.clear_expire_data()
        if not dm_cache.cache_map.has_key(cache_object.connectionid):
            dm_cache.cache_map[cache_object.connectionid]=[]
        dm_cache.cache_map[cache_object.connectionid].insert(0,cache_object)
        return True
    @staticmethod
    def clear_expire_data():
        curr_datetime=datetime.datetime.now()
        expire_time=datetime.timedelta(hours=2)#2个小时过期
        for key,value in dm_cache.cache_map.items():
            cache_object=value[0]
            if isinstance(cache_object,cc_agentcalldetail):
                if (cache_object.begincalltime+expire_time)<curr_datetime:
                    log.info('cc_queue_detail表的数据:connectionid:%s,queuestarttime:%s,被清除缓存',str(cache_object.connectionid),str(cache_object.queuestarttime))
                    
                    del dm_cache.cache_map[key]
            elif isinstance(cache_object,cc_recorddetail):
                if (cache_object.recordstarttime+expire_time)<curr_datetime:
                    log.info('cc_recorddetail表的数据:connectionid:%s,recordstarttime:%s,被清除缓存',str(cache_object.connectionid),str(cache_object.recordstarttime))
                    
                    del dm_cache.cache_map[key]
            else:
                log.info('未知类被清除缓存:%s',str(cache_object))
                del dm_cache.cache_map[key]
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
def getvcIdList():
    """获取虚中心ID"""
    sql="select distinct node_id from eccuc.company where sts='A'"
    vcIdList=[]
    try:
        nodeIdResult=__eccdm.execute(sql)
        for vcid in nodeIdResult:
            vcIdList.append(int(vcid[0]))
        log.debug('获取中兴虚中心的Id:'+sql)
    except:
        log.exception('获取虚中心,执行SQL语句错误:%s',sql)
    return vcIdList

def synDmCallLog(vcIdList):
    """
    更新dm_call_Log表 
    """
    updatetime=getLastTime('DM_CALL_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_calldetailList=__zxdbkf.query(cc_calldetail).filter(cc_calldetail.callendtime>orialupdatetime,cc_calldetail.vcid.in_(vcIdList)).order_by(cc_calldetail.callendtime)[:1000]
        calldetail=None
        for index,calldetail in enumerate(cc_calldetailList):
            try:
               call_log=dm.dm_call_log.get_dm_call_log(calldetail)
               #cache_objectList=dm_cache.has_cache(calldetail)
               #if cache_objectList:
                  #for cache_object in cache_objectList:
                     #if cache_object and isinstance(cache_object,cc_queuedetail):
                        #log.debug('找到cc_queuedetail的缓存类:%s',str(cache_object))
                        #queue_log=dm.dm_queue_log.get_dm_queue_log(cache_object,dm_call_log)
                        #__eccdm.add(queue_log)
                     #elif cache_object and isinstance(cache_object,cc_recorddetail):
                        #log.debug('找到cc_recorddetail的缓存类:%s',str(cache_object))
                        #update_record(cache_object,call_log)
                     #elif cache_object and isinstance(cache_object,cc_agentcalldetail):
                        #log.debug('找到cc_agentcalldetail的缓存类:%s',str(cache_object))
                        #term_call_log=dm.dm_term_call_log.get_dm_term_call_log(agentcalldetail,call_log)
                        #insertIntoDmTermCallLog(term_call_log)

               if call_log.call_type in (7,8,9,10) and company_tf_map.has_key(call_log.callee):# 7,8,9,10 表示呼入
                   call_log.company_id=company_tf_map[call_log.callee]
               elif  company_caller_nbr_map.has_key(call_log.caller):
                   call_log.company_id=company_caller_nbr_map[call_log.caller]
               __eccdm.add(call_log)
               __eccdm.flush()
               if calldetail.firstqueuesstarttime:#排队时间不为空说明有排队，获取排队的相关信息.
                   updateDmQueue(call_log)
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
    log.info('结束dm_call_log。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def updateDmQueue(call_log):
    try:
        connectionid=call_log.call_id
        vcid=call_log.node_id
        cc_queuedetailProxy=__zxdbkf.query(cc_queuedetail).filter(cc_queuedetail.connectionid==connectionid,cc_queuedetail.vcid==vcid).order_by(cc_queuedetail.queuestarttime)
        cc_queuedetailList=[]
        for queuedetail in cc_queuedetailProxy:
            cc_queuedetailList.append(queuedetail)
        queue_logList=dm.dm_queue_log.merge_queue_log(cc_queuedetailList,call_log)
        for queue_log in queue_logList:#设置公司ID
            if company_tf_map.has_key(queue_log.callee):
                queue_log.company_id=company_tf_map[queue_log.callee]
            if skill_no_domain_map.has_key(str(queue_log.acd_no)+','+str(queue_log.node_id)):
                queue_log.skilldomain=skill_no_domain_map[str(queue_log.acd_no)+','+str(queue_log.node_id)]
        if len(queue_logList)>0:
            __eccdm.add_all(queue_logList)
            __eccdm.flush()
        queue_mergeList=dm.dm_queue_merge.merge_queue_merge(cc_queuedetailList,call_log)
        for queue_merge in queue_mergeList:#设置公司ID
            if company_tf_map.has_key(queue_merge.callee):
                queue_merge.company_id=company_tf_map[queue_merge.callee]
            if skill_no_domain_map.has_key(str(queue_merge.last_acd_no)+','+str(queue_merge.node_id)):
                queue_merge.skilldomain=skill_no_domain_map[str(queue_merge.last_acd_no)+','+str(queue_merge.node_id)]

        if len(queue_mergeList)>0:
            __eccdm.add_all(queue_mergeList)
            __eccdm.flush()
    except:
       __eccdm.rollback()
       log.exception('更新排队的相关信息错误')

def synDmQueueLog(vcIdList):
    """
    更新dm_queue_merge,dm_queue_log表 
    """
    updatetime=getLastTime('DM_QUEUE_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_queuedetailList=__zxdbkf.query(cc_queuedetail,cc_calldetail)\
                .join(cc_calldetail,cc_calldetail.connectionid==cc_queuedetail.connectionid)\
                .filter(cc_queuedetail.updatetime>orialupdatetime,cc_queuedetail.vcid.in_(vcIdList)).order_by(cc_queuedetail.updatetime)[:1001]
        queuedetail=None
        for index,(queuedetail,calldetail) in enumerate(cc_queuedetailList):
            try:
               if calldetail==None:#先放在缓存中，在SynDmCallLog时更新数据
                   dm_queue_cache.set_cache(queuedetail)
                   continue
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
               queuedetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (queuedetail<>None):
          updatetime=queuedetail.updatetime
    except:
        __eccdm.rollback()
        queuedetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_QUEUE_LOG',updatetime)
    log.info('结束dm_queue_log。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def update_record(recorddetail,dm_call_log):
        """更新录音表的记录"""
        paramList=[]
        paramList.append(recorddetail.connectionid)#call_seq
        paramList.append('2')#sub_seq,在函数里会判断，如果call_seq重复，会自动加上2
        paramList.append(recorddetail.agentid)#staff_id
        paramList.append(recorddetail.vcid)#cti_node_id
        paramList.append(recorddetail.agentphone)#cti_terminal_info
        paramList.append(recorddetail.calltype)#call_type
        if dm_call_log:
           paramList.append(dm_call_log.caller)#caller_nbr
           paramList.append(dm_call_log.callee)#callee_nbr
        else:
           paramList.append(get_nbr(recorddetail.callingnumber))#caller_nbr
           paramList.append(get_nbr(recorddetail.callednumber))#callee_nbr
        paramList.append(recorddetail.durtime)#duration
        paramList.append(os.path.split(recorddetail.recordpath)[0])#file_path
        file_name=os.path.split(recorddetail.recordpath)[1]
        file_name=file_name.replace('.wav','')
        file_name=file_name.replace('.mp3','')
        paramList.append(file_name)#file_name
        paramList.append(recorddetail.recordstarttime)#begin_time
        paramList.append('99')#vri_node_id
        paramList.append('')#company_id,this is null,company_id set in function
        paramList.append(recorddetail.skillid)#skill_id
        if dm_call_log:
            paramList.append(dm_call_log.start_time)#call_time
        else:
            paramList.append(recorddetail.recordstarttime)#call_time
        funcStr='eccuc.PT_RECORD_WRITE_FROM_ZX('+','.join(str(i) for i in paramList)+')'
        cursor=__eccdmConn.cursor()
        try:
           #call_seq=recorddetail.connectionid
           #sub_seq=''
           #staff_id=recorddetail.agentid
           #cti_node_id=recorddetail.vcid
           #cti_terminal_info=recorddetail.agentphone
           #call_type=recorddetail.calltype
           #caller_nbr=dm_call_log.caller if dm_call_log else get_nbr(recorddetail.callingnumber)
           #callee_nbr=dm_call_log.callee if dm_call_log else get_nbr(recorddetail.callednumber)
           #duration=recorddetail.durtime
           #file_path=os.path.split(recorddetail.recordpath)[0]
           #file_name=os.path.split(recorddetail.recordpath)[1]
           #file_name=file_name.replace('.wav','')
           #file_name=file_name.replace('.mp3','')
           #begin_time=recorddetail.recordstarttime
           #vir_node_id='99'
           #company_id=''
           #skill_id=recorddetail.skillid
           #call_time=dm_call_log.start_time if dm_call_log else recorddetail.recordstarttime
           funcResult=cursor.callfunc('eccuc.PT_RECORD_WRITE_FROM_ZX',cx_Oracle.STRING,paramList)
           log.debug(funcStr)
           if funcResult=='0':
               return True
           else:
               log.warn('写录音错误,结果为:%s,输入参数为:%s',funcResult,funcStr)
               return False
        except:
            log.exception('写录音错误,输入参数为:%s',funcStr)
        finally:
            cursor.close()
def synRecordDetail(vcIdList):
    """
    更新mcc_voice_record表 
    """
    updatetime=getLastTime('RECORD_UPDATE_TIME')
    orialupdatetime=updatetime
    index=0
    try:
        cc_recorddetailList=__zxdbkf.query(cc_recorddetail,cc_calldetail)\
                .join(cc_calldetail,cc_calldetail.connectionid==cc_recorddetail.connectionid)\
                .filter(cc_recorddetail.updatetime>orialupdatetime,cc_recorddetail.vcid.in_(vcIdList)).order_by(cc_recorddetail.updatetime)[:1001]
        recorddetail=None
        for index,(recorddetail,calldetail) in enumerate(cc_recorddetailList):
            try:
               if not calldetail:#先放在缓存中，在SynDmCallLog时更新数据
                   log.info('cc_recorddetail表,connectionid:%s,找不到cc_calldetail的数据，暂时先还在缓存中',recorddetail.connectionid)
                   dm_cache.set_cache(recorddetail)
                   continue
               dm_call_log=dm.dm_call_log.get_dm_call_log(calldetail)
               bResult=update_record(recorddetail,dm_call_log)
            except:
               recorddetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        if (recorddetail<>None):
          updatetime=recorddetail.updatetime
    except:
        recorddetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('RECORD_UPDATE_TIME',updatetime)
    log.info('结束voice_record_MM。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def synStaffOnDutyInfo(vcIdList):
    """
    更新staff_on_duty_info表 
    """
    updatetime=getLastTime('STAFF_ON_DUTY_INFO')
    orialupdatetime=updatetime
    index=0
    try:
        cc_logonoffdetailList=__zxdbkf.query(cc_logonoffdetail).filter(cc_logonoffdetail.endtime>orialupdatetime,cc_logonoffdetail.vcid.in_(vcIdList)).order_by(cc_logonoffdetail.endtime)[:1000]
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
               logonoffdetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (logonoffdetail<>None):
          updatetime=logonoffdetail.endtime
    except:
        __eccdm.rollback()
        logonoffdetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('STAFF_ON_DUTY_INFO',updatetime)
    log.info('结束staff_on_duty_info。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def synDmStaffActionLog(vcIdList):
    """
    更新dm_staff_action_Log表 
    """
    updatetime=getLastTime('DM_STAFF_ACTION_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_agentonbusystatList=__zxdbkf.query(cc_agentonbusystat).filter(cc_agentonbusystat.end_time>orialupdatetime,cc_agentonbusystat.vcid.in_(vcIdList)).order_by(cc_agentonbusystat.end_time)[:1000]
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
               agentonbusystat=None#置成None可以保证，如果更新失败updatetime不会被更新.
               log.exception('执行SQL语句错误')
        __eccdm.flush()
        __eccdm.commit()
        if (agentonbusystat<>None):
          updatetime=agentonbusystat.end_time
    except:
        __eccdm.rollback()
        agentonbusystat=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('执行SQL语句错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_STAFF_ACTION_LOG',updatetime)
    log.info('结束dm_staff_action_log。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def synDmTermCallLog(vcIdList):
    """
    更新dm_term_call_Log表 
    """
    updatetime=getLastTime('DM_TERM_CALL_LOG')
    orialupdatetime=updatetime
    index=0
    try:
        cc_agentcalldetailList=__zxdbkf.query(cc_agentcalldetail,cc_calldetail)\
                .join(cc_calldetail,cc_calldetail.connectionid==cc_agentcalldetail.connectionid)\
                .filter(cc_agentcalldetail.updatetime>orialupdatetime,cc_agentcalldetail.vcid.in_(vcIdList)).order_by(cc_agentcalldetail.updatetime)[:1000]
        agentcalldetail=None
        term_call_log=None
        for index,(agentcalldetail,calldetail) in enumerate(cc_agentcalldetailList):
            call_log=None
            if not calldetail:#先放在缓存中，在SynDmCallLog时更新数据
                dm_cache.set_cache(agentcalldetail)
                continue
            call_log=dm.dm_call_log.get_dm_call_log(calldetail)
            term_call_log=dm.dm_term_call_log.get_dm_term_call_log(agentcalldetail,call_log)
            if not insertIntoDmTermCallLog(term_call_log):
                agentcalldetail=None
        if agentcalldetail:
          updatetime=agentcalldetail.updatetime
    except:
        agentcalldetail=None#置成None可以保证，如果更新失败updatetime不会被更新.
        log.exception('更新到dm_term_call_log的数据错误')
    if orialupdatetime<>updatetime:
        setLastTime('DM_TERM_CALL_LOG',updatetime)
    log.info('结束dm_term_call_log。上次更新时间点为:%s,本次时间点为:%s,总共更新:%s记录',str(orialupdatetime),str(updatetime),str(index))
def get_skill_no_domain_map(skill_no_domain_map):
    """获取技能组与技能域的对应关系"""
    sql="select skill_group_no,skill_domain_code,node_id from eccuc.company_skill_group aa  join eccuc.company_skill_domain bb on (aa.skill_domain_id=bb.skill_domain_id) where aa.sts='A'"
    try:
        countskillgroupResult=__eccdm.execute('select count(*) from ( '+sql+' )').first()
        if len(skill_no_domain_map)<>int(countskillgroupResult[0]):
           log.info('获取技能域与技能组的对应关系表的数据:%s',sql)
           skillgroupResult=__eccdm.execute(sql)
           for temp_skill_group_no,temp_skill_domain_code,temp_node_id in skillgroupResult:
               try:
                 skill_no_domain_map[temp_skill_group_no+','+temp_node_id]=int(temp_skill_domain_code)
               except:
                   log.exception('转换技能域成为int类型失败.技能域的值为:%s',str(temp_skill_domain_code))
    except:
        log.exception('执行SQL语句错误:%s',sql)
def get_company_staff(company_staff_map):
    """从ecc_staff_manager表中获取数据"""
    sql='select staff_id,company_id from eccuc.ecc_staff_manager'
    if len(company_staff_map)==0:
       try:
           log.info('获取ecc_staff_manager表的数据:%s',sql)
           staffResult=__eccdm.execute(sql)
           for temp_staff_id,temp_company_id in staffResult:
               company_staff_map[temp_staff_id]=temp_company_id
       except:
           log.exception('执行SQL语句错误:%s',sql)
    else:
        count_company_staff=len(company_staff_map)
        try:
            staff_count=__eccdm.execute('select count(*) from eccuc.ecc_staff_manager').first()
            if count_company_staff<>int(staff_count[0]):
                log.info('获取ecc_staff_manager表的数据:%s',sql)
                staffResult=__eccdm.execute(sql)
                for temp_staff_id,temp_company_id in staffResult:
                    company_staff_map[temp_staff_id]=temp_company_id
        except:
            log.exception('执行SQL语句错误:%s',sql)
def get_company_tf_nbr(company_tf_map,company_caller_nbr_map):
    """从eccuc.company_tf_nbr,eccuc.company_caller_nbr表中读取特服号码与公司ID的对应关系"""
    ###################################获取company_tf_map表的数据
    sql="select tf_nbr,company_id from eccuc.company_tf_nbr"
    if len(company_tf_map)==0:
       try:
           log.info('获取company_tf_nbr表的数据:%s',sql)
           tfnbrResult=__eccdm.execute(sql)
           for temp_tf_nbr,temp_company_id in tfnbrResult:
               company_tf_map[temp_tf_nbr]=temp_company_id
       except:
           log.exception('get_company_tf_nbr:全量执行SQL语句错误:%s',sql)
    else:
        count_company_tf=len(company_tf_map)
        try:
            tfnbr_count=__eccdm.execute('select count(*) from eccuc.company_tf_nbr ').first()
            if count_company_tf<>int(tfnbr_count[0]):
                tfnbrResult=__eccdm.execute(sql)
                for temp_tf_nbr,temp_company_id in tfnbrResult:
                    company_tf_map[temp_tf_nbr]=temp_company_id
        except:
            log.exception('get_company_tf_nbr:增量执行SQL语句错误:%s',sql)
    sql='select caller_nbr,company_id from eccuc.company_caller_nbr'
    if len(company_caller_nbr_map)==0:
        try:
            log.info('获取company_caller_nbr表的数据:%s',sql)
            caller_nbrResult=__eccdm.execute(sql)
            for temp_caller_nbr,temp_company_id in caller_nbrResult:
                company_caller_nbr_map[temp_caller_nbr]=temp_company_id
        except:
            log.exception('get_company_tf_nbr:全量执行SQL语句错误:%s',sql)
    else:
        count_company_caller=len(company_caller_nbr_map)
        try:
            caller_count=__eccdm.execute('select count(*) from eccuc.company_caller_nbr').first()
            if count_company_caller<>int(caller_count[0]):
                log.info('获取company_caller_nbr表的数据:%s',sql)
                caller_nbrResult=__eccdm.execute(sql)
                for temp_caller_nbr,temp_company_id in caller_nbrResult:
                    company_caller_nbr_map[temp_caller_nbr]=temp_company_id
        except:
            log.exception('get_company_tf_nbr:增量执行SQL语句错误:%s',sql)

def insertIntoDmTermCallLog(term_call_log):
    """将数据插入到dm_term_call_log表中"""
    bResult=True
    try:
       if company_staff_map.has_key(term_call_log.staff_id):
            term_call_log.company_id=company_staff_map[term_call_log.staff_id]
       if skill_no_domain_map.has_key(str(term_call_log.acd_no)+','+str(term_call_log.node_id)):
           term_call_log.skilldomain=skill_no_domain_map[str(term_call_log.acd_no)+','+str(term_call_log.node_id)]
       __eccdm.add(term_call_log)
       __eccdm.flush()
       __eccdm.commit()
    except sqlalchemy.exc.IntegrityError:
       __eccdm.rollback()
       max_sql='select max(call_seq) from '+term_call_log.__tablename__+' where call_id=:call_id'
       max_result=__eccdm.execute(max_sql,{'call_id':term_call_log.call_id}).first()
       log.info('dm_term_call_log over 2 call_id,must get max call_seq,call_id:%s,sql:%s',term_call_log.call_id,max_sql)
       if max_result:
           term_call_log.call_seq=int(max_result[0])+2
           __eccdm.add(term_call_log)
           __eccdm.flush()
           __eccdm.commit()
    except:
       __eccdm.rollback()
       bResult=False
       log.exception('执行SQL语句错误')
    return bResult
def __closeDB():
   if __eccdm<>None:
        __eccdm.close()
        log.info('eccucDB oracle connect success close()')
   if __zxdbkf<>None:
        __zxdbkf.close()
        log.info('zxDB oracle connect success close()')
   if __eccdmConn:
       __eccdmConn.close()
       log.info('__eccdmConn is close()')
if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
    global company_tf_map,company_caller_nbr_map,company_staff_map,skill_no_domain_map
    company_tf_map={}
    company_caller_nbr_map={}
    company_staff_map={}
    skill_no_domain_map={}
    if IS_START=='0':
       log.info('IS_START value=:'+IS_START+' so zx_dm exit!')
    while IS_START=='1':
       try:
           getCommonConfig()
           eccdmengine = create_engine('oracle+cx_oracle://'+ECCUC_DB_USER_PWD,echo=False,poolclass=NullPool)#不要连接池，默认是启用5个连接的连接池
           global __eccdm,__zxdbkf,__eccdmConn
           __eccdmConn=eccdmengine.raw_connection()
           ECCDMSession= sessionmaker(bind=eccdmengine)
           zxdbkfdmengine = create_engine('oracle+cx_oracle://'+NGCC_DB_USER_PWD,echo=False,poolclass=NullPool)
           ZXDBKFSession= sessionmaker(bind=zxdbkfdmengine)
           __eccdm= ECCDMSession()
           __zxdbkf= ZXDBKFSession()
           vcIdList=getvcIdList()
           if len(vcIdList)>0:
              get_company_tf_nbr(company_tf_map,company_caller_nbr_map)
              get_company_staff(company_staff_map)
              get_skill_no_domain_map(skill_no_domain_map)
              synDmCallLog(vcIdList)
              #synDmQueueLog(vcIdList)#已经被updateDmQueue方法代替
              synDmTermCallLog(vcIdList)
              synDmStaffActionLog(vcIdList)
              synStaffOnDutyInfo(vcIdList)
              synRecordDetail(vcIdList)
           if IS_START=='0':
               log.info('IS_START value=:'+IS_START+' so zx_dm exit!')
       except Exception:
           log.exception('系统错误')
       finally:
           __closeDB()
       time.sleep(RECYCLE_TIMES)
    h1.close()
