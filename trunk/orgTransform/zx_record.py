# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_record
# Purpose:#   1.同步录音记录
#
# Author:      林桦
#
# Created:     21/07/2012
# Copyright:   (c) 林桦 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cx_Oracle
import time
import os
__zxDB=None
__eccucDB=None
log=None
REC_RECYCLE_TIMES=20
REC_IS_START='1'
REC_ECCUC_DB_USER_PWD=''
REC_NGCC_DB_USER_PWD=''
class ZxVoice:
    def  __init__(self):
        self.staff_id=None #工号
        self.cti_node_id='1'#CIT节点号
        self.cti_terminal_id=None #终端号
        self.call_seq=None#呼叫流水号
        self.sub_seq=None #呼叫子流水号
        self.call_type=None #呼叫类型
        self.caller_nbr=None #主叫号码
        self.dial_nbr=None #被叫号码
        self.file_path=None #录音路径
        self.file_name=None #录音文件名
        self.duration=None #录音时长
        self.vri_node_id='99'
        self.company_id=None #公司ID
        self.skill_group_id=None #技能组ID
        self.callin_time=None #呼入时间
        self.begin_time=None #开始通话时间
    def updateZx(self,__eccucDB):
        cursor=__eccucDB.cursor()
        paramList=[]
        #callseq:A0140120720155500083
        try:
            self.callin_time=datetime.datetime.strptime(self.call_seq[-15,-3],'%y%m%d%H%M%S')#日期格式:yymmddhh24miss
        except:
            self.callin_time=self.begin_time
        paramList.append(self.call_seq)
        paramList.append(self.sub_seq)
        paramList.append(self.staff_id)
        paramList.append(self.cti_node_id)
        paramList.append(self.cti_terminal_id)
        paramList.append(self.call_type)
        paramList.append(self.caller_nbr)
        paramList.append(self.dial_nbr)
        paramList.append(self.duration)
        paramList.append(self.file_path)
        paramList.append(self.file_name)
        paramList.append(self.begin_time)
        paramList.append(self.vri_node_id)
        paramList.append(self.company_id)
        paramList.append(self.skill_group_id)
        paramList.append(self.callin_time)
        funcStr='PT_RECORD_WRITE_FROM_ZX('+','.join(str(i) for i in paramList)+')'
        try:
           funcResult=cursor.callfunc('PT_RECORD_WRITE_FROM_ZX',cx_Oracle.STRING,paramList)
           log.debug(funcStr)
           if funcResult=='0':
               return True
           else:
               log.warn('写录音错误,结果为:%s,输入参数为:%s',funcResult,funcStr)
               recordErrorlog.info(funcStr)
               return False
        except:
            log.exception('写录音错误,输入参数为:%s',funcStr)
            recordErrorlog.info(funcStr)
        finally:
            cursor.close()
def getLastRecordTime():
    """获取上次录音的更新时间"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from ecc_parameters t where t.param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=__eccucDB.cursor()
    updatetime=None
    try:
        cursor.execute(sql)
        updatetime=cursor.fetchone()[0]
        log.debug('获取的日期值为:'+str(updatetime))
        log.debug(sql)
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    return updatetime

def setLastRecordTime(updatetime):
    """设置上次录音的更新时间"""
    sql="update ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=__eccucDB.cursor()
    bResult=False
    try:
        log.info('最新更新的时间为:'+str(updatetime))
        cursor.execute(sql,updatetime=updatetime)
        __eccucDB.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    return bResult

def synZxVoice():
    """
     读取需要录音数据的数据
    """
    updatetime=getLastRecordTime()
    orialupdatetime=updatetime
    cursor=__zxDB.cursor()
    voiceList=[]
    try:
        #updatetime=datetime.datetime.strptime('20120719200430','%Y%m%d%H%M%S')
        sql=" select t.connectionid call_seq,t.callid sub_seq,t.agentid staff_id,\
         t.agentphone cti_terminal_id,t.vcid company_id,t.callingnumber caller_nbr ,\
         t.callednumber dial_nbr,calltype call_type,t.recordpath,(t.callendtime-t.answertime)*24*60*60 duration,\
         t.skillid skill_group_id,t.answertime,updatetime from   zxdb_kf.cc_agentcalldetail t\
         where t.recordpath is not null and t.updatetime>:updatetime order by updatetime"
        cursor.execute(sql,updatetime=updatetime)

        #operatorList=cursor.fetchall()
        recordpath=''
        for row in cursor:
            zxVoiceTemp=ZxVoice()
            zxVoiceTemp.call_seq=row[0]
            zxVoiceTemp.sub_seq=row[1]
            zxVoiceTemp.staff_id=row[2]
            zxVoiceTemp.cti_terminal_id =row[3]
            zxVoiceTemp.company_id=row[4]
            zxVoiceTemp.caller_nbr=row[5]
            zxVoiceTemp.dial_nbr=row[6]
            zxVoiceTemp.call_type=row[7]
            zxVoiceTemp.file_path=os.path.split(row[8])[0]
            zxVoiceTemp.file_name=os.path.split(row[8])[1]
            if(str(zxVoiceTemp.file_name)):
                zxVoiceTemp.file_name=zxVoiceTemp.file_name.replace('.wav','') #将后缀是.wav的去掉.
            try:
                zxVoiceTemp.duration=int(row[9])
            except:
                zxVoiceTemp.duration=0
            zxVoiceTemp.skill_group_id=row[10]
            zxVoiceTemp.begin_time=row[11]
            updatetime=row[12]
            log.info('callseq:%s,subseq:%s,staff_id:%s,caller_nbr:%s,file_path:%s,file_name:%s',zxVoiceTemp.call_seq,zxVoiceTemp.sub_seq,zxVoiceTemp.staff_id,zxVoiceTemp.caller_nbr,zxVoiceTemp.file_path,zxVoiceTemp.file_name)
            zxVoiceTemp.updateZx(__eccucDB)
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if orialupdatetime<>updatetime:
        setLastRecordTime(updatetime)
def syn(notUsed):
    try:
         log.info('zx_record 线程已启动')
         while REC_IS_START=='1':
            try:
                global __eccucDB,__zxDB,REC_RECYCLE_TIMES
                __eccucDB=cx_Oracle.connect(REC_ECCUC_DB_USER_PWD)
                __zxDB=cx_Oracle.connect(REC_NGCC_DB_USER_PWD)
                synZxVoice()
                time.sleep(REC_RECYCLE_TIMES)
                if REC_IS_START=='0':
                    log.info('IS_START value=:'+REC_IS_START+' so zx_record exit!')
            except Exception:
                log.exception('系统错误')
            finally:
                __closeDB()
    except Exception:
        log.exception('系统报错')
##    try:
##        while IS_START=='1':
##            try:
##                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
##                synZxGroup(eccucDB,zxDB)#同步班组信息
##                synZxoperator(eccucDB,zxDB) #同步员工信息
##                synZxSkill(eccucDB,zxDB)#同步技能组信息
##                time.sleep(RECYCLE_TIMES)
##                if IS_START=='0':
##                    log.info('IS_START value=:'+IS_START+' so exit!')
##            except Exception:
##                log.exception('系统错误')
##            finally:
##                closeDB()
##    except Exception:
##        log.exception('系统报错')
def __closeDB():
   if __eccucDB<>None:
        __eccucDB.close()
        log.info('zx_record eccucDB oracle connect success close()')
   if __zxDB<>None:
        __zxDB.close()
        log.info('zx_record zxDB oracle connect success close()')
