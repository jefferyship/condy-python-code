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
import threading
import zx_organization
import zx_record

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
    global DEFAULT_AGENT_PWD
    global ENHANCECC_URL
    config=ConfigParser.ConfigParser()
    ivrtrackFileObject=open(config_dir+'zxTransform.ini')
    config.readfp(ivrtrackFileObject)
    URL=config.get('common', 'URL')
    MONITOR_NAME=config.get('common', 'MONITOR_NAME')
    IS_START=config.get('common', 'IS_START')
    DEFAULT_AGENT_PWD=config.get('common', 'DEFAULT_AGENT_PWD')
    ENHANCECC_URL=config.get('common', 'ENHANCECC_URL')
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
    log.setLevel(logging.INFO)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'zxTransform.log',maxBytes=2097152,backupCount=5)
    f=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    get_version()
    getCommonConfig()
    zx_organization_thread=None
    zx_record_thread=None
    try:
        if IS_START=='0':
            log.info('zxTransform.ini配置的IS_START==\'0\',程序自动退出!')
        else:
            zx_organization.log=log
            zx_record.log=log
            while IS_START=='1':
                try:
                    getCommonConfig()
                    zx_organization.ORG_RECYCLE_TIMES=10
                    zx_organization.ORG_IS_START=IS_START
                    zx_organization.ORG_ECCUC_DB_USER_PWD=ECCUC_DB_USER_PWD
                    zx_organization.ORG_NGCC_DB_USER_PWD=NGCC_DB_USER_PWD
                    zx_organization.DEFAULT_AGENT_PWD=DEFAULT_AGENT_PWD
                    zx_organization.ENHANCECC_URL=ENHANCECC_URL
                    if zx_organization_thread==None:
                        zx_organization_thread=threading.Thread(target=zx_organization.syn,args=('',))#启动线程.
                        zx_organization_thread.start()
                        log.info('zx_organization,现场启动完毕，线程ID为:%s',str(zx_organization_thread))

                    zx_record.REC_RECYCLE_TIMES=15
                    zx_record.REC_IS_START=IS_START
                    zx_record.REC_ECCUC_DB_USER_PWD=ECCUC_DB_USER_PWD
                    zx_record.REC_NGCC_DB_USER_PWD=NGCC_DB_USER_PWD
                    if zx_record_thread==None:
                        zx_record_thread=threading.Thread(target=zx_record.syn,args=('',))#启动线程.
                        zx_record_thread.start()
                        log.info('zx_record,现场启动完毕，线程ID为:%s',str(zx_record_thread))

                    time.sleep(RECYCLE_TIMES)
                    if IS_START=='0':
                        log.info('IS_START value=:'+IS_START+' so zxTransform exit!')
                except Exception:
                    log.exception('系统错误')
    except Exception:
        log.exception('系统报错')
    finally:
        h1.close()

