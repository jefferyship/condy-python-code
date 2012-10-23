# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_queue_merge.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_queue_merge.py相关表
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
class dm_queue_merge(Base):
    __tablename__ = 'dm_queue_merge'
    call_id=Column(String(32))#呼叫流水号
    merge_id=Column(String(32),primary_key=True)
    merge_mode=Column(Float)
    node_id=Column(String(32))
    call_time=Column(DateTime)
    call_seq=Column(Float)
    wait_time=Column(Float)
    first_acd_no=Column(Float)
    last_acd_no=Column(Float)
    finish_reason=Column(Float)
    start_time=Column(DateTime)
    finish_time=Column(DateTime)
    primary_caller=Column(String(32))
    primary_callee=Column(String(32))
    caller=Column(String(32))
    callee=Column(String(32))
    term_id=Column(String(32))
    term_type=Column(String(32))
    staff_id=Column(String(32))
    dst_term_id=Column(String(32))
    dst_term_type=Column(Float)
    dst_staff_id=Column(String(32))
    merge_count=Column(Float)
    prev_merge_id=Column(String(32))
    next_merge_id=Column(String(32))
    skilldomain=Column(Float)
    company_id=Column(String(32))
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
def get_dm_queue_merge(cc_queuedetail,dm_call_log):
     queue_merge=dm_queue_merge()
     queue_merge.merge_id=cc_queuedetail.connectionid+cc_queuedetail.queuestarttime.strftime('%M%S')
     queue_merge.merge_mode=2#默认是2，这个在归并的merge的方法里面肯定需要修改的.
     queue_merge.call_id=cc_queuedetail.connectionid
     queue_merge.node_id=str(cc_queuedetail.vcid)
     queue_merge.call_seq=1#默认是1，在归并的merge方法中需要修改
     queue_merge.wait_time=cc_queuedetail.timelength
     queue_merge.first_acd_no=cc_queuedetail.skillid#在归并方法中修改
     queue_merge.last_acd_no=cc_queuedetail.skillid#在归并方法中修改
     queue_merge.set_finish_reason(cc_queuedetail,dm_call_log)
     queue_merge.start_time=cc_queuedetail.queuestarttime
     queue_merge.finish_time=cc_queuedetail.queueendtime
     #0:成功 1:用户挂机 2:系统挂机
     if dm_call_log<>None:
        queue_merge.primary_caller=dm_call_log.primary_caller
        queue_merge.primary_callee=dm_call_log.primary_callee
        queue_merge.call_time=dm_call_log.start_time
        queue_merge.caller=dm_call_log.caller
        queue_merge.callee=dm_call_log.callee
     else:
        queue_merge.primary_caller=cc_queuedetail.callingnumber
        queue_merge.primary_callee=''
        queue_merge.call_time=defaulttime
        queue_merge.caller=cc_queuedetail.callingnumber
        queue_merge.callee=''
     queue_merge.dst_term_id=0
     queue_merge.term_id=0
     queue_merge.dst_term_type=0
     queue_merge.dst_staff_id=cc_queuedetail.tqresultagentid
     queue_merge.skilldomain=0
     return queue_merge
def merge_queue_merge(orial_cc_queuedetailList,call_log):
     """将相同排队记录进行归并"""
     queue_mergeList=[]
     cc_queuedetailList=copy.deepcopy(orial_cc_queuedetailList)
     queue_len=len(cc_queuedetailList)
     index=1#统计联系排队的归并的个数
     queuedetail=None
     #######################统计同一队列连续排队的情况#############################
     for temp_queuedetail in cc_queuedetailList:
         if not queuedetail:#第一次循环，queuedetail的赋值，后面肯定不是None
             queuedetail=temp_queuedetail
             continue
         # 相同队列的归并条件:判断技能组是相同的，同时上次的排队的结束时间与下一次排队的开始时间的时间间隔小于2s，
         if queuedetail.skillid==temp_queuedetail.skillid and queuedetail.queueendtime+defaultqueuetimedel>temp_queuedetail.queuestarttime:
             index=index+1
             temp_queuedetail.queuestarttime=queuedetail.queuestarttime
             temp_queuedetail.timelength=temp_queuedetail.timelength+queuedetail.timelength
             queuedetail=temp_queuedetail
         else:
             queue_merge=get_dm_queue_merge(queuedetail,call_log)
             queue_merge.merge_mode=2#连续排队归并
             queue_merge.merge_count=index
             index=1#初始化成1，重新开始累计
             queue_merge.merge_id=queue_merge.merge_id+'_2'
             queue_mergeList.append(queue_merge)
             queuedetail=temp_queuedetail
     if queuedetail:
          queue_merge=get_dm_queue_merge(queuedetail,call_log)
          queue_merge.merge_mode=2#连续排队归并
          queue_merge.merge_count=1#连续排队归并
          queue_merge.merge_id=queue_merge.merge_id+'_2'
          queue_mergeList.append(queue_merge)
          queuedetail=None
     index=0
     for index,queue_merge in enumerate(queue_mergeList):
         queue_merge.call_seq=queue_merge.call_seq+(index*2)# call_seq奇数递增

     #######################统计连续排队的情况#############################
     queue_merge=None
     queue_merge_len=len(queue_mergeList)
     for i in range(queue_merge_len-1,-1,-1):#倒序循环
         temp_queue_merge=queue_mergeList[i]
         if not queue_merge:#第一次循环，赋值
             queue_merge=copy.deepcopy(temp_queue_merge)
             queue_merge.merge_id=queue_merge.merge_id.replace('_2','_1')
             queue_merge.merge_mode=1
             continue
         if queue_merge.call_seq==temp_queue_merge.call_seq:#判断是否属于同一个call_seq,属于同一个call_seq的需要归并
             queue_merge.first_acd_no=temp_queue_merge.first_acd_no
             #queue_merge.wait_time+=temp_queue_merge.wait_time
             queue_merge.merge_count+=temp_queue_merge.merge_count
             queue_merge.staff_id=temp_queue_merge.staff_id
         else:#不属于同一个呼叫流水，
             queue_mergeList.append(queue_merge)
             queue_merge=copy.deepcopy(temp_queue_merge)
             queue_merge.merge_id=queue_merge.merge_id.replace('_2','_1')
             queue_merge.merge_mode=1
     if queue_merge:
         queue_mergeList.append(queue_merge)
     for queue_merge in queue_mergeList:
         queue_merge.wait_time=(queue_merge.finish_time-queue_merge.start_time).seconds
     del cc_queuedetailList
     del queue_merge
     return queue_mergeList
