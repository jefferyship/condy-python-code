# -*- coding:utf-8-*-
#========================================================================
#   FileName: dm_term_call_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_term_call_log_xx相关表
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine,Integer
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class dm_term_call_log(object):
    call_id=Column(String(32),primary_key=True)#呼叫流水号
    call_seq=Column(Integer)#呼叫子序号
    node_id=Column(String(32))#CTI节点号
    term_id=Column(Float)#终端编号
    term_type=Column(Float)#终端类型
    staff_id=Column(String(32))#员工编号
    call_time=Column(DateTime)#呼叫时间
    direction=Column(Float)#呼叫方向 0:呼入，1：呼出
    join_mode=Column(Float)#接入方式
    prelink_time=Column(DateTime)#占用起始时间
    release_time=Column(DateTime)#占用结束时间
    iai_time=Column(DateTime)#通话起始时间
    acm_time=Column(DateTime)#通话应答时间
    ans_time=Column(DateTime)#通话摘机时间
    clr_time=Column(DateTime)#通话结束时间
    primary_caller=Column(String(32))#原始主叫号码
    primary_callee=Column(String(32))#原始被叫号码
    caller=Column(String(32))#主叫号码
    callee=Column(String(32))#被叫号码
    finish_reason=Column(Float)#结束原因
    call_type=Column(Float)#呼叫类型
    queue_start_time=Column(DateTime)#排队开始时间
    queue_finish_time=Column(DateTime)#排队结束时间
    acd_no=Column(Float)#技能组编号
    associate_merge_id=Column(String(32))#相关合并队列流水号
    caller_user_type=Column(Float)#主叫用户类型
    skilldomain=Column(Float)#技能域
    #affair_type=Column(String(32))#业务类型（10000号按键值）
    #customer_brand=Column(String(32))#客户品牌
    #customer_group=Column(String(32))#客户战略分群
    #tel_type=Column(String(32))#电话类型
    #collect_flag=Column(Float)#是否采集标志。0未采过，1正在采，2已采
    def set_call_type(self,cc_agentcalldetail):
        """呼叫类型的转换
        1 人工话务座席呼出（出）
        2 呼入人工话务座席引起的人工话务（入）
        3 座席互助转入的人工话务（入）
        4 自动转入的人工话务（入），福州话务只算外线量。
        5 会议转入的人工话务（入）
        6 监听引起的人工话务（入）
        7 强插引起的人工话务（入）
        8 辅助引起的人工话务（入）
        9 人工转入引起的人工话务(入)
        98 其他原因引起的呼入人工话务（入）
        99 其他原因引起的呼出人工话务（出）
        """
        if(cc_agentcalldetail.calltype==1):self.call_type=4#1为用户呼入（呼入）
        elif(cc_agentcalldetail.calltype==2):self.call_type=3#为转移话务（呼入）
        elif(cc_agentcalldetail.calltype==3):self.call_type=9#为内部呼入（呼入）
        elif(cc_agentcalldetail.calltype==4):self.call_type=6#为拦截话务
        elif(cc_agentcalldetail.calltype==5):self.call_type=7#为代答（目前实际没有这个类型）
        elif(cc_agentcalldetail.calltype==6):self.call_type=1#为外部呼出（呼出）
        elif(cc_agentcalldetail.calltype==7):self.call_type=99#为内部呼出（呼出）
        elif(cc_agentcalldetail.calltype==8):self.call_type=6#为监听
        elif(cc_agentcalldetail.calltype==9):self.call_type=7#为插话
        else:self.call_type=97#不清楚的呼叫类型
    def set_finish_reason(self,cc_agentcalldetail):
        """结束原因
        1 呼叫进入通话后本端挂机(振铃后)
        2 呼叫进入通话后对端挂机(振铃后)
        3 通话中异常结束（系统检测到错误后引起的挂机）
        4 呼叫通话建立过程中本端主动挂机(已经到达对端，但还未进入通话)
        5 呼叫通话建立过程中对端拒绝应答(已经到达对端，但还未进入通话)
        6 呼叫通话建立过程中对方超时未应答（与系统设置的超时时限相关，超时的情况下挂机的一方可能是本端也可能是被叫[交换机代挂机]）
        7 呼叫通话建立过程中异常结束(系统检测到错误后引起的挂机)
        8 对端为空号(没有到达对方)
        9 路由失败(没有到达对方)
        10 对端忙(没有达到对方)
        11 用户忙(呼叫外线时)
        99 其他原因
        """
        if(cc_agentcalldetail.callendtype ==1):#是用户挂机
            self.finish_reason=2
        elif(cc_agentcalldetail.callendtype ==2):#客代挂机
            self.finish_reason=1
        elif(cc_agentcalldetail.callendtype ==3):#转移话务
            self.finish_reason=99
        elif(cc_agentcalldetail.callendtype ==4):#转接语音
            self.finish_reason=1
        elif(cc_agentcalldetail.callendtype ==5):#拦截话务
            self.finish_reason=99
        elif(cc_agentcalldetail.callendtype ==6):#代答
            self.finish_reason=99
        elif(cc_agentcalldetail.calltype in (1,2,3) and cc_agentcalldetail.callendtype ==7):#呼入时的话务员拒绝接听
            self.finish_reason=4
        elif(cc_agentcalldetail.calltype in (6,7) and cc_agentcalldetail.callendtype ==7):#呼出时的用户拒绝接听
            self.finish_reason=5
        elif(cc_agentcalldetail.callendtype ==8):#超时未应答
            self.finish_reason=6
        elif(cc_agentcalldetail.callendtype ==10):#超时未应答
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
def get_dm_term_call_log(cc_agentcalldetail):
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
        term_call_log.call_seq=cc_agentcalldetail.callid
        term_call_log.node_id='1'
        term_call_log.term_id=1
        term_call_log.term_type=1
        term_call_log.staff_id=cc_agentcalldetail.agentid
        term_call_log.set_call_type(cc_agentcalldetail)

        if (cc_agentcalldetail.calltype in (1,2,3)): term_call_log.direction=0 #1为用户呼入（呼入）2为转移话务（呼入）3为内部呼入（呼入）
        elif (cc_agentcalldetail.calltype in (6,7)): term_call_log.direction=1 #为外部呼出（呼出）为内部呼出（呼出）
        else:term_call_log.direction=None #否则就配置为0

        term_call_log.join_mode=1
        term_call_log.prelink_time=cc_agentcalldetail.ringingstarttime
        term_call_log.release_time=cc_agentcalldetail.answertime
        term_call_log.iai_time=cc_agentcalldetail.answertime
        term_call_log.acm_time=cc_agentcalldetail.answertime
        term_call_log.ans_time=cc_agentcalldetail.answertime
        term_call_log.clr_time=cc_agentcalldetail.callendtime
        term_call_log.call_time=cc_agentcalldetail.begincalltime
        if(term_call_log.prelink_time==None):term_call_log.prelink_time=defaulttime
        if(term_call_log.release_time==None):term_call_log.release_time=defaulttime
        if(term_call_log.iai_time==None):term_call_log.iai_time=defaulttime
        if(term_call_log.acm_time==None):term_call_log.acm_time=defaulttime
        if(term_call_log.ans_time==None):term_call_log.ans_time=defaulttime
        if(term_call_log.clr_time==None):term_call_log.clr_time=defaulttime

        term_call_log.primary_caller=None #cc_agentcalldetail找不到原始主叫和被叫，TODO 估计要到cc_calldetail表中寻找
        term_call_log.primary_callee=None #cc_agentcalldetail找不到原始主叫和被叫，TODO 估计要到cc_calldetail表中寻找
        term_call_log.caller=cc_agentcalldetail.callingnumber
        term_call_log.callee=cc_agentcalldetail.callednumber
        if(len(term_call_log.caller)==15 and term_call_log.caller.startswith('059')):
            term_call_log.caller=term_call_log.caller[4:]
        if(len(term_call_log.callee)==15 and term_call_log.callee.startswith('059')):
            term_call_log.callee=term_call_log.callee[4:]
        term_call_log.set_finish_reason(cc_agentcalldetail)
        term_call_log.queue_start_time=cc_agentcalldetail.queuebegintime
        term_call_log.queue_finish_time=cc_agentcalldetail.queueendtime
        term_call_log.acd_no=cc_agentcalldetail.skillid
        term_call_log.associate_merge_id=None
        term_call_log.caller_user_type=None
        term_call_log.skilldomain=cc_agentcalldetail.vcid
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
