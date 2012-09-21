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
import threading
import zx_organization
import zx_record

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
        log.error('��ȡECCUC�����ݿ����ӳ�ʧ��,��ȷ��zxTransform.ini����ECCUC_DB_USER_PWD������')

    if len(URL)==0:
        URL='http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate'

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
            log.info('zxTransform.ini���õ�IS_START==\'0\',�����Զ��˳�!')
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
                        zx_organization_thread=threading.Thread(target=zx_organization.syn,args=('',))#�����߳�.
                        zx_organization_thread.start()
                        log.info('zx_organization,�ֳ�������ϣ��߳�IDΪ:%s',str(zx_organization_thread))

                    zx_record.REC_RECYCLE_TIMES=15
                    zx_record.REC_IS_START=IS_START
                    zx_record.REC_ECCUC_DB_USER_PWD=ECCUC_DB_USER_PWD
                    zx_record.REC_NGCC_DB_USER_PWD=NGCC_DB_USER_PWD
                    if zx_record_thread==None:
                        zx_record_thread=threading.Thread(target=zx_record.syn,args=('',))#�����߳�.
                        zx_record_thread.start()
                        log.info('zx_record,�ֳ�������ϣ��߳�IDΪ:%s',str(zx_record_thread))

                    time.sleep(RECYCLE_TIMES)
                    if IS_START=='0':
                        log.info('IS_START value=:'+IS_START+' so zxTransform exit!')
                except Exception:
                    log.exception('ϵͳ����')
    except Exception:
        log.exception('ϵͳ����')
    finally:
        h1.close()

