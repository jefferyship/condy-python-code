# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        zx_organization
# Purpose:#   1.工号、部门、技能组与中兴环境的对接
#   从云平台数据库中将增加、修改、删除的部门、工号表信息与中兴云呼叫中心平台同步.
#
# Author:      林桦
#
# Created:     21/07/2012
# Copyright:   (c) 林桦 2012
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
    """中兴技能组的增加删除修改"""
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
        """增加技能"""
        return True
    def deleteSkill(self):
        """删除技能"""
        return True
    def modifySkill(self):
        """删除技能"""
        return True
    def udpateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addSkill()
         elif self.action=='DELETE':
            bResult=self.deleteSkill()
         elif self.action=='MODIFY':
            bResult=self.modifySkill()
         else:
            log.warn('无法识别的技能更新动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin \
 insert all into zx_skill_group_log(order_id,vc_id,skill_id,skill_name,insert_time,update_time,action,sts,result)\
 select order_id,vc_id,skill_id,skill_id,insert_time,sysdate update_time,action, '"+self.sts+"' sts,'"+self.result+"' result from zx_skill_group\
  where order_id=:order_id1;\
  delete from zx_skill_group where order_id=:order_id2; end;"
        failSql="update zx_skill_group set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.result=='0':#同步中兴系统成功.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('更新技能组数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('更新技能组数据接口错误:'+failSql)
        cursor.close()
        return bResult;
class zxGroup:
    """中兴班组的增加删除修改"""
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
        """增加班组"""
        return True
    def deleteGroup(self):
        """删除班组"""
        return True
    def modifyGroup(self):
        """删除班组"""
        return True
    def udpateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addGroup()
         elif self.action=='DELETE':
            bResult=self.deleteGroup()
         elif self.action=='MODIFY':
            bResult=self.modifyGroup()
         else:
            log.warn('无法识别的班组更新动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin \
  insert all into zx_group_info_log(order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,update_time,action,sts,result)\
  select order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,sysdate update_time,action,'"+self.sts+"' sts,'"+self.result+"' result from zx_group_info\
  where order_id=:order_id1;\
  delete from zx_group_info where order_id=:order_id2; end;"
        failSql="update zx_group_info set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.result=='0':#同步中兴系统成功.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('更新班组数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('更新班组数据接口错误:'+failSql)
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
        """增加员工"""
        return True
    def deleteOperator(self):
        """删除员工"""
        return True
    def modifyOperator(self):
        """删除员工"""
        return True
    def udpateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addOperator()
         elif self.action=='DELETE':
            bResult=self.deleteOperator()
         elif self.action=='MODIFY':
            bResult=self.modifyOperator()
         else:
            log.warn('无法识别的工号动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;
def synZxSkill():
    """
     读取需要同步的技能组的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(skillList)==0:
        log.info('技能组没有待同步的数据')
    for skill in skillList:
        zxResult=skill.udpateZx()
        eccucResult=skill.updateEcc()
        log.info('更新技能组数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def synZxGroup():
    """
     读取需要同步的班组的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(groupList)==0:
        log.info('班组没有待同步的数据')
    for group in groupList:
        zxResult=group.udpateZx()
        eccucResult=group.updateEcc()
        log.info('更新班组数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def synZxoperator():
    """
     读取需要同步的工号的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('工号没有待同步的数据')
    for operator in operatorList:
        zxResult=operator.udpateZx()
        eccucResult=operator.updateEcc()
        log.info('获取工号数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def syn(notUsed):
    try:
         log.info('zx_organization 线程已启动')
         while ORG_IS_START=='1':
            try:
                global __eccucDB,__zxDB,ORG_RECYCLE_TIMES
                __eccucDB=cx_Oracle.connect(ORG_ECCUC_DB_USER_PWD)
                #__zxDB=cx_Oracle.connect(ORG_NGCC_DB_USER_PWD)
                synZxGroup()#同步班组信息
                synZxoperator() #同步员工信息
                synZxSkill()#同步技能组信息
                time.sleep(ORG_RECYCLE_TIMES)
                if ORG_IS_START=='0':
                    log.info('IS_START value=:'+ORG_IS_START+' so zx_organization exit!')
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
        log.info('zx_organization eccucDB oracle connect success close()')
   if __zxDB<>None:
        __zxDB.close()
        log.info('zx_organization zxDB oracle connect success close()')