# -*- coding:GBK-*-
#========================================================================
#   FileName: cc_queuedetail.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 中兴的cc_queuedetail表对应的类
# LastChange: 2012-08-18 20:08:03
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Integer, String, create_engine,DateTime
Base = declarative_base()
class cc_queuedetail(Base):
    __tablename__ = 'cc_queuedetail'
    connectionid=Column(String(40),primary_key=True)
    vcid=Column(Integer)
    servicekey=Column(String(40))
    skillid=Column(Integer)
    customlevel=Column(Integer)
    callkind=Column(Integer)
    callingnumber=Column(String(32))
    nettype=Column(Integer)
    strcallday=Column(String(10))
    queuestarttime=Column(DateTime,primary_key=True)
    queueendtime=Column(DateTime)
    tqresult=Column(Integer)
    tqresultagentid=Column(String(10))
    tqresultnumber=Column(String(32))
    ringingstarttime=Column(DateTime)
    ringingendtime=Column(String(40))
    answered=Column(Integer)
    talkingtime=Column(Integer)
    acwtime=Column(Integer)
    queuelen=Column(Integer)
    updatetime=Column(DateTime)
    oriconnectionid=Column(String(40))
    callingc3fdevice=Column(String(40))
    calledc3fdevice=Column(String(40))
    orivcid=Column(Integer)
    oriskillid=Column(Integer)
    queuetype=Column(Integer)
    calllocalid=Column(Integer)
    timelength=Column(Integer)
    callednumber=Column(String(32))
    langid=Column(Integer)
    dimid1=Column(String(40))
    dimid2=Column(String(40))
    dimid3=Column(String(40))
    dimid4=Column(String(40))
    dimid5=Column(String(40))
    dimid6=Column(String(40))
    dimid7=Column(String(40))
    dimid8=Column(String(40))
    dimid9=Column(String(40))
    dimid10=Column(String(40))
    dimid11=Column(String(40))
    setagentid=Column(String(40))
    setagentflag=Column(String(40))
    isagtselcall=Column(String(40))
    def __repr__(self):
        return 'vcid:'+self.vicd+',connectionid:'+self.connectionid+',callingnumber'+self.callingnumber+',callednumber'+self.callednumber
