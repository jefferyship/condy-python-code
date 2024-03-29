﻿------------------------------------------
-- Export file for user ECCUC           --
-- Created by 林桦 on 2011/1/18, 17:11:25 --
------------------------------------------

spool temp.log

prompt
prompt Creating table MONITOR_PT_FILE_INFO
prompt ===================================
prompt
create table MONITOR_PT_FILE_INFO
(
  MONITOR_NAME   VARCHAR2(32),
  FILE_PATH      VARCHAR2(128),
  KEYS           VARCHAR2(512),
  WARN_LIMIT     INTEGER,
  MONITOR_LINES  INTEGER,
  TIME_PATTERN   VARCHAR2(32),
  REMARK         VARCHAR2(512),
  ORDER_NUM      INTEGER,
  WARNING_SMS_ID VARCHAR2(32),
  LOG_TYPE			 VARCHAR2(32)
)
;
comment on table MONITOR_PT_FILE_INFO
  is '平台监控配置表';
comment on column MONITOR_PT_FILE_INFO.MONITOR_NAME
  is '平台名称';
comment on column MONITOR_PT_FILE_INFO.FILE_PATH
  is '监控日志地址.如果含有$mmddhh24mi$表示是宏变量';
comment on column MONITOR_PT_FILE_INFO.KEYS
  is '监控的关键字,多个关键字用||分隔';
comment on column MONITOR_PT_FILE_INFO.WARN_LIMIT
  is '告警阀值';
comment on column MONITOR_PT_FILE_INFO.MONITOR_LINES
  is '日志监控行数';
comment on column MONITOR_PT_FILE_INFO.TIME_PATTERN
  is '日期格式：mmddhh24mi表示FILE_PATH的相应宏变量会替换';
comment on column MONITOR_PT_FILE_INFO.REMARK
  is '备注';
comment on column MONITOR_PT_FILE_INFO.ORDER_NUM
  is '排序';
comment on column MONITOR_PT_FILE_INFO.WARNING_SMS_ID
  is '短信告警联系人ID';
comment on column MONITOR_PT_FILE_INFO.LOG_TYPE
  is '日志类型:websphere,svcsmgr,ctserver等';

prompt
prompt Creating table MONITOR_PT_HARDSPACE_LOG
prompt =======================================
prompt
create table MONITOR_PT_HARDSPACE_LOG
(
  MONITOR_NAME    VARCHAR2(32),
  HARDSPACE_NAME  VARCHAR2(64),
  TOTAL_HARDSPACE VARCHAR2(32),
  USED_HARDSPACE  VARCHAR2(32),
  AVI_HARDSPACE   VARCHAR2(32),
  AVI_PERCENT     VARCHAR2(32),
  DIRECT_NAME     VARCHAR2(64),
  INSERT_TIME     DATE default sysdate,
  UPDATE_TIME     DATE default sysdate not null
)
;
comment on table MONITOR_PT_HARDSPACE_LOG
  is '监控写硬盘空间日志表';
comment on column MONITOR_PT_HARDSPACE_LOG.MONITOR_NAME
  is '机器名称';
comment on column MONITOR_PT_HARDSPACE_LOG.HARDSPACE_NAME
  is '硬盘名称';
comment on column MONITOR_PT_HARDSPACE_LOG.TOTAL_HARDSPACE
  is '总容量(KB)';
comment on column MONITOR_PT_HARDSPACE_LOG.USED_HARDSPACE
  is '已使用容量(KB)';
comment on column MONITOR_PT_HARDSPACE_LOG.AVI_HARDSPACE
  is '可用容量(KB)';
comment on column MONITOR_PT_HARDSPACE_LOG.AVI_PERCENT
  is '可用百分比';
comment on column MONITOR_PT_HARDSPACE_LOG.DIRECT_NAME
  is '挂载点 名称';
comment on column MONITOR_PT_HARDSPACE_LOG.INSERT_TIME
  is '插入时间';
comment on column MONITOR_PT_HARDSPACE_LOG.UPDATE_TIME
  is '更新时间';
alter table MONITOR_PT_HARDSPACE_LOG
  add constraint PRI_PT_HARDSPACE_LOG unique (MONITOR_NAME, HARDSPACE_NAME);

prompt
prompt Creating table MONITOR_PT_MACHINE_NAME
prompt ======================================
prompt
create table MONITOR_PT_MACHINE_NAME
(
  MONITOR_NAME   VARCHAR2(32) not null,
  IP_ADDRESS     VARCHAR2(64),
  REMARK         VARCHAR2(64),
  WARNING_SMS_ID VARCHAR2(32)
)
;
comment on table MONITOR_PT_MACHINE_NAME
  is '平台监控机器名配置表';
comment on column MONITOR_PT_MACHINE_NAME.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_MACHINE_NAME.IP_ADDRESS
  is 'IP地址';
comment on column MONITOR_PT_MACHINE_NAME.REMARK
  is '备注';
comment on column MONITOR_PT_MACHINE_NAME.WARNING_SMS_ID
  is '告警联系人ID(表monitor_pt_warning_person)';
alter table MONITOR_PT_MACHINE_NAME
  add constraint PRI_PT_MACHINE_NAME primary key (MONITOR_NAME);

prompt
prompt Creating table MONITOR_PT_PROC_INFO
prompt ===================================
prompt
create table MONITOR_PT_PROC_INFO
(
  MONITOR_NAME   VARCHAR2(32),
  PROC_NAME      VARCHAR2(32),
  PROC_CPU_LIMIT VARCHAR2(32)
)
;
comment on table MONITOR_PT_PROC_INFO
  is '线程告警信息配置表，一个机器可以配置多个线程';
comment on column MONITOR_PT_PROC_INFO.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_PROC_INFO.PROC_NAME
  is '线程名称';
comment on column MONITOR_PT_PROC_INFO.PROC_CPU_LIMIT
  is 'CPU使用情况的告警阀值例如40表示，cpu使用达到40%告警.';

prompt
prompt Creating table MONITOR_PT_PROC_LOG
prompt ==================================
prompt
create table MONITOR_PT_PROC_LOG
(
  MONITOR_NAME VARCHAR2(32),
  PROC_NAME    VARCHAR2(32),
  USED_CPU     VARCHAR2(32),
  USED_MEMERY  VARCHAR2(32),
  PROC_ID      VARCHAR2(32),
  INSERT_TIME  DATE default sysdate not null
)
;
comment on table MONITOR_PT_PROC_LOG
  is '根据线程日志写的信息收集日志表';
comment on column MONITOR_PT_PROC_LOG.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_PROC_LOG.PROC_NAME
  is '线程名';
comment on column MONITOR_PT_PROC_LOG.USED_CPU
  is '使用CPU百分比';
comment on column MONITOR_PT_PROC_LOG.USED_MEMERY
  is '使用内存百分比';
comment on column MONITOR_PT_PROC_LOG.PROC_ID
  is '线程ID';
comment on column MONITOR_PT_PROC_LOG.INSERT_TIME
  is '插入时间';

prompt
prompt Creating table MONITOR_PT_SYSTEM_INFO
prompt =====================================
prompt
create table MONITOR_PT_SYSTEM_INFO
(
  MONITOR_NAME     VARCHAR2(32),
  CPU_IDLE_LIMIT   VARCHAR2(32),
  MEMORY_AVI_LIMIT VARCHAR2(32),
  HARDSPACE_NAME   VARCHAR2(64),
  HARDSPACE_LIMIT  VARCHAR2(32)
)
;
comment on table MONITOR_PT_SYSTEM_INFO
  is '系统信息(CPU,内存，硬盘)告警信息配置表';
comment on column MONITOR_PT_SYSTEM_INFO.MONITOR_NAME
  is '监控机器名';
comment on column MONITOR_PT_SYSTEM_INFO.CPU_IDLE_LIMIT
  is 'CPU Idle告警阀值,百分比例如:10';
comment on column MONITOR_PT_SYSTEM_INFO.MEMORY_AVI_LIMIT
  is '可以物理内存告警阀值.KB为单位例如:2048';
comment on column MONITOR_PT_SYSTEM_INFO.HARDSPACE_NAME
  is '监控的硬盘空间名称';
comment on column MONITOR_PT_SYSTEM_INFO.HARDSPACE_LIMIT
  is '监控硬盘告警阀值,百分比例如:10';

prompt
prompt Creating table MONITOR_PT_SYSTEM_LOG
prompt ====================================
prompt
create table MONITOR_PT_SYSTEM_LOG
(
  MONITOR_NAME VARCHAR2(32),
  CPU_IDLE     VARCHAR2(32),
  TOTAL_PHYMEN VARCHAR2(32),
  AVI_PHYMEN   VARCHAR2(32),
  USED_PHYMEN  VARCHAR2(32),
  INSERT_TIME  DATE not null
)
;
comment on column MONITOR_PT_SYSTEM_LOG.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_SYSTEM_LOG.CPU_IDLE
  is 'CPU的Idle情况.';
comment on column MONITOR_PT_SYSTEM_LOG.TOTAL_PHYMEN
  is '总的物理内存(KB)';
comment on column MONITOR_PT_SYSTEM_LOG.AVI_PHYMEN
  is '可用内存(KB)';
comment on column MONITOR_PT_SYSTEM_LOG.USED_PHYMEN
  is '已使用内存(KB)';
comment on column MONITOR_PT_SYSTEM_LOG.INSERT_TIME
  is '插入时间';

prompt
prompt Creating table MONITOR_PT_WARNING_PERSON
prompt ========================================
prompt
create table MONITOR_PT_WARNING_PERSON
(
  WARNING_SMS_ID  VARCHAR2(32),
  CONTACT_PERSONS VARCHAR2(512)
)
;
comment on table MONITOR_PT_WARNING_PERSON
  is '平台监控告警联系人配置表';
comment on column MONITOR_PT_WARNING_PERSON.WARNING_SMS_ID
  is '与monitor_pt_machine表关联';
comment on column MONITOR_PT_WARNING_PERSON.CONTACT_PERSONS
  is '多个人之间以;号做分隔';


-- Create table
create table MONITOR_PT_NETSTAT_INFO
(
  MONITOR_NAME VARCHAR2(32),
  COMMAND      VARCHAR2(256),
  COUNT_LIMIT  VARCHAR2(8)
);
-- Add comments to the table 
comment on table MONITOR_PT_NETSTAT_INFO
  is 'netstat线程监控';
-- Add comments to the columns 
comment on column MONITOR_PT_NETSTAT_INFO.MONITOR_NAME
  is '监控机器名';
comment on column MONITOR_PT_NETSTAT_INFO.COMMAND
  is 'netstat的命令程序';
comment on column MONITOR_PT_NETSTAT_INFO.COUNT_LIMIT
  is 'netstat的告警阀值';


spool off

--删除服务参数解码
delete from soa_interface_decode where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除服务错误代码
delete from soa_interface_error_code where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除输出映射信息
delete from soa_output_mapping where s_output_id in (select s_output_id from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo')));
--删除输入映射信息
delete from soa_input_mapping where s_input_id in (select s_input_id from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo')));
--删除服务输出参数信息
delete from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除服务输入参数信息
delete from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除服务组合信息
delete from soa_interface_service where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除服务实现信息
delete from soa_service_info where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除接口输出参数信息
delete from soa_interface_output where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除接口输入参数信息
delete from soa_interface_input where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
--删除接口定义信息
delete from soa_interface_info where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config','Monitor_Warn_To_Person','savePtResourceInfo'));
commit;

set define off;
declare
V_APP_SOA_INTERFACE_ID_3562 Varchar2(10);
V_APP_SOA_INPUT_ID_18594 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18428 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18429 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18430 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18431 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18432 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18433 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18434 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18435 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18436 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18437 Varchar2(10);
V_APP_SOA_SERVICE_ID_3510 Varchar2(10);
V_APP_SOA_INPUT_ID_18595 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18438 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18439 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18440 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18441 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18442 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18443 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18444 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18445 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18446 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18447 Varchar2(10);
V_APP_SOA_INTERFACE_ID_3542 Varchar2(10);
V_APP_SOA_INPUT_ID_18574 Varchar2(10);
V_APP_SOA_INPUT_ID_18575 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18408 Varchar2(10);
V_APP_SOA_SERVICE_ID_3490 Varchar2(10);
V_APP_SOA_INPUT_ID_18576 Varchar2(10);
V_APP_SOA_INPUT_ID_18577 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18409 Varchar2(10);
V_APP_SOA_INTERFACE_ID_3563 Varchar2(10);
V_APP_SOA_INPUT_ID_18597 Varchar2(10);
V_APP_SOA_INPUT_ID_18596 Varchar2(10);
V_APP_SOA_INPUT_ID_18598 Varchar2(10);
V_APP_SOA_INPUT_ID_18599 Varchar2(10);
V_APP_SOA_INPUT_ID_18600 Varchar2(10);
V_APP_SOA_INPUT_ID_18601 Varchar2(10);
V_APP_SOA_INPUT_ID_18602 Varchar2(10);
V_APP_SOA_INPUT_ID_18603 Varchar2(10);
V_APP_SOA_INPUT_ID_18604 Varchar2(10);
V_APP_SOA_INPUT_ID_18605 Varchar2(10);
V_APP_SOA_INPUT_ID_18606 Varchar2(10);
V_APP_SOA_INPUT_ID_18607 Varchar2(10);
V_APP_SOA_INPUT_ID_18608 Varchar2(10);
V_APP_SOA_INPUT_ID_18609 Varchar2(10);
V_APP_SOA_INPUT_ID_18610 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18449 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18448 Varchar2(10);
V_APP_SOA_SERVICE_ID_3511 Varchar2(10);
V_APP_SOA_INPUT_ID_18612 Varchar2(10);
V_APP_SOA_INPUT_ID_18611 Varchar2(10);
V_APP_SOA_INPUT_ID_18613 Varchar2(10);
V_APP_SOA_INPUT_ID_18614 Varchar2(10);
V_APP_SOA_INPUT_ID_18615 Varchar2(10);
V_APP_SOA_INPUT_ID_18616 Varchar2(10);
V_APP_SOA_INPUT_ID_18617 Varchar2(10);
V_APP_SOA_INPUT_ID_18618 Varchar2(10);
V_APP_SOA_INPUT_ID_18619 Varchar2(10);
V_APP_SOA_INPUT_ID_18620 Varchar2(10);
V_APP_SOA_INPUT_ID_18621 Varchar2(10);
V_APP_SOA_INPUT_ID_18622 Varchar2(10);
V_APP_SOA_INPUT_ID_18623 Varchar2(10);
V_APP_SOA_INPUT_ID_18624 Varchar2(10);
V_APP_SOA_INPUT_ID_18625 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18450 Varchar2(10);
V_APP_SOA_OUTPUT_ID_18451 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3562 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18594 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18428 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18429 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18430 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18431 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18432 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18433 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18434 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18435 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18436 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18437 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3510 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18595 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18438 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18439 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18440 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18441 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18442 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18443 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18444 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18445 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18446 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18447 from dual;
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3542 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18574 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18575 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18408 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3490 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18576 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18577 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18409 from dual;
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3563 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18597 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18596 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18598 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18599 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18600 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18601 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18602 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18603 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18604 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18605 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18606 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18607 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18608 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18609 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18610 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18449 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18448 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3511 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18612 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18611 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18613 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18614 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18615 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18616 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18617 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18618 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18619 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18620 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18621 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18622 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18623 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18624 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_18625 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18450 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_18451 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3562,'Monitor_Pt_Config','平台监控模块，根据监控平台的名称，获取监控的配置信息.','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18594,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18428,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18429,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_18430,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_18431,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18432,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18433,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_18434,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_18435,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18436,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_INTERFACE_ID_3562);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18437,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3562);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3510,'0','Monitor_Pt_Config','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18595,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_SERVICE_ID_3510);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18594,V_APP_SOA_INPUT_ID_18595);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_18438,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_18439,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18440,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18441,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_18442,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_18443,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18444,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18445,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18446,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_SERVICE_ID_3510);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18447,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_SERVICE_ID_3510);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18430,V_APP_SOA_OUTPUT_ID_18438);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18431,V_APP_SOA_OUTPUT_ID_18439);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18432,V_APP_SOA_OUTPUT_ID_18440);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18433,V_APP_SOA_OUTPUT_ID_18441);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18434,V_APP_SOA_OUTPUT_ID_18442);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18435,V_APP_SOA_OUTPUT_ID_18443);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18436,V_APP_SOA_OUTPUT_ID_18444);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18437,V_APP_SOA_OUTPUT_ID_18445);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18428,V_APP_SOA_OUTPUT_ID_18446);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18429,V_APP_SOA_OUTPUT_ID_18447);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3562,V_APP_SOA_SERVICE_ID_3510);


--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3542,'Monitor_Warn_To_Person','平台监控模块，根据监控平台的ID，发送短信告警的内容','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18574,'MONITOR_NAME','string','500','N','','N','','Y','告警ID','','',V_APP_SOA_INTERFACE_ID_3542);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_18575,'WARNING_CONTENT','string','2000','N','','N','','Y','告警内容','','',V_APP_SOA_INTERFACE_ID_3542);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18408,'Flag','string','100','N','','N','','Y','成功标志.0表示成功。其他失败','','',V_APP_SOA_INTERFACE_ID_3542);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3490,'0','Monitor_Warn_To_Person','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18576,'MONITOR_NAME','string','500','N','','N','','Y','告警ID','','',V_APP_SOA_SERVICE_ID_3490);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_18577,'WARNING_CONTENT','string','2000','N','','N','','Y','告警内容','','',V_APP_SOA_SERVICE_ID_3490);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18574,V_APP_SOA_INPUT_ID_18576);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18575,V_APP_SOA_INPUT_ID_18577);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18409,'Flag','string','100','N','','N','','Y','成功标志.0表示成功。其他失败','','',V_APP_SOA_SERVICE_ID_3490);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18408,V_APP_SOA_OUTPUT_ID_18409);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3542,V_APP_SOA_SERVICE_ID_3490);


--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3563,'savePtResourceInfo','将平台监控程序收集的数据保存到数据库中。','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18597,'cpu_idle','string','100','N','2','N','table2','Y','cpu idle','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18596,'monitor_name','string','100','N','1','N','table1','Y','机器名称','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_18598,'total_phy_men','string','100','N','2','N','table2','Y','总物理内存','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_INPUT_ID_18599,'avi_phymen','string','100','N','2','N','table2','Y','可用物理内存','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_INPUT_ID_18600,'used_phymen','string','100','N','2','N','table2','Y','已用物理内存','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18601,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_18602,'pid','string','100','N','3','Y','table3','Y','线程ID','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_INPUT_ID_18603,'proc_used_cpu','string','100','N','3','Y','table3','Y','线程使用CPU情况','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_INPUT_ID_18604,'proc_used_memory','string','100','N','3','Y','table3','Y','线程使用内存情况','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_18605,'hardspace_name','string','100','N','4','Y','table4','Y','文件系统名称','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_18606,'total_hardspace','string','100','N','4','Y','table4','Y','总大小(KB)','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_INPUT_ID_18607,'used_hardspace','string','100','N','4','Y','table4','Y','已使用大小(KB)','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_INPUT_ID_18608,'avi_hardspace','string','100','N','4','Y','table4','Y','可用大小(KB)','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('5',V_APP_SOA_INPUT_ID_18609,'used_hard_space_percent','string','100','N','4','Y','table4','Y','可用大小(百分比)','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('6',V_APP_SOA_INPUT_ID_18610,'file_hand_up','string','100','N','4','Y','table4','Y','挂载点','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18449,'flagMsg','string','100','N','','N','','Y','标志说明','','',V_APP_SOA_INTERFACE_ID_3563);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18448,'flag','string','100','N','','N','','Y','0：成功，其他失败','','',V_APP_SOA_INTERFACE_ID_3563);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3511,'0','savePtResourceInfo','','ecc.iserv.warn.call.SavePtResourceInfo','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18612,'monitor_name','string','100','N','1','N','table1','Y','机器名称','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18611,'cpu_idle','string','100','N','2','N','table2','Y','cpu idle','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_18613,'total_phy_men','string','100','N','2','N','table2','Y','总物理内存','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_INPUT_ID_18614,'avi_phymen','string','100','N','2','N','table2','Y','可用物理内存','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_INPUT_ID_18615,'used_phymen','string','100','N','2','N','table2','Y','已用物理内存','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18616,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_18617,'pid','string','100','N','3','Y','table3','Y','线程ID','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_INPUT_ID_18618,'proc_used_cpu','string','100','N','3','Y','table3','Y','线程使用CPU情况','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_INPUT_ID_18619,'proc_used_memory','string','100','N','3','Y','table3','Y','线程使用内存情况','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_18620,'hardspace_name','string','100','N','4','Y','table4','Y','文件系统名称','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_18621,'total_hardspace','string','100','N','4','Y','table4','Y','总大小(KB)','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_INPUT_ID_18622,'used_hardspace','string','100','N','4','Y','table4','Y','已使用大小(KB)','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_INPUT_ID_18623,'avi_hardspace','string','100','N','4','Y','table4','Y','可用大小(KB)','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('5',V_APP_SOA_INPUT_ID_18624,'used_hard_space_percent','string','100','N','4','Y','table4','Y','可用大小(百分比)','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('6',V_APP_SOA_INPUT_ID_18625,'file_hand_up','string','100','N','4','Y','table4','Y','挂载点','','',V_APP_SOA_SERVICE_ID_3511);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18596,V_APP_SOA_INPUT_ID_18612);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18597,V_APP_SOA_INPUT_ID_18611);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18598,V_APP_SOA_INPUT_ID_18613);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18599,V_APP_SOA_INPUT_ID_18614);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18600,V_APP_SOA_INPUT_ID_18615);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18601,V_APP_SOA_INPUT_ID_18616);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18602,V_APP_SOA_INPUT_ID_18617);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18603,V_APP_SOA_INPUT_ID_18618);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18604,V_APP_SOA_INPUT_ID_18619);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18605,V_APP_SOA_INPUT_ID_18620);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18606,V_APP_SOA_INPUT_ID_18621);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18607,V_APP_SOA_INPUT_ID_18622);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18608,V_APP_SOA_INPUT_ID_18623);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18609,V_APP_SOA_INPUT_ID_18624);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_18610,V_APP_SOA_INPUT_ID_18625);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_18450,'flag','string','100','N','','N','','Y','0：成功，其他失败','','',V_APP_SOA_SERVICE_ID_3511);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_18451,'flagMsg','string','100','N','','N','','Y','标志说明','','',V_APP_SOA_SERVICE_ID_3511);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18448,V_APP_SOA_OUTPUT_ID_18450);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_18449,V_APP_SOA_OUTPUT_ID_18451);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3563,V_APP_SOA_SERVICE_ID_3511);


commit;
end;
/
set define on;


--删除服务参数解码
delete from soa_interface_decode where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_Pt_Config'));
--删除服务错误代码
delete from soa_interface_error_code where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_Pt_Config'));
--删除输出映射信息
delete from soa_output_mapping where s_output_id in (select s_output_id from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config')));
--删除输入映射信息
delete from soa_input_mapping where s_input_id in (select s_input_id from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config')));
--删除服务输出参数信息
delete from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务输入参数信息
delete from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务组合信息
delete from soa_interface_service where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务实现信息
delete from soa_service_info where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除接口输出参数信息
delete from soa_interface_output where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
--删除接口输入参数信息
delete from soa_interface_input where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
--删除接口定义信息
delete from soa_interface_info where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
commit;

set define off;
declare
V_APP_SOA_INTERFACE_ID_3362 Varchar2(10);
V_APP_SOA_INPUT_ID_20114 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19536 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19537 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19538 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19539 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19540 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19541 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19542 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19543 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19544 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19545 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19562 Varchar2(10);
V_APP_SOA_SERVICE_ID_3190 Varchar2(10);
V_APP_SOA_INPUT_ID_20115 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19547 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19548 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19549 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19550 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19551 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19552 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19553 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19554 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19555 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19546 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19563 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3362 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20114 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19536 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19537 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19538 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19539 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19540 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19541 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19542 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19543 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19544 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19545 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19562 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3190 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20115 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19547 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19548 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19549 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19550 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19551 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19552 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19553 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19554 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19555 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19546 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19563 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3362,'Monitor_Pt_Config','平台监控模块，根据监控平台的名称，获取监控的配置信息.','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20114,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19536,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19537,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19538,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19539,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19540,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19541,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19542,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19543,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19544,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19545,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3362);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19562,'log_type','string','100','N','1','Y','table1','Y','日志类型:websphere,svcsmgr,ctserver等','','',V_APP_SOA_INTERFACE_ID_3362);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3190,'0','Monitor_Pt_Config','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20115,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_SERVICE_ID_3190);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20114,V_APP_SOA_INPUT_ID_20115);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19547,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19548,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19549,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19550,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19551,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19552,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19553,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19554,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19555,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19546,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_SERVICE_ID_3190);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19563,'log_type','string','100','','1','','','Y','','','',V_APP_SOA_SERVICE_ID_3190);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19539,V_APP_SOA_OUTPUT_ID_19547);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19540,V_APP_SOA_OUTPUT_ID_19548);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19541,V_APP_SOA_OUTPUT_ID_19549);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19542,V_APP_SOA_OUTPUT_ID_19550);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19543,V_APP_SOA_OUTPUT_ID_19551);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19544,V_APP_SOA_OUTPUT_ID_19552);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19545,V_APP_SOA_OUTPUT_ID_19553);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19536,V_APP_SOA_OUTPUT_ID_19554);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19537,V_APP_SOA_OUTPUT_ID_19555);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19538,V_APP_SOA_OUTPUT_ID_19546);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19562,V_APP_SOA_OUTPUT_ID_19563);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3362,V_APP_SOA_SERVICE_ID_3190);


commit;
end;
/
set define on;


-- Create table
create table MONITOR_PT_BACKUP_INFO
(
  MONITOR_NAME     VARCHAR2(32),
  BACKUP_PATH      VARCHAR2(1024),
  FTP_IP           VARCHAR2(32),
  FTP_USER         VARCHAR2(32),
  FTP_PASSWORD     VARCHAR2(32),
  FTP_BACKUP_PATH  VARCHAR2(256),
  LAST_BACKUP_TIME DATE,
  NEXT_BACKUP_TIME DATE,
  BACKUP_CYCLE     INTEGER
);
-- Add comments to the table 
comment on table MONITOR_PT_BACKUP_INFO
  is '平台备份配置表';
-- Add comments to the columns 
comment on column MONITOR_PT_BACKUP_INFO.MONITOR_NAME
  is '监控平台名称';
comment on column MONITOR_PT_BACKUP_INFO.BACKUP_PATH
  is '需要备份的路径,多个路径已||做分隔符';
comment on column MONITOR_PT_BACKUP_INFO.FTP_IP
  is '备份FTP的IP地址';
comment on column MONITOR_PT_BACKUP_INFO.FTP_USER
  is '备份FTP的用户名';
comment on column MONITOR_PT_BACKUP_INFO.FTP_PASSWORD
  is '备份FTP的密码';
comment on column MONITOR_PT_BACKUP_INFO.FTP_BACKUP_PATH
  is '备份FTP的路径';
comment on column MONITOR_PT_BACKUP_INFO.LAST_BACKUP_TIME
  is '上次备份的时间';
comment on column MONITOR_PT_BACKUP_INFO.NEXT_BACKUP_TIME
  is '本次备份的时间';
comment on column MONITOR_PT_BACKUP_INFO.BACKUP_CYCLE
  is '备份周期,以天为单位';


--删除服务参数解码
delete from soa_interface_decode where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_pt_backup_file'));
--删除服务错误代码
delete from soa_interface_error_code where interface_id in(  select interface_name from soa_interface_info where interface_name in('Monitor_pt_backup_file'));
--删除输出映射信息
delete from soa_output_mapping where s_output_id in (select s_output_id from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file')));
--删除输入映射信息
delete from soa_input_mapping where s_input_id in (select s_input_id from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file')));
--删除服务输出参数信息
delete from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file'));
--删除服务输入参数信息
delete from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file'));
--删除服务组合信息
delete from soa_interface_service where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file'));
--删除服务实现信息
delete from soa_service_info where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_pt_backup_file'));
--删除接口输出参数信息
delete from soa_interface_output where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_pt_backup_file'));
--删除接口输入参数信息
delete from soa_interface_input where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_pt_backup_file'));
--删除接口定义信息
delete from soa_interface_info where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_pt_backup_file'));
commit;
set define off;
declare
V_APP_SOA_INTERFACE_ID_3823 Varchar2(10);
V_APP_SOA_INPUT_ID_19416 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19238 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19239 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19240 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19241 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19242 Varchar2(10);
V_APP_SOA_SERVICE_ID_3771 Varchar2(10);
V_APP_SOA_INPUT_ID_19417 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19243 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19244 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19245 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19246 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19247 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3823 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_19416 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19238 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19239 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19240 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19241 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19242 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3771 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_19417 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19243 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19244 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19245 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19246 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19247 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3823,'Monitor_pt_backup_file','monitor_pt_backup_info表','Y','','0','','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_19416,'monitor_name','string','500','N','','N','','Y','监控平台','','',V_APP_SOA_INTERFACE_ID_3823);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19238,'backup_path','string','100','N','','N','','Y','备份的路径，多个路径以||做分隔','','',V_APP_SOA_INTERFACE_ID_3823);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19239,'ftp_ip','string','100','N','','N','','Y','备份的FTP地址','','',V_APP_SOA_INTERFACE_ID_3823);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19240,'ftp_user','string','100','N','','N','','Y','FTP用户名','','',V_APP_SOA_INTERFACE_ID_3823);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19241,'ftp_password','string','100','N','','N','','Y','FTP的密码','','',V_APP_SOA_INTERFACE_ID_3823);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19242,'ftp_backup_path','string','100','N','','N','','Y','上传FTP的路径','','',V_APP_SOA_INTERFACE_ID_3823);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3771,'0','Monitor_pt_backup_file','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_19417,'monitor_name','string','500','N','','N','','Y','监控平台','','',V_APP_SOA_SERVICE_ID_3771);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_19416,V_APP_SOA_INPUT_ID_19417);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19243,'backup_path','string','100','N','','N','','Y','备份的路径，多个路径以||做分隔','','',V_APP_SOA_SERVICE_ID_3771);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19244,'ftp_ip','string','100','N','','N','','Y','备份的FTP地址','','',V_APP_SOA_SERVICE_ID_3771);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19245,'ftp_user','string','100','N','','N','','Y','FTP用户名','','',V_APP_SOA_SERVICE_ID_3771);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19246,'ftp_password','string','100','N','','N','','Y','FTP的密码','','',V_APP_SOA_SERVICE_ID_3771);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19247,'ftp_backup_path','string','100','N','','N','','Y','上传FTP的路径','','',V_APP_SOA_SERVICE_ID_3771);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19238,V_APP_SOA_OUTPUT_ID_19243);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19239,V_APP_SOA_OUTPUT_ID_19244);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19240,V_APP_SOA_OUTPUT_ID_19245);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19241,V_APP_SOA_OUTPUT_ID_19246);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19242,V_APP_SOA_OUTPUT_ID_19247);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3823,V_APP_SOA_SERVICE_ID_3771);


commit;
end;
/
set define on;

--删除服务参数解码
delete from soa_interface_decode where interface_id in(  select interface_id from soa_interface_info where interface_name in('Monitor_Pt_Config'));
--删除服务错误代码
delete from soa_interface_error_code where interface_id in(  select interface_id from soa_interface_info where interface_name in('Monitor_Pt_Config'));
--删除输出映射信息
delete from soa_output_mapping where s_output_id in (select s_output_id from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config')));
--删除输入映射信息
delete from soa_input_mapping where s_input_id in (select s_input_id from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config')));
--删除服务输出参数信息
delete from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务输入参数信息
delete from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务组合信息
delete from soa_interface_service where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_Pt_Config'));
--删除服务实现信息
delete from soa_service_info where service_id in(select service_id from soa_service_info where service_name in('Monitor_Pt_Config'));
--删除接口输出参数信息
delete from soa_interface_output where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
--删除接口输入参数信息
delete from soa_interface_input where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
--删除接口定义信息
delete from soa_interface_info where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_Pt_Config'));
commit;

set define off;
declare
V_APP_SOA_INTERFACE_ID_3722 Varchar2(10);
V_APP_SOA_INPUT_ID_19294 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19528 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19529 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19068 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19069 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19070 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19071 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19072 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19073 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19074 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19075 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19076 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19077 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19078 Varchar2(10);
V_APP_SOA_SERVICE_ID_3670 Varchar2(10);
V_APP_SOA_INPUT_ID_19295 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19079 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19080 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19081 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19082 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19083 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19084 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19085 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19086 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19087 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19088 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19089 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19530 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19531 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3722 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_19294 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19528 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19529 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19068 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19069 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19070 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19071 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19072 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19073 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19074 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19075 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19076 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19077 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19078 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3670 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_19295 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19079 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19080 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19081 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19082 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19083 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19084 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19085 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19086 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19087 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19088 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19089 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19530 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19531 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3722,'Monitor_Pt_Config','平台监控模块，根据监控平台的名称，获取监控的配置信息.','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_19294,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19528,'command','string','1000','N','4','Y','table4','Y','netstat执行命令','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19529,'count_limit','string','100','N','4','Y','table4','Y','连接告警阀值','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19068,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19069,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19070,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19071,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19072,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19073,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19074,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19075,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19076,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19077,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_INTERFACE_ID_3722);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19078,'log_type','string','100','N','1','Y','table1','Y','日志类型:websphere,svcsmgr,ctserver等','','',V_APP_SOA_INTERFACE_ID_3722);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3670,'0','Monitor_Pt_Config','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_19295,'MONITOR_NAME','string','500','N','','N','','Y','监控平台名称','','',V_APP_SOA_SERVICE_ID_3670);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_19294,V_APP_SOA_INPUT_ID_19295);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19079,'tailRowNum','string','100','N','1','Y','table1','Y','监控文件的行数','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19080,'cpu_idle_limit','string','100','N','2','N','table2','Y','CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19081,'memory_avi_limit','string','100','N','2','N','table2','Y','可用内存告警阀值(KB)','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19082,'hardspace_name','string','100','N','2','N','table2','Y','硬盘名称(例如/dev/sda3)','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_19083,'hardspace_limit','string','100','N','2','N','table2','Y','硬盘告警阀值','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19084,'proc_name','string','100','N','3','Y','table3','Y','线程名称','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19085,'proc_cpu_limit','string','100','N','3','Y','table3','Y','线程CPU告警阀值','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19086,'monitorFile','string','1000','N','1','Y','table1','Y','监控文件名路径','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19087,'keys','string','2000','N','1','Y','table1','Y','监控关键字，多个关键字之间按有逗号分隔','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_19088,'countMonitor','string','100','N','1','Y','table1','Y','告警阀值','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_19089,'log_type','string','100','','1','','','Y','','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19530,'command','string','1000','','4','','','Y','','','',V_APP_SOA_SERVICE_ID_3670);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_19531,'count_limit','string','100','','4','','','Y','','','',V_APP_SOA_SERVICE_ID_3670);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19071,V_APP_SOA_OUTPUT_ID_19079);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19072,V_APP_SOA_OUTPUT_ID_19080);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19073,V_APP_SOA_OUTPUT_ID_19081);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19074,V_APP_SOA_OUTPUT_ID_19082);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19075,V_APP_SOA_OUTPUT_ID_19083);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19076,V_APP_SOA_OUTPUT_ID_19084);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19077,V_APP_SOA_OUTPUT_ID_19085);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19068,V_APP_SOA_OUTPUT_ID_19086);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19069,V_APP_SOA_OUTPUT_ID_19087);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19070,V_APP_SOA_OUTPUT_ID_19088);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19078,V_APP_SOA_OUTPUT_ID_19089);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19528,V_APP_SOA_OUTPUT_ID_19530);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19529,V_APP_SOA_OUTPUT_ID_19531);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3722,V_APP_SOA_SERVICE_ID_3670);


commit;
end;
/
set define on;


alter table MONITOR_PT_MACHINE_NAME add PLAN_ID VARCHAR2(64);
-- Add comments to the columns 
comment on column MONITOR_PT_MACHINE_NAME.PLAN_ID
  is '计划ID(表warn_plan_info)';
  
set define off;
declare
V_APP_SOA_INTERFACE_ID_3523 Varchar2(10);
V_APP_SOA_INPUT_ID_20680 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20119 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20118 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20120 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20121 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20122 Varchar2(10);
V_APP_SOA_SERVICE_ID_3371 Varchar2(10);
V_APP_SOA_INPUT_ID_20681 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20124 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20123 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20125 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20126 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20127 Varchar2(10);
V_APP_SOA_INTERFACE_ID_3363 Varchar2(10);
V_APP_SOA_INPUT_ID_20116 Varchar2(10);
V_APP_SOA_INPUT_ID_20117 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19556 Varchar2(10);
V_APP_SOA_SERVICE_ID_3191 Varchar2(10);
V_APP_SOA_INPUT_ID_20118 Varchar2(10);
V_APP_SOA_INPUT_ID_20119 Varchar2(10);
V_APP_SOA_OUTPUT_ID_19557 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3523 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20680 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20119 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20118 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20120 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20121 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20122 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3371 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20681 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20124 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20123 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20125 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20126 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20127 from dual;
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3363 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20116 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20117 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19556 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3191 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20118 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20119 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_19557 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3523,'Monitor_machine_info','从monitor_pt_machine_name表获取告警的信息','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20680,'monitor_name','string','100','N','','N','','Y','告警的机器名','','',V_APP_SOA_INTERFACE_ID_3523);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_20119,'IP_ADDRESS','string','100','N','','N','','Y','IP地址','','',V_APP_SOA_INTERFACE_ID_3523);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20118,'monitor_name','string','100','N','','N','','Y','告警机器名','','',V_APP_SOA_INTERFACE_ID_3523);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_20120,'REMARK','string','100','N','','N','','Y','备注','','',V_APP_SOA_INTERFACE_ID_3523);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_20121,'WARNING_SMS_ID','string','100','N','','N','','Y','告警联系人ID(表monitor_pt_warning_person)','','',V_APP_SOA_INTERFACE_ID_3523);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_20122,'PLAN_ID','string','100','N','','N','','Y','计划ID(表warn_plan_info)','','',V_APP_SOA_INTERFACE_ID_3523);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3371,'0','Monitor_machine_info','','com.ecc.service.sql.QueryService','select monitor_name,ip_address,remark,warning_sms_id,plan_id from monitor_pt_machine_name where monitor_name=?','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20681,'monitor_name','string','100','N','','N','','Y','告警的机器名','','',V_APP_SOA_SERVICE_ID_3371);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20680,V_APP_SOA_INPUT_ID_20681);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20124,'monitor_name','string','100','N','','N','','Y','告警机器名','','',V_APP_SOA_SERVICE_ID_3371);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_OUTPUT_ID_20123,'IP_ADDRESS','string','100','N','','N','','Y','IP地址','','',V_APP_SOA_SERVICE_ID_3371);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_OUTPUT_ID_20125,'REMARK','string','100','N','','N','','Y','备注','','',V_APP_SOA_SERVICE_ID_3371);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('4',V_APP_SOA_OUTPUT_ID_20126,'WARNING_SMS_ID','string','100','N','','N','','Y','告警联系人ID(表monitor_pt_warning_person)','','',V_APP_SOA_SERVICE_ID_3371);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('5',V_APP_SOA_OUTPUT_ID_20127,'PLAN_ID','string','100','N','','N','','Y','计划ID(表warn_plan_info)','','',V_APP_SOA_SERVICE_ID_3371);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20118,V_APP_SOA_OUTPUT_ID_20124);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20119,V_APP_SOA_OUTPUT_ID_20123);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20120,V_APP_SOA_OUTPUT_ID_20125);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20121,V_APP_SOA_OUTPUT_ID_20126);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20122,V_APP_SOA_OUTPUT_ID_20127);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3523,V_APP_SOA_SERVICE_ID_3371);


--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3363,'Monitor_Warn_To_Person','平台监控模块，根据监控平台的ID，发送短信告警的内容','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20116,'MONITOR_NAME','string','500','N','','N','','Y','告警ID','','',V_APP_SOA_INTERFACE_ID_3363);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_20117,'WARNING_CONTENT','string','2000','N','','N','','Y','告警内容','','',V_APP_SOA_INTERFACE_ID_3363);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19556,'Flag','string','100','N','','N','','Y','成功标志.0表示成功。其他失败','','',V_APP_SOA_INTERFACE_ID_3363);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3191,'0','Monitor_Warn_To_Person','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20118,'MONITOR_NAME','string','500','N','','N','','Y','告警ID','','',V_APP_SOA_SERVICE_ID_3191);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_20119,'WARNING_CONTENT','string','2000','N','','N','','Y','告警内容','','',V_APP_SOA_SERVICE_ID_3191);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20116,V_APP_SOA_INPUT_ID_20118);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20117,V_APP_SOA_INPUT_ID_20119);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_19557,'Flag','string','100','N','','N','','Y','成功标志.0表示成功。其他失败','','',V_APP_SOA_SERVICE_ID_3191);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_19556,V_APP_SOA_OUTPUT_ID_19557);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3363,V_APP_SOA_SERVICE_ID_3191);


commit;
end;
/
set define on;


set define off;
declare
V_APP_SOA_INTERFACE_ID_3524 Varchar2(10);
V_APP_SOA_INPUT_ID_20682 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20128 Varchar2(10);
V_APP_SOA_SERVICE_ID_3372 Varchar2(10);
V_APP_SOA_INPUT_ID_20683 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20129 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3524 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20682 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20128 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3372 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20683 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20129 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3524,'Monitor_alive','写入服务，表示该server未死','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20682,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_INTERFACE_ID_3524);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20128,'result','string','100','N','','N','','Y','','','',V_APP_SOA_INTERFACE_ID_3524);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3372,'0','Monitor_alive','','com.ecc.service.sql.UpdateService','MERGE INTO monitor_pt_alive_log D
   USING (SELECT  monitor_name FROM monitor_pt_machine_name where monitor_name=? ) S
   ON (D.monitor_name = S.monitor_name)
   WHEN MATCHED THEN UPDATE SET D.alive_date = sysdate
   WHEN NOT MATCHED THEN INSERT (D.monitor_name, D.alive_date)
   VALUES (S.monitor_name, sysdate)','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20683,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_SERVICE_ID_3372);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20682,V_APP_SOA_INPUT_ID_20683);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20129,'result','string','100','N','','N','','Y','','','',V_APP_SOA_SERVICE_ID_3372);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20128,V_APP_SOA_OUTPUT_ID_20129);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3524,V_APP_SOA_SERVICE_ID_3372);


commit;
end;
/
set define on;

-- Create table
create table MONITOR_PT_ALIVE_LOG
(
  MONITOR_NAME VARCHAR2(32),
  ALIVE_DATE   DATE
);
-- Add comments to the table 
comment on table MONITOR_PT_ALIVE_LOG
  is '系统监控，机器是否存活标志表';
-- Add comments to the columns 
comment on column MONITOR_PT_ALIVE_LOG.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_ALIVE_LOG.ALIVE_DATE
  is '最新的存活时间';


set define off;
declare
V_APP_SOA_INTERFACE_ID_3522 Varchar2(10);
V_APP_SOA_INPUT_ID_20674 Varchar2(10);
V_APP_SOA_INPUT_ID_20675 Varchar2(10);
V_APP_SOA_INPUT_ID_20676 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20116 Varchar2(10);
V_APP_SOA_SERVICE_ID_3370 Varchar2(10);
V_APP_SOA_INPUT_ID_20677 Varchar2(10);
V_APP_SOA_INPUT_ID_20678 Varchar2(10);
V_APP_SOA_INPUT_ID_20679 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20117 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3522 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20674 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20675 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20676 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20116 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3370 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20677 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20678 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20679 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20117 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3522,'WarnToPerson','告警监控，在warn_plan_info表配置一个虚拟的计划，然后在monitor_pt_machine_name表的plan_id字段配置这虚拟计划所指定的告警联系人或者联系方式','Y','','0','告警监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20674,'plan_id','string','100','N','','N','','Y','计划ID，对应warn_plan_info表','','',V_APP_SOA_INTERFACE_ID_3522);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_20675,'warn_level','string','100','N','','N','','Y','告警级别，A,B,C等值','','',V_APP_SOA_INTERFACE_ID_3522);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('3',V_APP_SOA_INPUT_ID_20676,'warn_content','string','10000','N','','N','','Y','告警内容','','',V_APP_SOA_INTERFACE_ID_3522);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20116,'result','string','100','N','','N','','Y','0,成功，其他失败','','',V_APP_SOA_INTERFACE_ID_3522);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3370,'0','WarnToPerson','','ecc.iserv.warn.call.WarnToPersonImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20677,'plan_id','string','100','N','','N','','Y','计划ID，对应warn_plan_info表','','',V_APP_SOA_SERVICE_ID_3370);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_20678,'warn_level','string','100','N','','N','','Y','告警级别，A,B,C等值','','',V_APP_SOA_SERVICE_ID_3370);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('3',V_APP_SOA_INPUT_ID_20679,'warn_content','string','10000','N','','N','','Y','告警内容','','',V_APP_SOA_SERVICE_ID_3370);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20674,V_APP_SOA_INPUT_ID_20677);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20675,V_APP_SOA_INPUT_ID_20678);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20676,V_APP_SOA_INPUT_ID_20679);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20117,'result','string','100','N','','N','','Y','0,成功，其他失败','','',V_APP_SOA_SERVICE_ID_3370);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20116,V_APP_SOA_OUTPUT_ID_20117);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3522,V_APP_SOA_SERVICE_ID_3370);


commit;
end;
/
set define on;

-- Create table
create table MONITOR_PT_NOHUP_VERSION
(
  MONITOR_NAME VARCHAR2(32),
  VERSION_MSG  VARCHAR2(512),
  UPDATE_TIME  DATE
);
-- Add comments to the table 
comment on table MONITOR_PT_NOHUP_VERSION
  is '平台监控-获取程序的版本号';
-- Add comments to the columns 
comment on column MONITOR_PT_NOHUP_VERSION.MONITOR_NAME
  is '机器名';
comment on column MONITOR_PT_NOHUP_VERSION.VERSION_MSG
  is '版本信息';
comment on column MONITOR_PT_NOHUP_VERSION.UPDATE_TIME
  is '更新时间';

set define off;
declare
V_APP_SOA_INTERFACE_ID_4322 Varchar2(10);
V_APP_SOA_INPUT_ID_20394 Varchar2(10);
V_APP_SOA_INPUT_ID_20395 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20108 Varchar2(10);
V_APP_SOA_SERVICE_ID_4270 Varchar2(10);
V_APP_SOA_INPUT_ID_20396 Varchar2(10);
V_APP_SOA_INPUT_ID_20397 Varchar2(10);
V_APP_SOA_OUTPUT_ID_20109 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_4322 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20394 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20395 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20108 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_4270 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20396 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_20397 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_20109 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_4322,'Monitor_nohupVersion','从监控程序的nohup.out文件中读取程序的版本号，写入数据库中.','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_20394,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_INTERFACE_ID_4322);


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('2',V_APP_SOA_INPUT_ID_20395,'version_msg','string','1000','N','','N','','Y','版本信息','','',V_APP_SOA_INTERFACE_ID_4322);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20108,'result','string','100','N','','N','','Y','成功,失败标志','','',V_APP_SOA_INTERFACE_ID_4322);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_4270,'0','Monitor_nohupVersion','','com.ecc.service.sql.UpdateService','MERGE INTO monitor_pt_nohup_version D
   USING (SELECT  ? as monitor_name,? as version_msg FROM dual ) S
   ON (D.monitor_name = S.monitor_name)
   WHEN MATCHED THEN UPDATE SET D.update_time = sysdate,D.version_msg=S.version_msg
   WHEN NOT MATCHED THEN INSERT (D.monitor_name, D.update_time,version_msg)
   VALUES (S.monitor_name, sysdate,S.version_msg)','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_20396,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_SERVICE_ID_4270);


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('2',V_APP_SOA_INPUT_ID_20397,'version_msg','string','1000','N','','N','','Y','版本信息','','',V_APP_SOA_SERVICE_ID_4270);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20394,V_APP_SOA_INPUT_ID_20396);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_20395,V_APP_SOA_INPUT_ID_20397);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_20109,'result','string','100','N','','N','','Y','成功,失败标志','','',V_APP_SOA_SERVICE_ID_4270);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_20108,V_APP_SOA_OUTPUT_ID_20109);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_4322,V_APP_SOA_SERVICE_ID_4270);


commit;
end;
/
set define on;
alter table MONITOR_PT_NOHUP_VERSION
  add constraint pri_PT_NOHUP_VERSION primary key (MONITOR_NAME);


set define off;
declare
V_APP_SOA_INTERFACE_ID_3803 Varchar2(10);
V_APP_SOA_INPUT_ID_22296 Varchar2(10);
V_APP_SOA_OUTPUT_ID_22187 Varchar2(10);
V_APP_SOA_SERVICE_ID_3671 Varchar2(10);
V_APP_SOA_INPUT_ID_22297 Varchar2(10);
V_APP_SOA_OUTPUT_ID_22191 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3803 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_22296 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_22187 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3671 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_22297 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_22191 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3803,'Monitor_get_sysdate','获取数据库的时间','Y','','0','平台监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_22296,'monitor_name','string','100','N','','N','','Y','告警的机器名','','',V_APP_SOA_INTERFACE_ID_3803);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_22187,'oracleDateStr','string','100','N','','N','','Y','告警机器名','','',V_APP_SOA_INTERFACE_ID_3803);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3671,'0','Monitor_get_sysdate','','com.ecc.service.sql.QueryService','select to_char(sysdate,''yyyymmddhh24miss'') oracleDateStr from dual','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_22297,'monitor_name','string','100','N','','N','','Y','告警的机器名','','',V_APP_SOA_SERVICE_ID_3671);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_22296,V_APP_SOA_INPUT_ID_22297);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_22191,'oracleDateStr','string','100','N','','N','','Y','告警机器名','','',V_APP_SOA_SERVICE_ID_3671);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_22187,V_APP_SOA_OUTPUT_ID_22191);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3803,V_APP_SOA_SERVICE_ID_3671);


commit;
end;
/
set define on;


-- Create table
create table MONITOR_PT_TIME_NOSYC
(
  MONITOR_NAME VARCHAR2(32)
)

-- Add comments to the table 
comment on table MONITOR_PT_TIME_NOSYC
  is '监控系统不需要时间同步的服务器配置';
-- Add comments to the columns 
comment on column MONITOR_PT_TIME_NOSYC.MONITOR_NAME
  is '机器名';

--删除服务参数解码
delete from soa_interface_decode where interface_id in(  select interface_id from soa_interface_info where interface_name in('Monitor_get_sysdate'));
--删除服务错误代码
delete from soa_interface_error_code where interface_id in(  select interface_id from soa_interface_info where interface_name in('Monitor_get_sysdate'));
--删除输出映射信息
delete from soa_output_mapping where s_output_id in (select s_output_id from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_get_sysdate')));
--删除输入映射信息
delete from soa_input_mapping where s_input_id in (select s_input_id from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_get_sysdate')));
--删除服务输出参数信息
delete from soa_service_output where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_get_sysdate'));
--删除服务输入参数信息
delete from soa_service_input where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_get_sysdate'));
--删除服务组合信息
delete from soa_interface_service where service_id in(select s.service_id from soa_interface_info i,soa_interface_service s where i.interface_id=s.interface_id and i.interface_name in ('Monitor_get_sysdate'));
--删除服务实现信息
delete from soa_service_info where service_id in(select service_id from soa_service_info where service_name in('Monitor_pt_get_sysdate'));
--删除接口输出参数信息
delete from soa_interface_output where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_get_sysdate'));
--删除接口输入参数信息
delete from soa_interface_input where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_get_sysdate'));
--删除接口定义信息
delete from soa_interface_info where interface_id in(select interface_id from soa_interface_info where interface_name in ('Monitor_get_sysdate'));
commit;


set define off;
declare
V_APP_SOA_INTERFACE_ID_3919 Varchar2(10);
V_APP_SOA_INPUT_ID_22931 Varchar2(10);
V_APP_SOA_OUTPUT_ID_22845 Varchar2(10);
V_APP_SOA_SERVICE_ID_3788 Varchar2(10);
V_APP_SOA_INPUT_ID_22932 Varchar2(10);
V_APP_SOA_OUTPUT_ID_22846 Varchar2(10);
begin
select SEQ_SOA_INTERFACE.nextval into V_APP_SOA_INTERFACE_ID_3919 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_22931 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_22845 from dual;
select SEQ_SOA_SERVICE.nextval into V_APP_SOA_SERVICE_ID_3788 from dual;
select SEQ_SOA_INPUT.nextval into V_APP_SOA_INPUT_ID_22932 from dual;
select SEQ_SOA_OUTPUT.nextval into V_APP_SOA_OUTPUT_ID_22846 from dual;
--插入接口信息
insert into SOA_INTERFACE_INFO (INTERFACE_ID, INTERFACE_NAME, DESCRIPTION,IS_USED, IS_LOG, TYPE, MODULE_NAME, CALL_TYPE)
values (V_APP_SOA_INTERFACE_ID_3919,'Monitor_get_sysdate','获取数据库的时间','Y','','0','系统监控','0');


--插入接口输入信息
insert into SOA_INTERFACE_INPUT (COLUMN_INDEX, I_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_INPUT_ID_22931,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_INTERFACE_ID_3919);


--插入接口输出信息
insert into SOA_INTERFACE_OUTPUT (COLUMN_INDEX, I_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, INTERFACE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_22845,'oracleDateStr','string','100','N','','N','','Y','数据库时间:格式:yyyymmddhh24miss','','',V_APP_SOA_INTERFACE_ID_3919);


--插入服务信息
insert into SOA_SERVICE_INFO (SERVICE_ID, COMPANY_ID, SERVICE_NAME,SERVICE_ATTACH, SERVICE_CLASS, DATASOURCE,MODIFY_STAFF_ID, MODIFY_TIME)
values (V_APP_SOA_SERVICE_ID_3788,'0','Monitor_pt_get_sysdate','','com.telthink.link.service.CallFunctionImpl','','','');


--插入服务输入信息
insert into SOA_SERVICE_INPUT (COLUMN_INDEX, S_INPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_INPUT_ID_22932,'monitor_name','string','100','N','','N','','Y','机器名','','',V_APP_SOA_SERVICE_ID_3788);


--插入输入映射信息
insert into SOA_INPUT_MAPPING (I_INPUT_ID,S_INPUT_ID)
values (V_APP_SOA_INPUT_ID_22931,V_APP_SOA_INPUT_ID_22932);


--插入服务输出信息
insert into SOA_SERVICE_OUTPUT (COLUMN_INDEX, S_OUTPUT_ID, COLUMN_NAME,COLUMN_TYPE, COLUMN_LENGTH, NEED_DECODE,TABLE_INDEX, IS_MULTI, TABLE_NAME,IS_USED, COLUMN_DESC, MODIFY_STAFF_ID,MODIFY_TIME, SERVICE_ID)
values ('1',V_APP_SOA_OUTPUT_ID_22846,'oracleDateStr','string','100','N','','N','','Y','数据库时间:格式:yyyymmddhh24miss','','',V_APP_SOA_SERVICE_ID_3788);


--插入输出映射信息
insert into SOA_OUTPUT_MAPPING (I_OUTPUT_ID,S_OUTPUT_ID)
values (V_APP_SOA_OUTPUT_ID_22845,V_APP_SOA_OUTPUT_ID_22846);


--插入服务组合信息
insert into SOA_INTERFACE_SERVICE (ORDER_NO, INTERFACE_ID, SERVICE_ID)
values ('',V_APP_SOA_INTERFACE_ID_3919,V_APP_SOA_SERVICE_ID_3788);


commit;
end;
/
set define on;

