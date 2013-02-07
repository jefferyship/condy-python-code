# -*- coding:GBK -*-
import pyvirmgr;
import cx_Oracle
import datetime 
import logging
import logging.handlers
import os,sys
import time
log=None
IS_START='1'
ECCUC_DB_USER_PWD='eccuc/eccuc@ecc10000'
RECYCLE_TIMES=20
def syn(notUsed):
    try:
         log.info('scanDB线程已启动')
         while IS_START=='1':
            try:
                global __eccucDB,RECYCLE_TIMES
                __eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
                syn_terminalInfo()
                pyvirmgr.vcidList=getvcIdList()
                if IS_START=='0':
                    log.info('IS_START value=:'+IS_START+' so scanDB exit!')
                    break
            except Exception:
                log.exception('系统错误')
            finally:
                __closeDB()
            time.sleep(RECYCLE_TIMES)
    except Exception:
        log.exception('系统报错')
def syn_terminalInfo():
    if len(pyvirmgr.terminalInfoMap)==0:
        scan_terminalInfo(pyvirmgr.terminalInfoMap)
    else:
        update_terminalInfo(pyvirmgr.terminalInfoMap)
def update_terminalInfo(terminalInfoMap):
    global scan_update_time
    sql="select staff_id,staff_name,staff_no,a.dept_id,b.dept_name,a.company_id,a.tel_role_name,a.tel_role_id,\
            a.right_role_name,a.right_role_id from ecc_staff_manager a \
            left join ecc_dept_manager b on (a.dept_id=b.dept_id) where a.sts='A' and a.sts_date>:sts_date"
    cursor=__eccucDB.cursor()
    try:
        index=0
        cursor.execute(sql,sts_date=scan_update_time)
        for row in cursor:
            tempTerminalInfo=None
            index=index+1
            if terminalInfoMap.has_key(row[0]):
                tempTerminalInfo=terminalInfoMap[row[0]]
            else:
                tempTerminalInfo=pyvirmgr.terminalInfo()
                terminalInfoMap[row[0]]=tempTerminalInfo
            tempTerminalInfo.staff_id=row[0]
            tempTerminalInfo.staff_name=row[1]
            tempTerminalInfo.staff_no=row[2]
            tempTerminalInfo.dept_id=row[3]
            tempTerminalInfo.dept_name=row[4]
            tempTerminalInfo.company_id=row[5]
            tempTerminalInfo.tel_role_name=row[6]
            tempTerminalInfo.tel_role_id=row[7]
            tempTerminalInfo.right_role_name=row[8]
            tempTerminalInfo.right_role_id=row[9]
            terminalInfoMap[row[0]]=tempTerminalInfo
        scan_update_time=datetime.datetime.now()
        log.info('更新ecc_staff_manager表数据():总共更新:%s条数据',str(index))
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    
def scan_terminalInfo(terminalInfoMap):
    global scan_update_time #记录上传扫描的时间，下次扫描，就从这个时间点开始扫描
    sql="select staff_id,staff_name,staff_no,a.dept_id,b.dept_name,a.company_id,a.tel_role_name,a.tel_role_id,\
            a.right_role_name,a.right_role_id from ecc_staff_manager a \
            left join ecc_dept_manager b on (a.dept_id=b.dept_id) where a.sts='A'"
    cursor=__eccucDB.cursor()
    try:
        cursor.execute(sql)
        for row in cursor:
            tempTerminalInfo=pyvirmgr.terminalInfo()
            tempTerminalInfo.staff_id=row[0]
            tempTerminalInfo.staff_name=row[1]
            tempTerminalInfo.staff_no=row[2]
            tempTerminalInfo.dept_id=row[3]
            tempTerminalInfo.dept_name=row[4]
            tempTerminalInfo.company_id=row[5]
            tempTerminalInfo.tel_role_name=row[6]
            tempTerminalInfo.tel_role_id=row[7]
            tempTerminalInfo.right_role_name=row[8]
            tempTerminalInfo.right_role_id=row[9]
            terminalInfoMap[row[0]]=tempTerminalInfo
        scan_update_time=datetime.datetime.now()
        log.info('扫描ecc_staff_manager表:总共更新:%s条数据',str(len(terminalInfoMap)))
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()

def getvcIdList():
    """获取虚中心ID"""
    sql="select distinct node_id from company where sts='A'"
    vcidList=[]
    cursor=__eccucDB.cursor()
    try:
        cursor.execute(sql)
        for vcidrow in cursor:
                vcidList.append(vcidrow[0])
        log.debug('获取中兴虚中心的Id:'+sql)
    except:
        log.exception('scanDB.py:获取虚中心,执行SQL语句错误:%s',sql)
    return vcidList
def __closeDB():
   if __eccucDB<>None:
        __eccucDB.close()
        log.info('scanDB.py:eccucDB oracle connect success close()')
#if __name__ == '__main__':
    #tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    #if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        #config_dir=os.getcwd()+os.sep
    #else:
        #config_dir=tempPath[0]+os.sep
    #log = logging.getLogger()
    #log.setLevel(logging.DEBUG)
    #h1 = logging.handlers.RotatingFileHandler(config_dir+'pyvirmgr.log',maxBytes=2097152,backupCount=5)
    #f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    #h1.setFormatter(f)
    #log.addHandler(h1)
    #syn('aa')
    #log.close()

