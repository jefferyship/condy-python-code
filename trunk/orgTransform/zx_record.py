# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_record
# Purpose:#   1.ͬ��¼����¼
#
# Author:      ����
#
# Created:     21/07/2012
# Copyright:   (c) ���� 2012
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
        self.staff_id=None #����
        self.cti_node_id='1'#CIT�ڵ��
        self.cti_terminal_id=None #�ն˺�
        self.call_seq=None#������ˮ��
        self.sub_seq=None #��������ˮ��
        self.call_type=None #��������
        self.caller_nbr=None #���к���
        self.dial_nbr=None #���к���
        self.file_path=None #¼��·��
        self.file_name=None #¼���ļ���
        self.duration=None #¼��ʱ��
        self.vri_node_id='99'
        self.company_id=None #��˾ID
        self.skill_group_id=None #������ID
        self.callin_time=None #����ʱ��
        self.begin_time=None #��ʼͨ��ʱ��
    def updateZx(self,__eccucDB):
        cursor=__eccucDB.cursor()
        paramList=[]
        #callseq:A0140120720155500083
        try:
            self.callin_time=datetime.datetime.strptime(self.call_seq[-15,-3],'%y%m%d%H%M%S')#���ڸ�ʽ:yymmddhh24miss
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
               log.warn('д¼������,���Ϊ:%s,�������Ϊ:%s',funcResult,funcStr)
               recordErrorlog.info(funcStr)
               return False
        except:
            log.exception('д¼������,�������Ϊ:%s',funcStr)
            recordErrorlog.info(funcStr)
        finally:
            cursor.close()
def getLastRecordTime():
    """��ȡ�ϴ�¼���ĸ���ʱ��"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from ecc_parameters t where t.param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=__eccucDB.cursor()
    updatetime=None
    try:
        cursor.execute(sql)
        updatetime=cursor.fetchone()[0]
        log.debug('��ȡ������ֵΪ:'+str(updatetime))
        log.debug(sql)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    return updatetime

def setLastRecordTime(updatetime):
    """�����ϴ�¼���ĸ���ʱ��"""
    sql="update ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=__eccucDB.cursor()
    bResult=False
    try:
        log.info('���¸��µ�ʱ��Ϊ:'+str(updatetime))
        cursor.execute(sql,updatetime=updatetime)
        __eccucDB.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    return bResult

def synZxVoice():
    """
     ��ȡ��Ҫ¼�����ݵ�����
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
                zxVoiceTemp.file_name=zxVoiceTemp.file_name.replace('.wav','') #����׺��.wav��ȥ��.
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
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if orialupdatetime<>updatetime:
        setLastRecordTime(updatetime)
def syn(notUsed):
    try:
         log.info('zx_record �߳�������')
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
                log.exception('ϵͳ����')
            finally:
                __closeDB()
    except Exception:
        log.exception('ϵͳ����')
##    try:
##        while IS_START=='1':
##            try:
##                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
##                synZxGroup(eccucDB,zxDB)#ͬ��������Ϣ
##                synZxoperator(eccucDB,zxDB) #ͬ��Ա����Ϣ
##                synZxSkill(eccucDB,zxDB)#ͬ����������Ϣ
##                time.sleep(RECYCLE_TIMES)
##                if IS_START=='0':
##                    log.info('IS_START value=:'+IS_START+' so exit!')
##            except Exception:
##                log.exception('ϵͳ����')
##            finally:
##                closeDB()
##    except Exception:
##        log.exception('ϵͳ����')
def __closeDB():
   if __eccucDB<>None:
        __eccucDB.close()
        log.info('zx_record eccucDB oracle connect success close()')
   if __zxDB<>None:
        __zxDB.close()
        log.info('zx_record zxDB oracle connect success close()')
