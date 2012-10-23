# -*- coding:GBK-*-
#========================================================================
#   FileName: cc_recorddetail.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 中兴的cc_recorddetail表对应的类
# LastChange: 2012-09-24 17:03:41
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Integer, String, create_engine,DateTime
Base = declarative_base()
class cc_recorddetail(Base):
    __tablename__ = 'cc_recorddetail'
    connectionid=Column(String(40))
    keystr=Column(String(30),primary_key=True)
    vcid=Column(Integer)
    listenedflag=Column(Integer)
    checkedflag=Column(Integer)
    agentid=Column(Integer)
    agentphone=Column(String(32))
    callingnumber=Column(String(32))
    callednumber=Column(String(32))
    agentid1=Column(String(10))
    strcallday=Column(String(10))
    recordtype=Column(Integer)
    recordlocal=Column(Integer)
    servicekey=Column(Integer)
    recordstarttime=Column(DateTime)
    durtime=Column(Integer)
    recordpath=Column(String(255))
    skillid=Column(Integer)
    viprec=Column(Integer)
    oricalled=Column(String(20))
    accesscode=Column(String(20))
    calltype=Column(Integer)
    callendtype=Column(Integer)
    anstime=Column(DateTime)
    callendtime=Column(DateTime)
    nfsdevid=Column(Integer)
    nfsinitpath=Column(String(100))
    operlocalid=Column(Integer)
    calllocalid=Column(Integer)
    updatetime=Column(DateTime)
    groupid=Column(Integer)
    errcode=Column(Integer)
    def __repr__(self):
        return 'vcid:'+self.vicd+',connectionid:'+self.connectionid+',callingnumber'+self.callingnumber+',callednumber'+self.callednumber
