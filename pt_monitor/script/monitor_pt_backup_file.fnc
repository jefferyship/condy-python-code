create or replace function monitor_pt_backup_file(monitorName varchar2) return varchar2 is
/*
    create by Condy 2011.05.26
    功能：获取监控平台的备份信息
          
    输入：
    monitorName:监控平台名称
    输出：
     
    
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
  return '0'||chr(1)||'成功'||chr(3)||backupPath||chr(1)||ftpIp||chr(1)||ftpUser||chr(1)||ftpPassword||chr(1)||ftpBackupPath;
  exception
    when no_data_found then
      return '0'||chr(1)||'没有配置数据';
    when others then 
        rollback;
        return sqlcode||chr(1)||'调用服务失败';
end;
/
