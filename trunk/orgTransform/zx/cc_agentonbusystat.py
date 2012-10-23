# -*- coding:GBK-*-
#========================================================================
#   FileName: cc_agentonbusystat.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage: 中兴的cc_agentonbusystat表对应的类,签入、迁出,示忙对应表
# LastChange: 2012-08-18 20:08:03
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Integer, String, create_engine,DateTime
Base = declarative_base()
class cc_agentonbusystat(Base):
    __tablename__ = 'cc_agentonbusystat'
    agent_oper_id=Column(String(20),primary_key=True)
    vcid=Column(Integer)
    agent_id=Column(String(20))
    oper_type=Column(Integer)
    begin_time=Column(DateTime)
    end_time=Column(DateTime)
    recid=Column(Integer)
    platformid=Column(Integer)
    busycause=Column(Integer)
    groupid=Column(Integer)
    updatetime=Column(DateTime)
