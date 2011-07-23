create or replace function monitor_pt_backup_file(monitorName varchar2) return varchar2 is
/*
    create by Condy 2011.05.26
    ���ܣ���ȡ���ƽ̨�ı�����Ϣ
          
    ���룺
    monitorName:���ƽ̨����
    �����
     
    
  */
  backupPath varchar2(1024);
  ftpIp varchar2(32);
  ftpUser varchar2(32);
  ftpPassword varchar2(32);
  ftpBackupPath varchar2(512);
  
begin
  select backup_path,ftp_ip,ftp_user,ftp_password,ftp_backup_path 
        into backupPath,ftpIp,ftpUser,ftpPassword,ftpBackupPath from monitor_pt_backup_info where (next_backup_time<sysdate or next_backup_time is null) and monitor_name=monitorName;
  update monitor_pt_backup_info a set a.last_backup_time=a.next_backup_time,a.next_backup_time=sysdate+a.backup_cycle where monitor_name=monitorName;
  commit;
  return '0'||chr(1)||'�ɹ�'||chr(3)||backupPath||chr(1)||ftpIp||chr(1)||ftpUser||chr(1)||ftpPassword||chr(1)||ftpBackupPath;
  exception
    when no_data_found then
      return '0'||chr(1)||'û����������';
    when others then 
        rollback;
        return sqlcode||chr(1)||'���÷���ʧ��';
end;
/