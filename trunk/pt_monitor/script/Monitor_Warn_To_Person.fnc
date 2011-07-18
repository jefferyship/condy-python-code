create or replace function Monitor_Warn_To_Person(monitorName in varchar2,WarningContent in varchar2) return varchar2 is
/*
    create by Condy 2011.01.05
    ���ܣ���ȡ���ƽ̨����Ϣ����������ļ�����صĹؼ��֣��澯��ֵ��.

    ���룺
    monitorName:���ƽ̨����
    �����

  */
  smsResult varchar2(100);
  v_contact_persons varchar2(512);
begin
   for c in (select WARNING_SMS_ID from monitor_pt_machine_name d where d.monitor_name=monitorName and d.WARNING_SMS_ID is not null)
   loop
     select contact_persons into v_contact_persons from monitor_pt_warning_person where warning_sms_id=c.WARNING_SMS_ID;
     smsResult:=ECC_SMS_INSERT('10001',v_contact_persons,WarningContent,'SYSTEMWARING','','5910','1','0591','ϵͳ�澯','');
   end loop;
  return '0'||chr(1)||'�ɹ�'||chr(3)||smsResult;
end ;
/
