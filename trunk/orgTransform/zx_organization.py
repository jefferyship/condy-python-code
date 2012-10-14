# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_organization
# Purpose:#   1.���š����š������������˻����ĶԽ�
#   ����ƽ̨���ݿ��н����ӡ��޸ġ�ɾ���Ĳ��š����ű���Ϣ�������ƺ�������ƽ̨ͬ��.
#
# Author:      ����
#
# Created:     21/07/2012
# Copyright:   (c) ���� 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cx_Oracle
import time
from suds.client import Client
import os,sys
import logging
import logging.handlers
__eccucDB=None
log=None
ORG_RECYCLE_TIMES=20
ORG_IS_START='1'
ORG_ECCUC_DB_USER_PWD=''
ORG_NGCC_DB_USER_PWD=''
ENHANCECC_URL='http://117.27.135.241:9085/enhancecc/services/ZteNgccSoapSOAP?wsdl'
DEFAULT_AGENT_PWD='ABcd1234'
DEFAULT_TIME_OUT=10
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
        self.result_msg=''
        self.state_sts='A'
    def addSkill(self):
        """���Ӽ���"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           skill_name=decodeUnicode(self.skill_name)
           skill_desc=decodeUnicode(self.skill_desc)
           result=client.service.AddSkillConfigRequest(self.vc_id,self.skill_id,skill_name,skill_desc)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('���Ӽ�����ɹ�,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('���Ӽ�����ʧ�ܣ�����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,skill_id:%s,skill_name:%s','AddSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id,self.skill_name)
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def deleteSkill(self):
        """ɾ������"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelSkillConfigRequest(self.vc_id,self.skill_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('ɾ��������ɹ�,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('ɾ��������ʧ�ܣ�����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,skill_id:%s','DelSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
               self.result_msg='����webService�����쳣'
               log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def modifySkill(self):
        """�޸ļ���"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           skill_name=decodeUnicode(self.skill_name)
           skill_desc=decodeUnicode(self.skill_desc)
           result=client.service.ModSkillConfigRequest(self.vc_id,self.skill_id,skill_name,skill_desc)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('�޸ļ�����ɹ�,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('�޸ļ�����ʧ�ܣ�����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,skill_id:%s,skill_name:%s,skill_desc:%s','ModSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id,self.skill_name,self.skill_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
               self.result_msg='����webService�����쳣'
               log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addSkill()
         elif self.action=='DELETE':
            bResult=self.deleteSkill()
         elif self.action=='UPDATE':
            bResult=self.modifySkill()
         else:
            log.warn('�޷�ʶ��ļ��ܸ��¶�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)
         return bResult;
    def updateEcc(self,__eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin \
 insert all into zx_skill_group_log(order_id,vc_id,skill_id,skill_name,insert_time,update_time,action,sts,result,result_msg)\
 select order_id,vc_id,skill_id,skill_name,insert_time,sysdate update_time,action, '"+self.state_sts+"' sts,'"+self.result+"' result,'"+self.result_msg+"' result_msg from zx_skill_group\
  where order_id=:order_id1;\
  delete from zx_skill_group where order_id=:order_id2; end;"
        failSql="update zx_skill_group set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('���¼��������ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('���¼��������ݽӿڴ���:'+failSql)
        cursor.close()
        return bResult;
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
        self.result_msg=''
        self.state_sts='A'
    def addGroup(self):
        """���Ӱ���"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           group_name=decodeUnicode(self.group_name)
           group_desc=decodeUnicode(self.group_desc)
           result=client.service.AddGroupConfigRequest(self.vc_id,self.group_id,self.parent_group_id,group_name,group_desc)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('���Ӱ���ɹ�,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('���Ӱ���ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','AddGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def deleteGroup(self):
        """ɾ������"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelGroupConfigRequest(self.vc_id,self.group_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('ɾ������ɹ�,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('ɾ������ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','DelGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def modifyGroup(self):
        """�޸İ���"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           group_name=decodeUnicode(self.group_name)
           group_desc=decodeUnicode(self.group_desc)
           result=client.service.ModGroupConfigRequest(self.vc_id,self.group_id,group_name,group_desc)
           self.state_sts='B'
           if result:
               self.result=encodeStr(result.ResultCode)
               self.result_msg=encodeStr(result.ResultInfo)
           if self.result=='0':
               log.info('�޸İ���ɹ�,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('�޸İ���ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','ModGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addGroup()
         elif self.action=='DELETE':
            bResult=self.deleteGroup()
         elif self.action=='UPDATE':
            bResult=self.modifyGroup()
         else:
            log.warn('�޷�ʶ��İ�����¶�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self,__eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin \
  insert all into zx_group_info_log(order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,update_time,action,sts,result,result_msg)\
  select order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,sysdate update_time,action,'"+self.state_sts+"' sts,'"+self.result+"' result,'"+self.result_msg+"' result_msg from zx_group_info\
  where order_id=:order_id1;\
  delete from zx_group_info where order_id=:order_id2; end;"
        failSql="update zx_group_info set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('���°������ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('���°������ݽӿڴ���:')
        cursor.close()
        return bResult;

class zxOperator:
    def  __init__(self):
        self.order_id=None
        self.vc_id=None
        self.group_id=None
        self.agent_id=None
        self.agent_name=None
        self.action=None
        self.result='-1'
        self.state_sts='A'
        self.result_msg=''
    def addOperator(self):
        """����Ա��"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           agent_name=decodeUnicode(self.agent_name)
           result=client.service.AddAgentConfigRequest(self.vc_id,self.group_id,self.agent_id,agent_name,DEFAULT_AGENT_PWD)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('���ӹ��ųɹ�,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('���ӹ���ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,agent_id:%s,agent_name:%s','AddAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def deleteOperator(self):
        """ɾ��Ա��"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelAgentConfigRequest(self.vc_id,self.agent_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('ɾ�����ųɹ�,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('ɾ������ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,agent_id:%s,agent_name:%s','DelAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
            self.result_msg='����webService�����쳣'
            log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def modifyOperator(self):
        """�޸�Ա��"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL)
           agent_name=decodeUnicode(self.agent_name)
           result=client.service.ModAgentConfigRequest(self.vc_id,self.agent_id,agent_name,DEFAULT_AGENT_PWD)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('�޸Ĺ��ųɹ�,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('�޸Ĺ���ʧ��,����%s����ʧ�ܣ�ʧ��ԭ��:%s,�������:vc_id:%s,agent_id:%s,agent_name:%s','ModAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #���˲������������͵Ĺ��Ż�����,�����޷�ͬ����
        except Exception:
           self.result_msg='����webService�����쳣'
           log.exception('����ZX��WebService�����ַ:%s,����',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         ���µ�����ƽ̨
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addOperator()
         elif self.action=='DELETE':
            bResult=self.deleteOperator()
         elif self.action=='UPDATE':
            bResult=self.modifyOperator()
         else:
            log.warn('�޷�ʶ��Ĺ��Ŷ�����agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;
    def updateEcc(self,__eccucDB):
        """
        ���µ�eccucƽ̨.
        """
        bResult=False
        succSql="begin \
 insert all into zx_operator_log(order_id,vc_id,group_id,agent_id,agent_name,insert_time,update_time,action,sts,result,result_msg)\
 select order_id,vc_id,group_id,agent_id,agent_name,insert_time,sysdate update_time,action, '"+self.state_sts+"' sts, '"+self.result+"' result ,'"+self.result_msg+"' result_msg from zx_operator where order_id=:order_id1;\
delete from zx_operator where order_id=:order_id2; end;"
        failSql="update zx_operator set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('����Ա�����ݽӿڴ���:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('����Ա�����ݽӿڴ���:'+failSql)
        cursor.close()
        return bResult;
def synZxSkill():
    """
     ��ȡ��Ҫͬ���ļ����������
    """
    cursor=__eccucDB.cursor()
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
        zxResult=skill.updateZx()
        eccucResult=skill.updateEcc(__eccucDB)
        log.info('���¼��������ݣ�skill_id:%s,action:%s,orderId:%s,skill_name:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',skill.skill_id,skill.action,skill.order_id,skill.skill_name,zxResult,eccucResult)
def synZxGroup():
    """
     ��ȡ��Ҫͬ���İ��������
    """
    cursor=__eccucDB.cursor()
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
        zxResult=group.updateZx()
        eccucResult=group.updateEcc(__eccucDB)
        log.info('���°������ݣ�group_id:%s,action:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',group.group_id,group.action,group.order_id,zxResult,eccucResult)
def synZxoperator():
    """
     ��ȡ��Ҫͬ���Ĺ��ŵ�����
    """
    cursor=__eccucDB.cursor()
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
            zxOperatorTemp.agent_name=row[4]
            zxOperatorTemp.action=row[5]
            operatorList.append(zxOperatorTemp)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('����û�д�ͬ��������')
    for operator in operatorList:
        zxResult=operator.updateZx()
        eccucResult=operator.updateEcc(__eccucDB)
        log.info('��ȡ�������ݣ�vc_id:%s,agent_id:%s,group_id:%s,agent_name:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.vc_id,operator.agent_id,operator.group_id,operator.agent_name,operator.order_id,zxResult,eccucResult)
def syn(notUsed):
    try:
         log.info('zx_organization �߳�������')
         while ORG_IS_START=='1':
            try:
                global __eccucDB,ORG_RECYCLE_TIMES
                if ORG_ECCUC_DB_USER_PWD<>None and len(ORG_ECCUC_DB_USER_PWD)>0:
                   __eccucDB=cx_Oracle.connect(ORG_ECCUC_DB_USER_PWD)
                   synZxGroup()#ͬ��������Ϣ
                   synZxoperator() #ͬ��Ա����Ϣ
                   synZxSkill()#ͬ����������Ϣ
                else:
                   log.info('��ȡ�����ݿ����Ӵ�:ORG_ECCUC_DB_USER_PWD:%s',str(ORG_ECCUC_DB_USER_PWD))
                
                if ORG_IS_START=='0':
                    log.info('IS_START value=:'+ORG_IS_START+' so zx_organization exit!')
            except Exception:
                log.exception('ϵͳ����')
            finally:
                __closeDB()
            time.sleep(ORG_RECYCLE_TIMES)
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
   try:
     if __eccucDB<>None:
          __eccucDB.close()
          log.info('zx_organization eccucDB oracle connect success close()')
   except Exception:
       log.error('�ر����ݿ����ӱ���:')
#def init_db():
    #global __eccucDB
    #__eccucDB=cx_Oracle.connect(ORG_ECCUC_DB_USER_PWD)
def decodeUnicode(tempStr):
    uniStr=''
    if tempStr<>None and isinstance(tempStr,str):
        uniStr=tempStr.decode('GBK')
    return uniStr 
def encodeStr(uniStr):
    tempStr=''
    if uniStr<>None and isinstance(uniStr,unicode):
        tempStr=uniStr.encode('GBK')
    return tempStr 
    
#if __name__ == '__main__':
    #tempPath=os.path.split(sys.argv[0])#ȡ�ļ�����·����
    #if tempPath[0]=='':#�ļ������þ���·�������ǲ������·��ʱ��ȡ����Ŀ¼�µ�·��
        #config_dir=os.getcwd()+os.sep
    #else:
        #config_dir=tempPath[0]+os.sep
    #log = logging.getLogger()
    #log.setLevel(logging.INFO)
    #h1 = logging.handlers.RotatingFileHandler(config_dir+'zxTransform.log',maxBytes=2097152,backupCount=5)
    #f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    #h1.setFormatter(f)
    #log.addHandler(h1)
    #logging.getLogger('suds.client').setLevel(logging.INFO)
    #ORG_ECCUC_DB_USER_PWD='eccuc/eccuc@ecc10000'
    #try:
       #init_db()
       ##synZxGroup()#ͬ��������Ϣ
       ##synZxSkill()
       #synZxoperator()
    #except Exception:
        #log.exception('ϵͳ����')
    #finally:
      #__closeDB()
