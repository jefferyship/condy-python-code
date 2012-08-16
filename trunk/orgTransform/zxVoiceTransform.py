#!/usr/bin/env python
# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        ������֯�ܹ�����ģ��
# Purpose:
#   1.���š����š������������˻����ĶԽ�
#   ����ƽ̨���ݿ��н����ӡ��޸ġ�ɾ���Ĳ��š����ű���Ϣ�������ƺ�������ƽ̨ͬ��.
#
# Author:      ����
#
# Created:     09/07/2012
# Copyright:   (c) ���� 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cx_Oracle
import os
import sys
import logging
import logging.handlers
import ConfigParser
import time
import thread
import datetime 
class zxSkill:
    """���˼����������ɾ���޸�"""
    def  __init__(self):
        self.order_id=None
        self.vc_id=None
        self.skill_id=None
        self.skill_name=None
        self.skill_desc=None
        self.action=None
        self.result='-1'
        self.state_sts='A'
    def addSkill(self):
        """���Ӽ���"""
        return True
    def deleteSkill(self):
        """ɾ������"""
        return True
    def modifySkill(self):
        """ɾ������"""
        return True
    def udpateZx(self,zxDB):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addSkill()
         elif self.action=='DELETE':
            bResult=self.deleteSkill()
         elif self.action=='MODIFY':
            bResult=self.modifySkill()
         else:
            log.warn('�޷�ʶ��ļ��ܸ��¶�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self,eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin \
 insert all into zx_skill_group_log(order_id,vc_id,skill_id,skill_name,insert_time,update_time,action,sts,result)\
 select order_id,vc_id,skill_id,skill_id,insert_time,sysdate update_time,action, '"+self.sts+"' sts,'"+self.result+"' result from zx_skill_group\
  where order_id=:order_id1;\
  delete from zx_skill_group where order_id=:order_id2; end;"
        failSql="update zx_skill_group set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=eccucDB.cursor()

        if self.result=='0':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('���¼��������ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
                bResult=True
            except:
                log.exception('���¼��������ݽӿڴ���:'+failSql)
        cursor.close()
        return bResult;
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
    def updateZx(self,eccucDB):
        cursor=eccucDB.cursor()
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

class zxGroup:
    """���˰��������ɾ���޸�"""
    def  __init__(self):
        self.order_id=None
        self.vc_id=None
        self.group_id=None
        self.parent_group_id=None
        self.group_name=None
        self.group_desc=None
        self.action=None
        self.result='-1'
        self.state_sts='A'
    def addGroup(self):
        """���Ӱ���"""
        return True
    def deleteGroup(self):
        """ɾ������"""
        return True
    def modifyGroup(self):
        """ɾ������"""
        return True
    def udpateZx(self,zxDB):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addGroup()
         elif self.action=='DELETE':
            bResult=self.deleteGroup()
         elif self.action=='MODIFY':
            bResult=self.modifyGroup()
         else:
            log.warn('�޷�ʶ��İ�����¶�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self,eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin \
  insert all into zx_group_info_log(order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,update_time,action,sts,result)\
  select order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,sysdate update_time,action,'"+self.sts+"' sts,'"+self.result+"' result from zx_group_info\
  where order_id=:order_id1;\
  delete from zx_group_info where order_id=:order_id2; end;"
        failSql="update zx_group_info set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=eccucDB.cursor()

        if self.result=='0':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('���°������ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
                bResult=True
            except:
                log.exception('���°������ݽӿڴ���:'+failSql)
        cursor.close()
        return bResult;

class zxOperator:
    def  __init__(self):
        self.order_id=None
        self.vc_id=None
        self.group_id=None
        self.agent_id=None
        self.action=None
        self.result='-1'
        self.state_sts='A'
    def addOperator(self):
        """����Ա��"""
        return True
    def deleteOperator(self):
        """ɾ��Ա��"""
        return True
    def modifyOperator(self):
        """ɾ��Ա��"""
        return True
    def udpateZx(self,zxDB):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addOperator()
         elif self.action=='DELETE':
            bResult=self.deleteOperator()
         elif self.action=='MODIFY':
            bResult=self.modifyOperator()
         else:
            log.warn('�޷�ʶ��Ĺ��Ŷ�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self,eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin insert all into zx_operator_log(order_id,vc_id,group_id,agent_id,agent_name,action,result,insert_time,update_time,sts)\
 select order_id,vc_id,group_id,agent_id,agent_name,action,'"+self.result+"' result,insert_time,sysdate update_time,'"+self.sts+"' sts from zx_operator\
 where order_id=:orderId1; delete from zx_operator where order_id=:orderId2; end;"
        failSql="update zx_operator set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=eccucDB.cursor()

        if self.result=='0':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('����ҵ�����ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
                bResult=True
            except:
                log.exception('����ҵ�����ݽӿڴ���:'+failSql)
        cursor.close()
        return bResult;

def synZxSkill(eccucDB,zxDB):
    """
     ��ȡ��Ҫͬ���ļ����������
    """
    cursor=eccucDB.cursor()
    skillList=[]
    try:
        sql="""select order_id,vc_id,skill_id,skill_name,action from zx_skill_group where state_sts=:sts and rownum<100 order by insert_time,order_id
        """
        cursor.execute(sql,sts='A')

        for row in cursor:
            zxSkillTemp=zxSkill()
            zxSkillTemp.order_id=row[0]
            zxSkillTemp.vc_id=row[1]
            zxSkillTemp.skill_id=row[2]
            zxSkillTemp.skill_name=row[3]
            zxSkillTemp.action=row[4]
            skillList.append(zxSkillTemp)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if len(skillList)==0:
        log.info('������û�д�ͬ��������')
    for skill in skillList:
        zxResult=skill.udpateZx(zxDB)
        eccucResult=skill.updateEcc(eccucDB)
        log.info('���¼��������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def synZxGroup(eccucDB,zxDB):
    """
     ��ȡ��Ҫͬ���İ��������
    """
    cursor=eccucDB.cursor()
    groupList=[]
    try:
        sql="""select order_id,vc_id,group_id,parent_group_id,group_name,action from zx_group_info where state_sts=:sts and rownum<100 order by insert_time,order_id
        """
        cursor.execute(sql,sts='A')
        for row in cursor:
            zxGroupTemp=zxGroup()
            zxGroupTemp.order_id=row[0]
            zxGroupTemp.vc_id=row[1]
            zxGroupTemp.group_id=row[2]
            zxGroupTemp.parent_group_id=row[3]
            zxGroupTemp.group_name=row[4]
            zxGroupTemp.action=row[5]
            groupList.append(zxGroupTemp)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if len(groupList)==0:
        log.info('����û�д�ͬ��������')
    for group in groupList:
        zxResult=group.udpateZx(zxDB)
        eccucResult=group.updateEcc(eccucDB)
        log.info('���°������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)

def getLastRecordTime(eccucDB):
    """��ȡ�ϴ�¼���ĸ���ʱ��"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from ecc_parameters t where t.param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=eccucDB.cursor()
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

def setLastRecordTime(eccucDB,updatetime):
    """�����ϴ�¼���ĸ���ʱ��"""
    sql="update ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=eccucDB.cursor()
    bResult=False
    try:
        log.info('���¸��µ�ʱ��Ϊ:'+str(updatetime))
        cursor.execute(sql,updatetime=updatetime)
        eccucDB.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    return bResult

def synZxVoice(eccucDB,zxDB):
    """
     ��ȡ��Ҫ¼�����ݵ�����
    """
    updatetime=getLastRecordTime(eccucDB)
    orialupdatetime=updatetime
    cursor=zxDB.cursor()
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
            try:
                zxVoiceTemp.duration=int(row[9])
            except:
                zxVoiceTemp.duration=0
            zxVoiceTemp.skill_group_id=row[10]
            zxVoiceTemp.begin_time=row[11]
            updatetime=row[12]
            log.info('callseq:%s,subseq:%s,staff_id:%s,caller_nbr:%s,file_path:%s,file_name:%s',zxVoiceTemp.call_seq,zxVoiceTemp.sub_seq,zxVoiceTemp.staff_id,zxVoiceTemp.caller_nbr,zxVoiceTemp.file_path,zxVoiceTemp.file_name)
            zxVoiceTemp.updateZx(eccucDB)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if orialupdatetime<>updatetime:
        setLastRecordTime(eccucDB,updatetime)
def synZxoperator(eccucDB,zxDB):
    """
     ��ȡ��Ҫͬ���Ĺ��ŵ�����
    """
    cursor=eccucDB.cursor()
    operatorList=[]
    try:
        sql="""select order_id,vc_id,group_id,agent_id,agent_name,action from zx_operator where state_sts=:sts and rownum<100 order by insert_time,order_id
        """
        cursor.execute(sql,sts='A')

        #operatorList=cursor.fetchall()
        for row in cursor:
            zxOperatorTemp=zxOperator()
            zxOperatorTemp.order_id=row[0]
            zxOperatorTemp.vc_id=row[1]
            zxOperatorTemp.group_id=row[2]
            zxOperatorTemp.agent_id=row[3]
            zxOperatorTemp.action=row[4]
            operatorList.append(zxOperatorTemp)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('����û�д�ͬ��������')
    for operator in operatorList:
        zxResult=operator.udpateZx(zxDB)
        eccucResult=operator.updateEcc(eccucDB)
        log.info('��ȡ�������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def getCommonConfig():
    """
      ��ȡivrtrack.ini�������ļ���Ϣ
    """
    global URL
    global MONITOR_NAME
    global IS_START
    global RECYCLE_TIMES
    global ECCUC_DB_USER_PWD
    global NGCC_DB_USER_PWD
    global sNGCCzxStaffPassword
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'zxTransform.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    sNGCCzxStaffPassword=config.get('common', 'sNGCCzxStaffPassword')
    try:
        RECYCLE_TIMES=float(config.get('common', 'RECYCLE_TIMES'))
    except TypeError:
        RECYCLE_TIMES=10
    try:
        ECCUC_DB_USER_PWD=config.get('database', 'ECCUC_DB_USER_PWD')
        NGCC_DB_USER_PWD=config.get('database', 'NGCC_DB_USER_PWD')
    except TypeError:
        log.error('��ȡECCUC�����ݿ����ӳ�ʧ��,��ȷ��zxTransform.ini����ECCUC_DB_USER_PWD������')

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def synNgcc():
    try:
        while IS_START=='1':
            try:
                getCommonConfig()
                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
                synZxGroup(eccucDB,zxDB)#ͬ��������Ϣ
                synZxoperator(eccucDB,zxDB) #ͬ��Ա����Ϣ
                synZxSkill(eccucDB,zxDB)#ͬ����������Ϣ
                time.sleep(RECYCLE_TIMES)
                if IS_START=='0':
                    log.info('IS_START value=:'+IS_START+' so exit!')
            except Exception:
                log.exception('ϵͳ����')
            finally:
                closeDB()
    except Exception:
        log.exception('ϵͳ����')
def closeDB():
   if eccucDB<>None:
        eccucDB.close()
        log.info('eccucDB oracle connect success close()')
   if zxDB<>None:
        zxDB.close()
        log.info('zxDB oracle connect success close()')
def get_version():
    version ='1.0.0'
    """
     ��ȡ�汾��Ϣ.
    """
    log.info( '=========================================================================')
    log.info('  zxTransform.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.07.10 ')
    log.info('  ʹ�÷���:��������1.ȷ��zxTransform.ini�е�IS_START=1.���� nohup ./zxTransform.py &  ')
    log.info('           �ر�:zxTransform.ini�е�IS_START��������Ϊ0.�ͻ��Զ�ֹͣ')
    log.info('  ���ܵ㣺ͬ��������ϵͳ�Ĺ���')
    log.info( '=========================================================================')
    return version

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'zxTransform.log',maxBytes=2097152,backupCount=5)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    recordErrorlog = logging.getLogger('recordError')
    recordErrorlog .setLevel(logging.DEBUG)
    h2 = logging.handlers.RotatingFileHandler(config_dir+'recordError.log',maxBytes=2097152,backupCount=5)
    f2=logging.Formatter('%(asctime)s %(message)s')
    h2.setFormatter(f2)
    recordErrorlog.addHandler(h2)
    get_version()
    getCommonConfig()
    zxDB=None
    eccucDB=None
    try:
        if IS_START=='0':
            log.info('zxTransform.ini���õ�IS_START==\'0\',�����Զ��˳�!')
        while IS_START=='1':
            try:
                getCommonConfig()
                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
                zxDB=cx_Oracle.connect(NGCC_DB_USER_PWD)
                synZxGroup(eccucDB,zxDB)#ͬ��������Ϣ
                synZxoperator(eccucDB,zxDB) #ͬ��Ա����Ϣ
                synZxVoice(eccucDB,zxDB) #ͬ��Ա����Ϣ
                synZxSkill(eccucDB,zxDB)#ͬ����������Ϣ

            except Exception:
                log.exception('ϵͳ����')
            finally:
                closeDB()
            time.sleep(RECYCLE_TIMES)
            if IS_START=='0':
                log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('ϵͳ����')
    finally:
        h1.close()
