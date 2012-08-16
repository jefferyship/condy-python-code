#!/usr/bin/env python
# -*- coding:GBK -*-
#-------------------------------------------------------------------------------
# Name:        中兴组织架构搬运模块
# Purpose:
#   1.工号、部门、技能组与中兴环境的对接
#   从云平台数据库中将增加、修改、删除的部门、工号表信息与中兴云呼叫中心平台同步.
#
# Author:      林桦
#
# Created:     09/07/2012
# Copyright:   (c) 林桦 2012
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
    def udpateZx(self,zxDB):
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


    def updateEcc(self,eccucDB):
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
        cursor=eccucDB.cursor()

        if self.result=='0':#同步中兴系统成功.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('更新技能组数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
                bResult=True
            except:
                log.exception('更新技能组数据接口错误:'+failSql)
        cursor.close()
        return bResult;
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
    def updateZx(self,eccucDB):
        cursor=eccucDB.cursor()
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
    def udpateZx(self,zxDB):
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


    def updateEcc(self,eccucDB):
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
        cursor=eccucDB.cursor()

        if self.result=='0':#同步中兴系统成功.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('更新班组数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
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
    def udpateZx(self,zxDB):
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


    def updateEcc(self,eccucDB):
        """
        更新到eccuc平台.
        """
        bResult=False
        succSql="begin insert all into zx_operator_log(order_id,vc_id,group_id,agent_id,agent_name,action,result,insert_time,update_time,sts)\
 select order_id,vc_id,group_id,agent_id,agent_name,action,'"+self.result+"' result,insert_time,sysdate update_time,'"+self.sts+"' sts from zx_operator\
 where order_id=:orderId1; delete from zx_operator where order_id=:orderId2; end;"
        failSql="update zx_operator set result=:result,update_time=sysdate where order_id=:orderId"
        cursor=eccucDB.cursor()

        if self.result=='0':#同步中兴系统成功.
             try:
                cursor.execute(succSql,orderId1=self.order_id,orderId2=self.order_id)
                eccucDB.commit()
                bResult=True
             except:
                log.exception('更新业务数据接口错误:'+succSql);
        else:
            try:
                cursor.execute(failSql,result=self.result,orderId=self.order_id)
                eccucDB.commit()
                bResult=True
            except:
                log.exception('更新业务数据接口错误:'+failSql)
        cursor.close()
        return bResult;

def synZxSkill(eccucDB,zxDB):
    """
     读取需要同步的技能组的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(skillList)==0:
        log.info('技能组没有待同步的数据')
    for skill in skillList:
        zxResult=skill.udpateZx(zxDB)
        eccucResult=skill.updateEcc(eccucDB)
        log.info('更新技能组数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def synZxGroup(eccucDB,zxDB):
    """
     读取需要同步的班组的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(groupList)==0:
        log.info('班组没有待同步的数据')
    for group in groupList:
        zxResult=group.udpateZx(zxDB)
        eccucResult=group.updateEcc(eccucDB)
        log.info('更新班组数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)

def getLastRecordTime(eccucDB):
    """获取上次录音的更新时间"""
    sql="select to_date(param_value,'yyyymmddhh24miss') from ecc_parameters t where t.param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=eccucDB.cursor()
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

def setLastRecordTime(eccucDB,updatetime):
    """设置上次录音的更新时间"""
    sql="update ecc_parameters set param_value=to_char(:updatetime,'yyyymmddhh24miss') where param_code='RECORD_UPDATE_TIME' and param_owner='ZX_CLOUD'"
    cursor=eccucDB.cursor()
    bResult=False
    try:
        log.info('最新更新的时间为:'+str(updatetime))
        cursor.execute(sql,updatetime=updatetime)
        eccucDB.commit()
        log.debug(sql)
        bResult=True
    except:
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    return bResult

def synZxVoice(eccucDB,zxDB):
    """
     读取需要录音数据的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if orialupdatetime<>updatetime:
        setLastRecordTime(eccucDB,updatetime)
def synZxoperator(eccucDB,zxDB):
    """
     读取需要同步的工号的数据
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
        log.exception('执行SQL语句错误:%s',sql)
    finally:
        cursor.close()
    if len(operatorList)==0:
        log.info('工号没有待同步的数据')
    for operator in operatorList:
        zxResult=operator.udpateZx(zxDB)
        eccucResult=operator.updateEcc(eccucDB)
        log.info('获取工号数据：agent_id:%s,orderId:%s,中兴平台更新结果:%s,业务平台更新结果:%s',operator.agent_id,operator.order_id,zxResult,eccucResult)
def getCommonConfig():
    """
      读取ivrtrack.ini的配置文件信息
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
        log.error('获取ECCUC的数据库连接池失败,请确认zxTransform.ini中有ECCUC_DB_USER_PWD的配置')

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'
def synNgcc():
    try:
        while IS_START=='1':
            try:
                getCommonConfig()
                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
                synZxGroup(eccucDB,zxDB)#同步班组信息
                synZxoperator(eccucDB,zxDB) #同步员工信息
                synZxSkill(eccucDB,zxDB)#同步技能组信息
                time.sleep(RECYCLE_TIMES)
                if IS_START=='0':
                    log.info('IS_START value=:'+IS_START+' so exit!')
            except Exception:
                log.exception('系统错误')
            finally:
                closeDB()
    except Exception:
        log.exception('系统报错')
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
     获取版本信息.
    """
    log.info( '=========================================================================')
    log.info('  zxTransform.py current version is %s               '%(version))
    log.info('  author:Condy create time:2012.07.10 ')
    log.info('  使用方法:启动方法1.确认zxTransform.ini中的IS_START=1.启动 nohup ./zxTransform.py &  ')
    log.info('           关闭:zxTransform.ini中的IS_START参数更改为0.就会自动停止')
    log.info('  功能点：同步与中兴系统的工号')
    log.info( '=========================================================================')
    return version

if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
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
            log.info('zxTransform.ini配置的IS_START==\'0\',程序自动退出!')
        while IS_START=='1':
            try:
                getCommonConfig()
                eccucDB=cx_Oracle.connect(ECCUC_DB_USER_PWD)
                zxDB=cx_Oracle.connect(NGCC_DB_USER_PWD)
                synZxGroup(eccucDB,zxDB)#同步班组信息
                synZxoperator(eccucDB,zxDB) #同步员工信息
                synZxVoice(eccucDB,zxDB) #同步员工信息
                synZxSkill(eccucDB,zxDB)#同步技能组信息

            except Exception:
                log.exception('系统错误')
            finally:
                closeDB()
            time.sleep(RECYCLE_TIMES)
            if IS_START=='0':
                log.info('IS_START value=:'+IS_START+' so exit!')
    except Exception:
        log.exception('系统报错')
    finally:
        h1.close()
