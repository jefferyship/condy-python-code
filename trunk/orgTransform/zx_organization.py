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
    """中兴技能组的增加删除修改"""
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
        """增加技能"""
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
               log.info('增加技能组成功,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('增加技能组失败，调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,skill_id:%s,skill_name:%s','AddSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id,self.skill_name)
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def deleteSkill(self):
        """删除技能"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelSkillConfigRequest(self.vc_id,self.skill_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('删除技能组成功,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('删除技能组失败，调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,skill_id:%s','DelSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
               self.result_msg='调用webService服务异常'
               log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def modifySkill(self):
        """修改技能"""
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
               log.info('修改技能组成功,vc_id:%s,skill_id:%s,skill_name:%s',self.vc_id,self.skill_id,self.skill_name)
               bResult=True
           else:
               log.warn('修改技能组失败，调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,skill_id:%s,skill_name:%s,skill_desc:%s','ModSkillConfigRequest',self.result_msg,self.vc_id,self.skill_id,self.skill_name,self.skill_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
               self.result_msg='调用webService服务异常'
               log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addSkill()
         elif self.action=='DELETE':
            bResult=self.deleteSkill()
         elif self.action=='UPDATE':
            bResult=self.modifySkill()
         else:
            log.warn('无法识别的技能更新动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)
         return bResult;
    def updateEcc(self,__eccucDB):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin \
 insert all into zx_skill_group_log(order_id,vc_id,skill_id,skill_name,insert_time,update_time,action,sts,result,result_msg)\
 select order_id,vc_id,skill_id,skill_name,insert_time,sysdate update_time,action, '"+self.state_sts+"' sts,'"+self.result+"' result,'"+self.result_msg+"' result_msg from zx_skill_group\
  where order_id=:order_id1;\
  delete from zx_skill_group where order_id=:order_id2; end;"
        failSql="update zx_skill_group set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#同步中兴系统成功.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
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
        self.result_msg=''
        self.state_sts='A'
    def addGroup(self):
        """增加班组"""
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
               log.info('增加班组成功,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('增加班组失败,调用%s服务失败，失败原因:%s,输入参数,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','AddGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def deleteGroup(self):
        """删除班组"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelGroupConfigRequest(self.vc_id,self.group_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('删除班组成功,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('删除班组失败,调用%s服务失败，失败原因:%s,输入参数,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','DelGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def modifyGroup(self):
        """修改班组"""
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
               log.info('修改班组成功,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s',self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               bResult=True
           else:
               log.warn('修改班组失败,调用%s服务失败，失败原因:%s,输入参数,vc_id:%s,group_id:%s,parent_group_id:%s,group_name:%s,group_desc:%s','ModGroupConfigRequest',self.result_msg,self.vc_id,self.group_id,self.parent_group_id,self.group_name,self.group_desc)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addGroup()
         elif self.action=='DELETE':
            bResult=self.deleteGroup()
         elif self.action=='UPDATE':
            bResult=self.modifyGroup()
         else:
            log.warn('无法识别的班组更新动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;


    def updateEcc(self,__eccucDB):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin \
  insert all into zx_group_info_log(order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,update_time,action,sts,result,result_msg)\
  select order_id,vc_id,group_id,parent_group_id,dept_id,group_name,insert_time,sysdate update_time,action,'"+self.state_sts+"' sts,'"+self.result+"' result,'"+self.result_msg+"' result_msg from zx_group_info\
  where order_id=:order_id1;\
  delete from zx_group_info where order_id=:order_id2; end;"
        failSql="update zx_group_info set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#同步中兴系统成功.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
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
                log.exception('更新班组数据接口错误:')
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
        """增加员工"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           agent_name=decodeUnicode(self.agent_name)
           result=client.service.AddAgentConfigRequest(self.vc_id,self.group_id,self.agent_id,agent_name,DEFAULT_AGENT_PWD)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('增加工号成功,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('增加工号失败,调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,agent_id:%s,agent_name:%s','AddAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def deleteOperator(self):
        """删除员工"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL,timeout=DEFAULT_TIME_OUT)
           result=client.service.DelAgentConfigRequest(self.vc_id,self.agent_id)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('删除工号成功,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('删除工号失败,调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,agent_id:%s,agent_name:%s','DelAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
            self.result_msg='调用webService服务异常'
            log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def modifyOperator(self):
        """修改员工"""
        bResult=False
        try:
           client=Client(ENHANCECC_URL)
           agent_name=decodeUnicode(self.agent_name)
           result=client.service.ModAgentConfigRequest(self.vc_id,self.agent_id,agent_name,DEFAULT_AGENT_PWD)
           self.result=encodeStr(result.ResultCode)
           self.result_msg=encodeStr(result.ResultInfo)
           self.state_sts='B'
           if self.result=='0':
               log.info('修改工号成功,vc_id:%s,agent_id:%s,agent_name:%s',self.vc_id,self.agent_id,self.agent_name)
               bResult=True
           else:
               log.info('修改工号失败,调用%s服务失败，失败原因:%s,输入参数:vc_id:%s,agent_id:%s,agent_name:%s','ModAgentConfigRequest',self.result_msg,self.vc_id,self.agent_id,self.agent_name)
               if self.result_msg.find('does not exist')>-1:
                   bResult=True #中兴不存在这种类型的工号或技能组,班组无法同步。
        except Exception:
           self.result_msg='调用webService服务异常'
           log.exception('调用ZX的WebService服务地址:%s,报错',ENHANCECC_URL)
        return bResult
    def updateZx(self):
         """
         更新到中兴平台
         """
         bResult=False
         if self.action=='INSERT':
            bResult=self.addOperator()
         elif self.action=='DELETE':
            bResult=self.deleteOperator()
         elif self.action=='UPDATE':
            bResult=self.modifyOperator()
         else:
            log.warn('无法识别的工号动作，agent_id:%s,order_id:%s,action:%s',self.agent_id,self.order_id,self.action)

       #  self.sts='B'
       #  self.result='0'
         return bResult;
    def updateEcc(self,__eccucDB):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin \
 insert all into zx_operator_log(order_id,vc_id,group_id,agent_id,agent_name,insert_time,update_time,action,sts,result,result_msg)\
 select order_id,vc_id,group_id,agent_id,agent_name,insert_time,sysdate update_time,action, '"+self.state_sts+"' sts, '"+self.result+"' result ,'"+self.result_msg+"' result_msg from zx_operator where order_id=:order_id1;\
delete from zx_operator where order_id=:order_id2; end;"
        failSql="update zx_operator set result=:result,result_msg='"+self.result_msg+"',update_time=sysdate where order_id=:orderId"
        cursor=__eccucDB.cursor()

        if self.state_sts=='B':#同步中兴系统成功.
             try:
                cursor.execute(succSql,order_id1=self.order_id,order_id2=self.order_id)
                __eccucDB.commit()
                bResult=True
             except:
                log.exception('更新员工数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                __eccucDB.commit()
                bResult=True
            except:
                log.exception('更新员工数据接口错误:'+failSql)
        cursor.close()
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
        zxResult=skill.updateZx()
        eccucResult=skill.updateEcc(__eccucDB)
        log.info('更新技能组数据：skill_id:%s,action:%s,orderId:%s,skill_name:%s,中兴平台更新结果:%s,业务平台更新结果:%s',skill.skill_id,skill.action,skill.order_id,skill.skill_name,zxResult,eccucResult)
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
        zxResult=group.updateZx()
        eccucResult=group.updateEcc(__eccucDB)
        log.info('更新班组数据：group_id:%s,action:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',group.group_id,group.action,group.order_id,zxResult,eccucResult)
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
            zxOperatorTemp.agent_name=row[4]
            zxOperatorTemp.action=row[5]
            operatorList.append(zxOperatorTemp)
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('工号没有待同步的数据')
    for operator in operatorList:
        zxResult=operator.updateZx()
        eccucResult=operator.updateEcc(__eccucDB)
        log.info('获取工号数据：vc_id:%s,agent_id:%s,group_id:%s,agent_name:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.vc_id,operator.agent_id,operator.group_id,operator.agent_name,operator.order_id,zxResult,eccucResult)
def syn(notUsed):
    try:
         log.info('zx_organization 线程已启动')
         while ORG_IS_START=='1':
            try:
                global __eccucDB,ORG_RECYCLE_TIMES
                if ORG_ECCUC_DB_USER_PWD<>None and len(ORG_ECCUC_DB_USER_PWD)>0:
                   __eccucDB=cx_Oracle.connect(ORG_ECCUC_DB_USER_PWD)
                   synZxGroup()#同步班组信息
                   synZxoperator() #同步员工信息
                   synZxSkill()#同步技能组信息
                else:
                   log.info('读取的数据库连接串:ORG_ECCUC_DB_USER_PWD:%s',str(ORG_ECCUC_DB_USER_PWD))
                
                if ORG_IS_START=='0':
                    log.info('IS_START value=:'+ORG_IS_START+' so zx_organization exit!')
            except Exception:
                log.exception('系统错误')
            finally:
                __closeDB()
            time.sleep(ORG_RECYCLE_TIMES)
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
   try:
     if __eccucDB<>None:
          __eccucDB.close()
          log.info('zx_organization eccucDB oracle connect success close()')
   except Exception:
       log.error('关闭数据库连接报错:')
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
    #tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    #if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
       ##synZxGroup()#同步班组信息
       ##synZxSkill()
       #synZxoperator()
    #except Exception:
        #log.exception('系统错误')
    #finally:
      #__closeDB()
