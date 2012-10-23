# -*- coding:GBK-*-
#========================================================================
#   FileName: cc_logonoffdetail.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 中兴的cc_logonoffdetail表对应的类,签入、迁出对应表
# LastChange: 2012-08-18 20:08:03
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Integer, String, create_engine,DateTime
Base = declarative_base()
class cc_logonoffdetail(Base):
    __tablename__ = 'cc_logonoffdetail'
    agentid=Column(String(10),primary_key=True)
    vcid=Column(Integer)
    agentphone=Column(String(32))
    opertype=Column(Integer)
    begintime=Column(DateTime,primary_key=True)
    endtime=Column(DateTime)
    durtime=Column(Integer)
    strcallday=Column(String(10))
    endcause=Column(Integer)
    mem=Column(String(30))
    operlocalid=Column(Integer)
    ipaddress=Column(String(30))
    macaddress=Column(String(30))
    moduleno=Column(Integer)
    updatetime=Column(DateTime)
    srcagentid=Column(Integer)
