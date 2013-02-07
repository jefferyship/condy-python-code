# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_term_call_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_term_call_log_xx��ر�
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine,Integer
from sqlalchemy.orm import sessionmaker
import datetime 
import dm_call_log
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#Ĭ�ϵ����ڸ�ʽ
class dm_term_call_log(object):
    call_id=Column(String(32),primary_key=True)#������ˮ��
    call_seq=Column(Integer,primary_key=True)#���������
    node_id=Column(String(32))#CTI�ڵ��
    term_id=Column(Float)#�ն˱��
    term_type=Column(Float)#�ն�����
    staff_id=Column(String(32))#Ա�����
    call_time=Column(DateTime)#����ʱ��
    direction=Column(Float)#���з��� 0:���룬1������
    join_mode=Column(Float)#���뷽ʽ
    prelink_time=Column(DateTime)#ռ����ʼʱ��
    release_time=Column(DateTime)#ռ�ý���ʱ��
    iai_time=Column(DateTime)#ͨ����ʼʱ��
    acm_time=Column(DateTime)#ͨ��Ӧ��ʱ��
    ans_time=Column(DateTime)#ͨ��ժ��ʱ��
    clr_time=Column(DateTime)#ͨ������ʱ��
    primary_caller=Column(String(32))#ԭʼ���к���
    primary_callee=Column(String(32))#ԭʼ���к���
    caller=Column(String(32))#���к���
    callee=Column(String(32))#���к���
    finish_reason=Column(Float)#����ԭ��
    call_type=Column(Float)#��������
    queue_start_time=Column(DateTime)#�Ŷӿ�ʼʱ��
    queue_finish_time=Column(DateTime)#�Ŷӽ���ʱ��
    acd_no=Column(Float)#��������
    associate_merge_id=Column(String(32))#��غϲ�������ˮ��
    caller_user_type=Column(Float)#�����û�����
    skilldomain=Column(Float)#������
    company_id=Column(String(32))
    #affair_type=Column(String(32))#ҵ�����ͣ�10000�Ű���ֵ��
    #customer_brand=Column(String(32))#�ͻ�Ʒ��
    #customer_group=Column(String(32))#�ͻ�ս�Է�Ⱥ
    #tel_type=Column(String(32))#�绰����
    #collect_flag=Column(Float)#�Ƿ�ɼ���־��0δ�ɹ���1���ڲɣ�2�Ѳ�
    def set_call_type(self,cc_agentcalldetail):
        """�������͵�ת��
        1 �˹�������ϯ����������
        2 �����˹�������ϯ������˹������룩
        3 ��ϯ����ת����˹������룩
        4 �Զ�ת����˹������룩�����ݻ���ֻ����������
        5 ����ת����˹������룩
        6 ����������˹������룩
        7 ǿ��������˹������룩
        8 ����������˹������룩
        9 �˹�ת��������˹�����(��)
        98 ����ԭ������ĺ����˹������룩
        99 ����ԭ������ĺ����˹����񣨳���
        """
        if(cc_agentcalldetail.calltype==1):self.call_type=4#1Ϊ�û����루���룩
        elif(cc_agentcalldetail.calltype==2):self.call_type=3#Ϊת�ƻ��񣨺��룩
        elif(cc_agentcalldetail.calltype==3):self.call_type=9#Ϊ�ڲ����루���룩
        elif(cc_agentcalldetail.calltype==4):self.call_type=6#Ϊ���ػ���
        elif(cc_agentcalldetail.calltype==5):self.call_type=7#Ϊ����Ŀǰʵ��û��������ͣ�
        elif(cc_agentcalldetail.calltype==6):self.call_type=1#Ϊ�ⲿ������������
        elif(cc_agentcalldetail.calltype==7):self.call_type=99#Ϊ�ڲ�������������
        elif(cc_agentcalldetail.calltype==8):self.call_type=6#Ϊ����
        elif(cc_agentcalldetail.calltype==9):self.call_type=7#Ϊ�廰
        else:self.call_type=97#������ĺ�������
    def set_finish_reason(self,cc_agentcalldetail):
        """����ԭ��
        1 ���н���ͨ���󱾶˹һ�(�����)
        2 ���н���ͨ����Զ˹һ�(�����)
        3 ͨ�����쳣������ϵͳ��⵽���������Ĺһ���
        4 ����ͨ�����������б��������һ�(�Ѿ�����Զˣ�����δ����ͨ��)
        5 ����ͨ�����������жԶ˾ܾ�Ӧ��(�Ѿ�����Զˣ�����δ����ͨ��)
        6 ����ͨ�����������жԷ���ʱδӦ����ϵͳ���õĳ�ʱʱ����أ���ʱ������¹һ���һ�������Ǳ���Ҳ�����Ǳ���[���������һ�]��
        7 ����ͨ�������������쳣����(ϵͳ��⵽���������Ĺһ�)
        8 �Զ�Ϊ�պ�(û�е���Է�)
        9 ·��ʧ��(û�е���Է�)
        10 �Զ�æ(û�дﵽ�Է�)
        11 �û�æ(��������ʱ)
        99 ����ԭ��
        """
        if cc_agentcalldetail.callendtype ==1:#�û��һ�
           if  cc_agentcalldetail.answertime==None:#����Ӧ��ʱ��գ�˵��ͨ����û�н������û������һ�
               self.finish_reason=5
           else: #����Ӧ��ʱ�䲻Ϊ�գ�˵������ɹ�
               self.finish_reason=2
        elif cc_agentcalldetail.callendtype ==2:#�ʹ��һ�
           if  cc_agentcalldetail.answertime==None:#����Ӧ��ʱ��գ�˵��ͨ����û�н������ʹ������һ�
               self.finish_reason=4
           else: #����Ӧ��ʱ�䲻Ϊ�գ�˵������ɹ�
               self.finish_reason=1
        elif(cc_agentcalldetail.callendtype ==3):#ת�ƻ���
            self.finish_reason=99
        elif(cc_agentcalldetail.callendtype ==4):#ת������
            self.finish_reason=1
        elif(cc_agentcalldetail.callendtype ==5):#���ػ���
            self.finish_reason=99
        elif(cc_agentcalldetail.callendtype ==6):#����
            self.finish_reason=99
        elif(cc_agentcalldetail.calltype in (1,2,3) and cc_agentcalldetail.callendtype ==7):#����ʱ�Ļ���Ա�ܾ�����
            self.finish_reason=4
        elif(cc_agentcalldetail.calltype in (6,7) and cc_agentcalldetail.callendtype ==7):#����ʱ���û��ܾ�����
            self.finish_reason=5
        elif(cc_agentcalldetail.callendtype ==8):#��ʱδӦ��
            self.finish_reason=6
        elif(cc_agentcalldetail.callendtype ==10):#��ʱδӦ��
            self.finish_reason=1
        else:self.finish_reason=99

class dm_term_call_log_01(dm_term_call_log,Base):
     __tablename__ = 'dm_term_call_log_01'
class dm_term_call_log_02(dm_term_call_log,Base):
     __tablename__ = 'dm_term_call_log_02'
class dm_term_call_log_03(dm_term_call_log,Base):
     __tablename__ = 'dm_term_call_log_03'
class dm_term_call_log_04(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_04'
class dm_term_call_log_05(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_05'
class dm_term_call_log_06(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_06'
class dm_term_call_log_07(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_07'
class dm_term_call_log_08(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_08'
class dm_term_call_log_09(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_09'
class dm_term_call_log_10(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_10'
class dm_term_call_log_11(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_11'
class dm_term_call_log_12(dm_term_call_log,Base):
    __tablename__ = 'dm_term_call_log_12'
def get_dm_term_call_log(cc_agentcalldetail,call_log):
    month=cc_agentcalldetail.begincalltime.strftime('%m')# 08
    term_call_log=None
    if(month=='01'): term_call_log=dm_term_call_log_01()
    elif(month=='02'): term_call_log=dm_term_call_log_02()
    elif(month=='03'): term_call_log=dm_term_call_log_03()
    elif(month=='04'): term_call_log=dm_term_call_log_04()
    elif(month=='05'): term_call_log=dm_term_call_log_05()
    elif(month=='06'): term_call_log=dm_term_call_log_06()
    elif(month=='07'): term_call_log=dm_term_call_log_07()
    elif(month=='08'): term_call_log=dm_term_call_log_08()
    elif(month=='09'): term_call_log=dm_term_call_log_09()
    elif(month=='10'): term_call_log=dm_term_call_log_10()
    elif(month=='11'): term_call_log=dm_term_call_log_11()
    elif(month=='12'): term_call_log=dm_term_call_log_12()
    if(term_call_log<>None):
        term_call_log.call_id=cc_agentcalldetail.connectionid
        term_call_log.call_seq=2
        term_call_log.node_id=str(cc_agentcalldetail.vcid)
        term_call_log.term_id=1
        term_call_log.term_type=1
        term_call_log.staff_id=cc_agentcalldetail.agentid
        term_call_log.set_call_type(cc_agentcalldetail)

        if (cc_agentcalldetail.calltype in (1,2,3)): term_call_log.direction=0 #1Ϊ�û����루���룩2Ϊת�ƻ��񣨺��룩3Ϊ�ڲ����루���룩
        elif (cc_agentcalldetail.calltype in (6,7)): term_call_log.direction=1 #Ϊ�ⲿ������������Ϊ�ڲ�������������
        else:term_call_log.direction=None #���������Ϊ0

        term_call_log.join_mode=1
        term_call_log.prelink_time=cc_agentcalldetail.ringingstarttime
        if term_call_log.prelink_time==None: term_call_log.prelink_time=cc_agentcalldetail.begincalltime
        term_call_log.release_time=cc_agentcalldetail.callendtime
        term_call_log.iai_time=cc_agentcalldetail.ringingstarttime
        term_call_log.acm_time=cc_agentcalldetail.ringingstarttime
        term_call_log.ans_time=cc_agentcalldetail.answertime
        term_call_log.clr_time=cc_agentcalldetail.callendtime
        term_call_log.call_time=cc_agentcalldetail.begincalltime
        if(term_call_log.prelink_time==None):term_call_log.prelink_time=defaulttime
        if(term_call_log.release_time==None):term_call_log.release_time=defaulttime
        if(term_call_log.iai_time==None):term_call_log.iai_time=defaulttime
        if(term_call_log.acm_time==None):term_call_log.acm_time=defaulttime
        if(term_call_log.ans_time==None):term_call_log.ans_time=defaulttime
        if(term_call_log.clr_time==None):term_call_log.clr_time=defaulttime

        term_call_log.primary_caller=call_log.primary_caller
        term_call_log.primary_callee=call_log.primary_callee
        term_call_log.caller=call_log.caller
        term_call_log.callee=call_log.callee
        if term_call_log.caller:
           term_call_log.caller=dm_call_log.get_nbr(term_call_log.caller)#����11λ�ƶ�������������ָ�
        if term_call_log.callee:
           term_call_log.callee=dm_call_log.get_nbr(term_call_log.callee)#����11λ�ƶ�������������ָ�
        term_call_log.set_finish_reason(cc_agentcalldetail)
        term_call_log.queue_start_time=cc_agentcalldetail.queuebegintime
        term_call_log.queue_finish_time=cc_agentcalldetail.queueendtime
        term_call_log.acd_no=cc_agentcalldetail.skillid
        term_call_log.associate_merge_id=None
        term_call_log.caller_user_type=None
        term_call_log.skilldomain=0
        #term_call_log.affair_type=cc_agentcalldetail.servicekey
        #term_call_log.collect_flag=1
    return term_call_log
if __name__ == '__main__':
    engine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000')
    Session = sessionmaker(bind=engine)
    session = Session()
    dmCallLogList=session.query(dm_term_call_log_08).all()
    print dmCallLogList
    if len(dmCallLogList)>0:
        print dmCallLogList[0].call_id
    session.close()
