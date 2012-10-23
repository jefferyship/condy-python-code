# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_call_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_call_log_xx��ر�
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#Ĭ�ϵ����ڸ�ʽ
class dm_call_log(object):
    call_id=Column(String(32),primary_key=True)
    node_id=Column(String(32))
    call_type=Column(Float)
    charge_flag=Column(Float)
    #���н���ԭ��:
    finish_reason=Column(Float)
    primary_caller=Column(String(32))
    primary_callee=Column(String(32))
    caller=Column(String(32))
    callee=Column(String(32))
    start_time=Column(DateTime)
    dial_time=Column(DateTime)
    answer_time=Column(DateTime)
    offhook_time=Column(DateTime)
    hangup_time=Column(DateTime)
    finish_time=Column(DateTime)
    caller_user_type=Column(Float)
    company_id=Column(String(32))
    def set_call_type(self,cc_calldetail):
        """�����������
    #��������:
    # 1:�˹�������ϯ��������
    # 2:�˹�������ϯ����IVR
    # 3:�˹�������ϯ�����˹�������ϯ
    # 4:IVR��������
    # 5:IVR����IVR
    # 6:IVR�����˹�������ϯ
    # 7:���ߺ���IVR
    # 8:���ߺ����˹�����̨ϯ
    # 9:���ߺ���ת����
    # 10:����
        """
        if(cc_calldetail.calltype==1):self.call_type=7#����
        if(cc_calldetail.calltype==2):self.call_type=3#�ڲ�����
        if(cc_calldetail.calltype==3):self.call_type=1#�˹����
        if(cc_calldetail.calltype==4):self.call_type=4#�Զ����
        if(cc_calldetail.calltype==5):self.call_type=4#�Զ����ת�˹�,TODO ��ʱ��������ڹ�ϵ������Ϊ���Զ����
        if(cc_calldetail.calltype==6):self.call_type=10#webcall����
        if(cc_calldetail.calltype==7):self.call_type=7#�������������������
    def set_finish_reason(self,cc_calldetail):
        """���ú��н���ԭ����Ҫ��ת��
    #1:���н���ͨ�������з��һ�
    #2:���н���ͨ���󱻽з��һ�
    #10:����æ ԭʼ�ӿ�outcallfailcode:3
    #12:��Ӧ��  ԭʼ�ӿ�outcallfailcode:10
    #13:�û����ɴ� ԭʼ�ӿ�outcallfailcode:13
    #14:�û������� ԭʼ�ӿ�outcallfailcode:14
    #26:���з���  ԭʼ�ӿ�outcallfailcode:26
    #99:δ֪����  ԭʼ�ӿ�outcallfailcode:70
        """
        #@TODO δ����ͨ��״̬�����з��һ������з��һ�������ͨ��״̬�����з��һ������з��һ���ô�ж�
        #���гɹ����������������:
        # 0: δ֪�������
        # 1: ����
        # 2:�ڲ�����
        # 6:webcall����
        # 7:���������������� ��iscustomrelease=1��ʾ���û����йһ�,iscustomrelease=0��ʾ���йһ�
        if(cc_calldetail.callresult==1 and cc_calldetail.calltype in (0,1,2,6,7)):
            if(cc_calldetail.iscustomrelease==1):self.finish_reason=1
            else:self.finish_reason=2
        elif(cc_calldetail.callresult==1):#���гɹ��������������
            if(cc_calldetail.iscustomrelease==1):self.finish_reason=2
            else:self.finish_reason=1
        #���ʧ�ܣ��ж����ʧ�ܵ�ԭ��
        elif(cc_calldetail.callresult==0):#����ʧ�ܣ�
            if(cc_calldetail.outcallfailcode==3):self.finish_reason=10
            elif(cc_calldetail.outcallfailcode==10):self.finish_reason=12
            elif(cc_calldetail.outcallfailcode==70):self.finish_reason=99
            elif(cc_calldetail.outcallfailcode<>None):self.finish_reason=cc_calldetail.outcallfailcode
            else:self.finish_reason=99
        else:self.finish_reason=99
class dm_call_log_01(dm_call_log,Base):
     __tablename__ = 'dm_call_log_01'
class dm_call_log_02(dm_call_log,Base):
     __tablename__ = 'dm_call_log_02'
class dm_call_log_03(dm_call_log,Base):
     __tablename__ = 'dm_call_log_03'
class dm_call_log_04(dm_call_log,Base):
    __tablename__ = 'dm_call_log_04'
class dm_call_log_05(dm_call_log,Base):
    __tablename__ = 'dm_call_log_05'
class dm_call_log_06(dm_call_log,Base):
    __tablename__ = 'dm_call_log_06'
class dm_call_log_07(dm_call_log,Base):
    __tablename__ = 'dm_call_log_07'
class dm_call_log_08(dm_call_log,Base):
    __tablename__ = 'dm_call_log_08'
class dm_call_log_09(dm_call_log,Base):
    __tablename__ = 'dm_call_log_09'
class dm_call_log_10(dm_call_log,Base):
    __tablename__ = 'dm_call_log_10'
class dm_call_log_11(dm_call_log,Base):
    __tablename__ = 'dm_call_log_11'
class dm_call_log_12(dm_call_log,Base):
    __tablename__ = 'dm_call_log_12'
def get_nbr(orial_nbr):
    """��ȡ������ж�"""
    length=len(orial_nbr)
    resultNbr=orial_nbr
    if length in (14,15) and orial_nbr.startswith('0') and orial_nbr[-11]=='1':
        resultNbr=orial_nbr[-11:]
    return resultNbr
def get_dm_call_log(cc_calldetail):
    callday=cc_calldetail.strcallday#2012.01.02
    month=callday[5:7]#01
    call_log=None
    if(month=='01'): call_log=dm_call_log_01()
    elif(month=='02'): call_log=dm_call_log_02()
    elif(month=='03'): call_log=dm_call_log_03()
    elif(month=='04'): call_log=dm_call_log_04()
    elif(month=='05'): call_log=dm_call_log_05()
    elif(month=='06'): call_log=dm_call_log_06()
    elif(month=='07'): call_log=dm_call_log_07()
    elif(month=='08'): call_log=dm_call_log_08()
    elif(month=='09'): call_log=dm_call_log_09()
    elif(month=='10'): call_log=dm_call_log_10()
    elif(month=='11'): call_log=dm_call_log_11()
    elif(month=='12'): call_log=dm_call_log_12()
    if(call_log<>None):
        call_log.call_id=cc_calldetail.connectionid
        call_log.node_id=str(cc_calldetail.vcid)
        call_log.set_call_type(cc_calldetail)
        call_log.set_finish_reason(cc_calldetail)
        call_log.charge_flag='2'
        call_log.primary_caller=cc_calldetail.fakecalling
        call_log.primary_callee=cc_calldetail.oricallednumber
        if(cc_calldetail.calltype==3):#�˹���ϯ�����α������дΪ����
            call_log.caller=cc_calldetail.fakecalling
            call_log.primary_caller=cc_calldetail.callingnumber
        else:
            call_log.caller=cc_calldetail.callingnumber
        call_log.caller=get_nbr(call_log.caller)#�غ���
        call_log.callee=cc_calldetail.callednumber
        call_log.callee=get_nbr(call_log.callee)#�غ���
        call_log.start_time=cc_calldetail.callstarttime
        call_log.dial_time=cc_calldetail.ringingstarttime
        call_log.answer_time=cc_calldetail.answertime
        call_log.offhook_time=cc_calldetail.answertime
        call_log.hangup_time=cc_calldetail.callendtime
        call_log.finish_time=cc_calldetail.callendtime
        call_log.caller_user_type=cc_calldetail.customtype
        #ʱ��Ϊ�յģ�Ĭ�����ó�1970-01-01 08:00:00
        if(call_log.finish_time==None): call_log.finish_time=defaulttime
        if(call_log.start_time==None): call_log.start_time=defaulttime
        if(call_log.dial_time==None): call_log.dial_time=defaulttime
        if(call_log.answer_time==None): call_log.answer_time=defaulttime
        if(call_log.offhook_time==None): call_log.offhook_time=defaulttime
        if(call_log.hangup_time==None): call_log.hangup_time=defaulttime
    return call_log
if __name__ == '__main__':
    engine = create_engine('oracle+cx_oracle://eccdm:eccdm@ecc10000')
    Session = sessionmaker(bind=engine)
    session = Session()
    dmCallLogList=session.query(dm_call_log_08).all()
    print dmCallLogList
    if len(dmCallLogList)>0:
        print dmCallLogList[0].call_id
    session.close()
