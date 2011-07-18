﻿prompt PL/SQL Developer import file
prompt Created on 2011年2月15日 by 林桦
set feedback off
set define off
prompt Disabling triggers for ECC_CODE_DICT...
alter table ECC_CODE_DICT disable all triggers;
prompt Loading ECC_CODE_DICT...
insert into ECC_CODE_DICT (CODE, VALUE, REMARK, GROUP_ID, MODULE, STS, COMPANY_ID, ORDER_NUM)
values ('version', '1.1.0.5', '平台监控程序的版本', 'PATCH', 'PT_MONITOR', 'A', '-1', null);
insert into ECC_CODE_DICT (CODE, VALUE, REMARK, GROUP_ID, MODULE, STS, COMPANY_ID, ORDER_NUM)
values ('ip', '134.128.196.10', '平台监控程序的补丁FTP的IP', 'PATCH', 'PT_MONITOR', 'A', '-1', null);
insert into ECC_CODE_DICT (CODE, VALUE, REMARK, GROUP_ID, MODULE, STS, COMPANY_ID, ORDER_NUM)
values ('user', 'websphere', '平台监控程序的补丁FP的用户名', 'PATCH', 'PT_MONITOR', 'A', '-1', null);
insert into ECC_CODE_DICT (CODE, VALUE, REMARK, GROUP_ID, MODULE, STS, COMPANY_ID, ORDER_NUM)
values ('password', '0590tnstns', '平台监控程序的补丁FP的密码', 'PATCH', 'PT_MONITOR', 'A', '-1', null);
insert into ECC_CODE_DICT (CODE, VALUE, REMARK, GROUP_ID, MODULE, STS, COMPANY_ID, ORDER_NUM)
values ('dict', '/home/websphere/python_code', '平台监控程序的补丁FTP的补丁路径', 'PATCH', 'PT_MONITOR', 'A', '-1', null);
commit;
prompt 5 records loaded
prompt Enabling triggers for ECC_CODE_DICT...
alter table ECC_CODE_DICT enable all triggers;
set feedback on
set define on
prompt Done.
