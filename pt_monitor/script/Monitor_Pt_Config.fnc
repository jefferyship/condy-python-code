create or replace function Monitor_Pt_Config(monitorName in varchar2) return varchar2 is
/*
    create by Condy 2011.01.05
    ���ܣ���ȡ���ƽ̨����Ϣ��
          
    ���룺
    monitorName:���ƽ̨����
    �����
      table1:��־���(�������).
         �����־���ļ���,��صĹؼ���,�澯��ֵ,�����־������,
      tabl2:ϵͳ��أ��������)
         CPU Idle��ֵ,���������ڴ淧ֵ(KB),Ӳ������(����/dev/sda3),Ӳ�̸澯��ֵ(�ٷֱ�)
      table3:�̸߳澯(�������)
         �߳����ƣ��澯��ֵ
    modify by Condy 2011.08.04 ����netstat��������Ϣ��ȡ.
    
  */
  returnValue varchar2(2000);
  v_mi varchar2(10);
  v_time varchar2(32);
  v_file_path varchar2(512);
  v_first_loop integer:=0;
  v_cpu_idle_limit varchar2(64);
  v_memory_avi_limit varchar2(64);
  v_hardspace_name varchar2(64);
  v_hardspace_limit varchar2(64);      
begin
  --��־���(�������).
   for c in (select monitor_name,file_path,keys,warn_limit,monitor_lines,time_pattern,log_type from monitor_pt_file_info where monitor_name=monitorName order by order_num)
   loop
    if v_first_loop<>0 then
      returnValue:=returnValue||chr(2);
    end if;
    v_first_loop:=v_first_loop+1;
    if c.time_pattern ='mmddhh24mi' then 
      v_time:=to_char(sysdate,'mmddhh24');
      v_mi:=to_char(sysdate,'mi');
      if c.log_type='resmgr' then --resgmgr����־��30���ӣ�����һ��.
        if v_mi>='00' and v_mi<'30' then
          v_mi:='00';
        else
          v_mi:='30';
        end if;
      else
        v_mi:=substr(v_mi,1,1)||'0';
      end if;
      v_time:=v_time||v_mi;
      v_file_path:=Replace(c.file_path, '$mmddhh24mi$', v_time);
    else
      v_file_path:=c.file_path;
    end if;
    returnValue:=returnValue||v_file_path||chr(1)||c.keys||chr(1)||c.warn_limit||chr(1)||c.monitor_lines||chr(1)||c.log_type;
   end loop;
   --returnValue:='0'||chr(1)||'�ɹ�'||chr(3)||'/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/fjas2server1/SystemOut.log'||chr(1)||'ERROR'||chr(1)||'10'||chr(1)||'1000';
   --returnValue:=returnValue||chr(2)||'/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/logs/fjas2server2/SystemOut.log'||chr(1)||'ERR'||chr(1)||'10'||chr(1)||'500';
   if returnValue is null then
      returnValue:=chr(3);
   else
     returnValue:=returnValue||chr(3);
  end if;
  
--  ϵͳ��أ��������)
begin
  select d.cpu_idle_limit,d.memory_avi_limit,d.hardspace_name,d.hardspace_limit 
   into v_cpu_idle_limit,v_memory_avi_limit,v_hardspace_name,v_hardspace_limit from monitor_pt_system_info d where monitor_name=monitorName;
   returnValue:=returnValue||v_cpu_idle_limit;
   returnValue:=returnValue||chr(1)||v_memory_avi_limit;
   returnValue:=returnValue||chr(1)||v_hardspace_name;
   returnValue:=returnValue||chr(1)||v_hardspace_limit;
   returnValue:=returnValue||chr(3);
exception
  when no_data_found then
    returnValue:=returnValue||chr(3);
end;
--�̸߳澯(�������) 
v_first_loop:=0;
 for c in (select d.proc_name,d.proc_cpu_limit from monitor_pt_proc_info d where monitor_name=monitorName ) 
 loop
   if v_first_loop<>0 then
      returnValue:=returnValue||chr(2);
    end if;
    v_first_loop:=v_first_loop+1;
    returnValue:=returnValue||c.proc_name||chr(1)||c.proc_cpu_limit;
 end loop;
 --netstat���(�������)
 v_first_loop:=0;
 returnValue:=returnValue||chr(3);
 for c in (select command,count_limit from monitor_pt_netstat_info where monitor_name=monitorName ) 
 loop
   if v_first_loop<>0 then
      returnValue:=returnValue||chr(2);
    end if;
    v_first_loop:=v_first_loop+1;
    returnValue:=returnValue||c.command||chr(1)||c.count_limit;
 end loop;
 return '0'||chr(1)||'�ɹ�'||chr(3)||returnValue;
exception 
   when others then
     return sqlcode||chr(1)||'ʧ��';
end Monitor_Pt_Config;
/
