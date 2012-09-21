# -*- coding:utf-8-*-
#========================================================================
#   FileName: dm_queue_merge.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  dm_queue_merge.py相关表
# LastChange: 2012-08-18 21:02:57
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine,Integer
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class dm_queue_merge(Base):
    __tablename__ = 'dm_queue_merge'
    queue_id=Column(String(32),primary_key=True)
    call_id=Column(String(32))#呼叫流水号
    merge_id=Column(String(32))
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
