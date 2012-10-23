# -*- coding:utf-8-*-
#========================================================================
#   FileName: staff_on_duty_info.py
#     Author: linh
#      Email: linh@ecallcen.com
#   HomePage:  staff_on_duty_info相关表
# LastChange: 2012-09-04 16:11:23
#========================================================================
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column,\
                        Float, String ,DateTime,create_engine
from sqlalchemy.orm import sessionmaker
import datetime 
Base = declarative_base()
defaulttime=datetime.datetime.strptime('1970-01-01 08:00:00','%Y-%m-%d %H:%M:%S')#默认的日期格式
class staff_on_duty_info(Base):
    __tablename__ = 'eccuc.staff_on_duty_info'
    __table_args__ = {'quote': False}#如果对应其他用户的表访问，要加上这句话
    workday=Column(DateTime)
    on_duty_type=Column(String(4))
    staff_id=Column(String(60),primary_key=True)
    begin_time=Column(DateTime,primary_key=True)
    end_time=Column(DateTime)
    node_id=Column(String(30))
    machine_ip=Column(String(32))
    port=Column(String(32))
    skill_short=Column(String(500))
def get_staff_on_duty_info(cc_logonoffdetail):
    on_duty_info=staff_on_duty_info()
    on_duty_info.workday=datetime.datetime.strptime(cc_logonoffdetail.strcallday,'%Y.%m.%d')
    on_duty_info.on_duty_type='0'
    on_duty_info.staff_id=cc_logonoffdetail.agentid
    on_duty_info.begin_time=cc_logonoffdetail.begintime
    on_duty_info.end_time=cc_logonoffdetail.endtime
    on_duty_info.node_id=str(cc_logonoffdetail.vcid)
    on_duty_info.machine_ip=cc_logonoffdetail.ipaddress
    on_duty_info.port=cc_logonoffdetail.agentphone
    on_duty_info.skill_short=''
    return on_duty_info
