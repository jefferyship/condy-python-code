# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_queue_merge.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_queue_merge.py��ر�
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine,Integer
from sqlalchemy.orm import sessionmaker
import datetime 
import copy
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#Ĭ�ϵ����ڸ�ʽ
defaultqueuetimedel=datetime.timedelta(seconds=2)
class dm_queue_merge(Base):
    __tablename__ = 'dm_queue_merge'
    call_id=Column(String(32))#������ˮ��
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
        #0:�ɹ� 1:�û��һ� 2:ϵͳ�һ� 4:�Ŷӳ�ʱ 3:����������� 8:����������������� 6:�쳣
        """
        if cc_queuedetail.tqresult in (1,2):# 1:·�ɳɹ� 2:�Ŷӳɹ�
            self.finish_reason=0
        elif cc_queuedetail.tqresult==3:#3:�Ŷӳ�ʱ
            self.finish_reason=4
        elif cc_queuedetail.tqresult==4:#4:�Ŷ�ȡ��
            if dm_call_log<>None and dm_call_log.finish_reason==0:
                self.finish_reason=1
            else:
                self.finish_reason=2
        elif cc_queuedetail.tqresult in (5,6,7,14):#5:����������� 6:�������ҵ�� 7:������������� 14:�����������������ƽ̨
            self.finish_reason=3
        elif cc_queuedetail.tqresult==14:#5:����������� 6:�������ҵ�� 7:������������� 
            self.finish_reason=8
        else:
            self.finish_reason=6
def get_dm_queue_merge(cc_queuedetail,dm_call_log):
     queue_merge=dm_queue_merge()
     queue_merge.merge_id=cc_queuedetail.connectionid+cc_queuedetail.queuestarttime.strftime('%M%S')
     queue_merge.merge_mode=2#Ĭ����2������ڹ鲢��merge�ķ�������϶���Ҫ�޸ĵ�.
     queue_merge.call_id=cc_queuedetail.connectionid
     queue_merge.node_id=str(cc_queuedetail.vcid)
     queue_merge.call_seq=1#Ĭ����1���ڹ鲢��merge��������Ҫ�޸�
     queue_merge.wait_time=cc_queuedetail.timelength
     queue_merge.first_acd_no=cc_queuedetail.skillid#�ڹ鲢�������޸�
     queue_merge.last_acd_no=cc_queuedetail.skillid#�ڹ鲢�������޸�
     queue_merge.set_finish_reason(cc_queuedetail,dm_call_log)
     queue_merge.start_time=cc_queuedetail.queuestarttime
     queue_merge.finish_time=cc_queuedetail.queueendtime
     #0:�ɹ� 1:�û��һ� 2:ϵͳ�һ�
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
     """����ͬ�ŶӼ�¼���й鲢"""
     queue_mergeList=[]
     cc_queuedetailList=copy.deepcopy(orial_cc_queuedetailList)
     queue_len=len(cc_queuedetailList)
     index=1#ͳ����ϵ�ŶӵĹ鲢�ĸ���
     queuedetail=None
     #######################ͳ��ͬһ���������Ŷӵ����#############################
     for temp_queuedetail in cc_queuedetailList:
         if not queuedetail:#��һ��ѭ����queuedetail�ĸ�ֵ������϶�����None
             queuedetail=temp_queuedetail
             continue
         # ��ͬ���еĹ鲢����:�жϼ���������ͬ�ģ�ͬʱ�ϴε��ŶӵĽ���ʱ������һ���ŶӵĿ�ʼʱ���ʱ����С��2s��
         if queuedetail.skillid==temp_queuedetail.skillid and queuedetail.queueendtime+defaultqueuetimedel>temp_queuedetail.queuestarttime:
             index=index+1
             temp_queuedetail.queuestarttime=queuedetail.queuestarttime
             temp_queuedetail.timelength=temp_queuedetail.timelength+queuedetail.timelength
             queuedetail=temp_queuedetail
         else:
             queue_merge=get_dm_queue_merge(queuedetail,call_log)
             queue_merge.merge_mode=2#�����Ŷӹ鲢
             queue_merge.merge_count=index
             index=1#��ʼ����1�����¿�ʼ�ۼ�
             queue_merge.merge_id=queue_merge.merge_id+'_2'
             queue_mergeList.append(queue_merge)
             queuedetail=temp_queuedetail
     if queuedetail:
          queue_merge=get_dm_queue_merge(queuedetail,call_log)
          queue_merge.merge_mode=2#�����Ŷӹ鲢
          queue_merge.merge_count=1#�����Ŷӹ鲢
          queue_merge.merge_id=queue_merge.merge_id+'_2'
          queue_mergeList.append(queue_merge)
          queuedetail=None
     index=0
     for index,queue_merge in enumerate(queue_mergeList):
         queue_merge.call_seq=queue_merge.call_seq+(index*2)# call_seq��������

     #######################ͳ�������Ŷӵ����#############################
     queue_merge=None
     queue_merge_len=len(queue_mergeList)
     for i in range(queue_merge_len-1,-1,-1):#����ѭ��
         temp_queue_merge=queue_mergeList[i]
         if not queue_merge:#��һ��ѭ������ֵ
             queue_merge=copy.deepcopy(temp_queue_merge)
             queue_merge.merge_id=queue_merge.merge_id.replace('_2','_1')
             queue_merge.merge_mode=1
             continue
         if queue_merge.call_seq==temp_queue_merge.call_seq:#�ж��Ƿ�����ͬһ��call_seq,����ͬһ��call_seq����Ҫ�鲢
             queue_merge.first_acd_no=temp_queue_merge.first_acd_no
             #queue_merge.wait_time+=temp_queue_merge.wait_time
             queue_merge.merge_count+=temp_queue_merge.merge_count
             queue_merge.staff_id=temp_queue_merge.staff_id
         else:#������ͬһ��������ˮ��
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
