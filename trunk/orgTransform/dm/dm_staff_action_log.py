# -*- coding:GBK-*-
#========================================================================
#   FileName: dm_staff_action_log.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_staff_action_log相关表
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class dm_staff_action_log(Base):
    __tablename__ = 'dm_staff_action_log'
    staff_id=Column(String(32),primary_key=True)
    action_id=Column(Float)
    start_time=Column(DateTime,primary_key=True)
    end_time=Column(DateTime)
    description=Column(String(256))
    check_action=Column(String(2))
    node_id=Column(String(32))
def get_dm_staff_action_log(cc_agentonbusystat):
    staff_action_log=dm_staff_action_log()
    staff_action_log.staff_id=cc_agentonbusystat.agent_id
    staff_action_log.action_id=cc_agentonbusystat.oper_type#0:迁入 1:示忙
    staff_action_log.start_time=cc_agentonbusystat.begin_time
    staff_action_log.end_time=cc_agentonbusystat.end_time
    staff_action_log.description=''
    staff_action_log.node_id=str(cc_agentonbusystat.vcid)
    return staff_action_log 
