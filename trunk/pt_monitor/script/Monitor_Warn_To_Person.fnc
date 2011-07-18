create or replace function Monitor_Warn_To_Person(monitorName in varchar2,WarningContent in varchar2) return varchar2 is
/*
    create by Condy 2011.01.05
    功能：获取监控平台的信息，包括监控文件、监控的关键字，告警阀值等.

    输入：
    monitorName:监控平台名称
    输出：

  */
  smsResult varchar2(100);
  v_contact_persons varchar2(512);
begin
   for c in (select WARNING_SMS_ID from monitor_pt_machine_name d where d.monitor_name=monitorName and d.WARNING_SMS_ID is not null)
   loop
     select contact_persons into v_contact_persons from monitor_pt_warning_person where warning_sms_id=c.WARNING_SMS_ID;
     smsResult:=ECC_SMS_INSERT('10001',v_contact_persons,WarningContent,'SYSTEMWARING','','5910','1','0591','系统告警','');
   end loop;
  return '0'||chr(1)||'成功'||chr(3)||smsResult;
end ;
/
