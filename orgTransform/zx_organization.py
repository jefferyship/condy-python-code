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
__zxDB=None
__eccucDB=None
log=None
ORG_RECYCLE_TIMES=20
ORG_IS_START='1'
ORG_ECCUC_DB_USER_PWD=''
ORG_NGCC_DB_USER_PWD=''
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
    def udpateZx(self):
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


    def updateEcc(self):
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
        cursor=__eccucDB.cursor()

        if self.result=='0':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
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
    def udpateZx(self):
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


    def updateEcc(self):
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
        cursor=__eccucDB.cursor()

        if self.result=='0':#ͬ������ϵͳ�ɹ�.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
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
    def udpateZx(self):
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
        zxResult=skill.udpateZx()
        eccucResult=skill.updateEcc()
        log.info('���¼��������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
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
        zxResult=group.udpateZx()
        eccucResult=group.updateEcc()
        log.info('���°������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
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
            zxOperatorTemp.action=row[4]
            operatorList.append(zxOperatorTemp)
    except:
        log.exception('ִ��SQL������:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('����û�д�ͬ��������')
    for operator in operatorList:
        zxResult=operator.udpateZx()
        eccucResult=operator.updateEcc()
        log.info('��ȡ�������ݣ�agent_id:%s,orderId:%s,����ƽ̨���½��:%s,ҵ��ƽ̨���½��:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def syn(notUsed):
    try:
         log.info('zx_organization �߳�������')
         while ORG_IS_START=='1':
            try:
                global __eccucDB,__zxDB,ORG_RECYCLE_TIMES
                __eccucDB=cx_Oracle.connect(ORG_ECCUC_DB_USER_PWD)
                #__zxDB=cx_Oracle.connect(ORG_NGCC_DB_USER_PWD)
                synZxGroup()#ͬ��������Ϣ
                synZxoperator() #ͬ��Ա����Ϣ
                synZxSkill()#ͬ����������Ϣ
                time.sleep(ORG_RECYCLE_TIMES)
                if ORG_IS_START=='0':
                    log.info('IS_START value=:'+ORG_IS_START+' so zx_organization exit!')
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
        log.info('zx_organization eccucDB oracle connect success close()')
   if __zxDB<>None:
        __zxDB.close()
        log.info('zx_organization zxDB oracle connect success close()')