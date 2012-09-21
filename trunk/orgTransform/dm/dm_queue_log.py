# -*- coding:utf-8-*-
#========================================================================
#   FileName: dm_queue_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_queue_log.py相关表
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine,Integer
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class dm_queue_log(Base):
    __tablename__ = 'dm_queue_log'
    queue_id=Column(String(32),primary_key=True)
    call_id=Column(String(32))#呼叫流水号
    call_time=Column(DateTime)
    node_id=Column(String(32))
    acd_no=Column(Float)
    wait_time=Column(Float)
    start_time=Column(DateTime)
    finish_time=Column(DateTime)
    finish_reason=Column(Float)
    primary_caller=Column(String(32))
    primary_callee=Column(String(32))
    callee=Column(String(32))
    caller=Column(String(32))
    term_id=Column(Float)
    term_type=Column(Float)
    staff_id=Column(String(32))
    call_seq=Column(Float)
    dst_term_id=Column(Float)
    dst_term_type=Column(Float)
    dst_staff_id=Column(Float)
    skilldomain=Column(Float)
    def set_finish_reason(self,cc_queuedetail,dm_call_log):
        """
        #0:成功 1:用户挂机 2:系统挂机 4:排队超时 3:溢出到技能组 8:溢出到其他呼叫中心 6:异常
        """
        if cc_queuedetail.tqresult in (1,2):# 1:路由成功 2:排队成功
            self.finish_reason='0'
        elif cc_queuedetail.tqresult==3:#3:排队超时
            self.finish_reason='4'
        elif cc_queuedetail.tqresult==4:#4:排队取消
            if dm_call_log<>None and dm_call_log.finish_reason==0:
                self.finish_reason='1'
            else:
                self.finish_reason='2'
        elif cc_queuedetail.tqresult in (5,6,7,14):#5:溢出到技能组 6:溢出到子业务 7:溢出到语音信箱 14:溢出到其他呼叫中心平台
            self.finish_reason='3'
        elif cc_queuedetail.tqresult==14:#5:溢出到技能组 6:溢出到子业务 7:溢出到语音信箱 
            self.finish_reason='8'
        else:
            self.finish_reason='6'
def get_dm_queue_log(cc_queuedetail,dm_call_log):
     queue_log=dm_queue_log()
     queue_log.queue_id=cc_queuedetail.connectionid
     queue_log.call_id=cc_queuedetail.connectionid
     queue_log.node_id='1'
     queue_log.acd_no=cc_queuedetail.skillid
     queue_log.wait_time=cc_queuedetail.timelength
     queue_log.start_time=cc_queuedetail.queuestarttime
     queue_log.finish_time=cc_queuedetail.queueendtime
     #0:成功 1:用户挂机 2:系统挂机
     queue_log.set_finish_reason(cc_queuedetail,dm_call_log)
     if dm_call_log<>None:
        queue_log.primary_caller=dm_call_log.primary_caller
        queue_log.call_time=dm_call_log.start_time
        queue_log.primary_callee=dm_call_log.primary_callee
        queue_log.caller=dm_call_log.caller
        queue_log.callee=dm_call_log.callee
     else:
        queue_log.primary_caller=cc_queuedetail.callingnumber
        queue_log.primary_callee=''
        queue_log.call_time=defaulttime
        queue_log.caller=cc_queuedetail.callingnumber
        queue_log.callee=''
     queue_log.dst_term_id=0
     queue_log.dst_term_type=0
     queue_log.dst_staff_id=cc_queuedetail.tqresultagentid
     queue_log.skilldomain=cc_queuedetail.vcid
     queue_log.call_seq=0
     return queue_log
