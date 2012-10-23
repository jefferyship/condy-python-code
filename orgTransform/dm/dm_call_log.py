# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_call_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_call_log_xx相关表
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class dm_call_log(object):
    call_id=Column(String(32),primary_key=True)
    node_id=Column(String(32))
    call_type=Column(Float)
    charge_flag=Column(Float)
    #呼叫结束原因:
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
        """设置外呼类型
    #呼叫类型:
    # 1:人工话务座席呼叫外线
    # 2:人工话务座席呼叫IVR
    # 3:人工话务座席呼叫人工话务座席
    # 4:IVR呼叫外线
    # 5:IVR呼叫IVR
    # 6:IVR呼叫人工话务座席
    # 7:外线呼叫IVR
    # 8:外线呼叫人工话务台席
    # 9:外线呼入转呼出
    # 10:其它
        """
        if(cc_calldetail.calltype==1):self.call_type=7#呼入
        if(cc_calldetail.calltype==2):self.call_type=3#内部呼叫
        if(cc_calldetail.calltype==3):self.call_type=1#人工外呼
        if(cc_calldetail.calltype==4):self.call_type=4#自动外呼
        if(cc_calldetail.calltype==5):self.call_type=4#自动外呼转人工,TODO 暂时不清楚对于关系，先认为是自动外呼
        if(cc_calldetail.calltype==6):self.call_type=10#webcall呼入
        if(cc_calldetail.calltype==7):self.call_type=7#其他呼叫中兴溢入呼叫
    def set_finish_reason(self,cc_calldetail):
        """设置呼叫结束原因需要做转义
    #1:呼叫进入通话后主叫方挂机
    #2:呼叫进入通话后被叫方挂机
    #10:被叫忙 原始接口outcallfailcode:3
    #12:无应答  原始接口outcallfailcode:10
    #13:用户不可达 原始接口outcallfailcode:13
    #14:用户不存在 原始接口outcallfailcode:14
    #26:主叫放弃  原始接口outcallfailcode:26
    #99:未知错误  原始接口outcallfailcode:70
        """
        #@TODO 未进入通话状态，主叫方挂机，被叫方挂机，进入通话状态，主叫方挂机，被叫方挂机怎么判断
        #呼叫成功，并且外呼类型是:
        # 0: 未知外呼类型
        # 1: 呼入
        # 2:内部呼叫
        # 6:webcall呼入
        # 7:其他呼入中心溢入 的iscustomrelease=1表示是用户主叫挂机,iscustomrelease=0表示被叫挂机
        if(cc_calldetail.callresult==1 and cc_calldetail.calltype in (0,1,2,6,7)):
            if(cc_calldetail.iscustomrelease==1):self.finish_reason=1
            else:self.finish_reason=2
        elif(cc_calldetail.callresult==1):#呼叫成功，但可能是外呼
            if(cc_calldetail.iscustomrelease==1):self.finish_reason=2
            else:self.finish_reason=1
        #外呼失败，判断外呼失败的原因
        elif(cc_calldetail.callresult==0):#呼叫失败，
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
    """截取号码的判断"""
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
        if(cc_calldetail.calltype==3):#人工坐席外呼，伪主叫是写为主叫
            call_log.caller=cc_calldetail.fakecalling
            call_log.primary_caller=cc_calldetail.callingnumber
        else:
            call_log.caller=cc_calldetail.callingnumber
        call_log.caller=get_nbr(call_log.caller)#截号码
        call_log.callee=cc_calldetail.callednumber
        call_log.callee=get_nbr(call_log.callee)#截号码
        call_log.start_time=cc_calldetail.callstarttime
        call_log.dial_time=cc_calldetail.ringingstarttime
        call_log.answer_time=cc_calldetail.answertime
        call_log.offhook_time=cc_calldetail.answertime
        call_log.hangup_time=cc_calldetail.callendtime
        call_log.finish_time=cc_calldetail.callendtime
        call_log.caller_user_type=cc_calldetail.customtype
        #时间为空的，默认配置成1970-01-01 08:00:00
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
