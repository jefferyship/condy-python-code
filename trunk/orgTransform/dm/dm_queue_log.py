# -*- coding:GBK-*-
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
import copy
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
defaultqueuetimedel=datetime.timedelta(seconds=2)
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
    dst_staff_id=Column(String(32))
    skilldomain=Column(Float)
    def set_finish_reason(self,cc_queuedetail,dm_call_log):
        """
        #0:成功 1:用户挂机 2:系统挂机 4:排队超时 3:溢出到技能组 8:溢出到其他呼叫中心 6:异常
        """
        if cc_queuedetail.tqresult in (1,2):# 1:路由成功 2:排队成功
            self.finish_reason=0
        elif cc_queuedetail.tqresult==3:#3:排队超时
            self.finish_reason=4
        elif cc_queuedetail.tqresult==4:#4:排队取消
            if dm_call_log<>None and dm_call_log.finish_reason==0:
                self.finish_reason=1
            else:
                self.finish_reason=2
        elif cc_queuedetail.tqresult in (5,6,7,14):#5:溢出到技能组 6:溢出到子业务 7:溢出到语音信箱 14:溢出到其他呼叫中心平台
            self.finish_reason=3
        elif cc_queuedetail.tqresult==14:#5:溢出到技能组 6:溢出到子业务 7:溢出到语音信箱 
            self.finish_reason=8
        else:
            self.finish_reason=6
def get_dm_queue_log(cc_queuedetail,dm_call_log):
     queue_log=dm_queue_log()
     queue_log.queue_id=cc_queuedetail.connectionid+cc_queuedetail.queuestarttime.strftime('%M%S')
     queue_log.call_id=cc_queuedetail.connectionid
     queue_log.node_id=str(cc_queuedetail.vcid)
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
     queue_log.call_seq=1
     return queue_log
def merge_queue_log(orial_cc_queuedetailList,call_log):
     """将相同排队记录进行归并"""
     queue_logList=[]
     cc_queuedetailList=copy.deepcopy(orial_cc_queuedetailList)
     queue_len=len(cc_queuedetailList)
     index=0
     queuedetail=None
     for temp_queuedetail in cc_queuedetailList:
         if not queuedetail:#第一次循环，queuedetail的赋值，后面肯定不是None
             #print 'connectionid:'+str(call_log.call_id)+'len:'+str(len(cc_queuedetailList))
             queuedetail=temp_queuedetail
             continue
         # 相同队列的归并条件:判断技能组是相同的，同时上次的排队的结束时间与下一次排队的开始时间的时间间隔小于2s，
         if queuedetail.skillid==temp_queuedetail.skillid and queuedetail.queueendtime+defaultqueuetimedel>temp_queuedetail.queuestarttime:
             #print ('merge:connectionid:%s,skillid:%s,queuestarttime:%s,quesendtime:%s')%(str(queuedetail.connectionid),str(queuedetail.skillid),str(queuedetail.queuestarttime),str(temp_queuedetail.queueendtime))
             temp_queuedetail.queuestarttime=queuedetail.queuestarttime
             #temp_queuedetail.timelength=temp_queuedetail.timelength+queuedetail.timelength
             queuedetail=temp_queuedetail
         else:
             #print ('not merge,connectionid:%s,skillid:%s,queuestarttime:%s,quesendtime:%s')%(str(queuedetail.connectionid),str(queuedetail.skillid),str(queuedetail.queuestarttime),str(temp_queuedetail.queueendtime))
             queue_log=get_dm_queue_log(queuedetail,call_log)
             queue_logList.append(queue_log)
             queuedetail=temp_queuedetail
     if queuedetail:
          queue_log=get_dm_queue_log(queuedetail,call_log)
          queue_logList.append(queue_log)
          queuedetail=None
     for index,queue_log in enumerate(queue_logList):
         queue_log.call_seq=queue_log.call_seq+(index*2)# call_seq奇数递增
         queue_log.wait_time=(queue_log.finish_time-queue_log.start_time).seconds
     del cc_queuedetailList
     del queuedetail
     return queue_logList
