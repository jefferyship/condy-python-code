# -*- coding:GBK -*-
'''
Created on 2011-1-7
modify by Condy 2011.12.15 �޸�getHardSpace()������

@author: ����
'''
import os
psutilUsed=True
try:
    import psutil
except Exception:
    psutilUsed=False
def getHardSpace():
    """
    ��ȡ�ļ�ϵͳ�Ĵ��̿ռ�
    ����ֵ:list���󡣰���:tuple����(�ļ�ϵͳ,���ÿռ�,���ÿռ�,����%,���ص�)��
  �ռ�ĵ�λ��KB
     �ļ�ϵͳ                                        1K-��        ����                          ����   ����% ���ص�
/dev/sda3            123887420  23195148  94297600  20% /
/dev/sda1              2030736     43240   1882676   3% /boot
tmpfs                  8202300         0   8202300   0% /dev/shm
    """
    hardSpaceStd=os.popen('df')
    hardSpaceList=[]
    lastHarsSpaceLine=''
    for hardSpaceLine in hardSpaceStd.readlines():
        hardSpaceLineList=hardSpaceLine.split()
       #������Ӧ���Ƕ�len(hardSpaceLineList)<6���жϣ����п��ܴ��ڿ��е�����len(hardSpaceLineList)<5���ж�
        if len(hardSpaceLineList)<5 or hardSpaceLineList[0] in ['tmpfs','none']:
            lastHarsSpaceLine=hardSpaceLine
            continue
        #�������ֿ��е��ַ������⴦��
        #192.168.91.15:/data39
        #               1099538656 757823808 284960416  73% /data15guazai
        if len(lastHarsSpaceLine.split())==1 and len(hardSpaceLineList)==5:
            hardSpaceList.append((lastHarsSpaceLine.split()[0],hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3][:-1],hardSpaceLineList[4]))
        elif len(hardSpaceLineList)>=6:#�ļ�ϵͳ,�ܼƴ�С,���ÿռ�,���ÿռ�,����%,���ص�
            hardSpaceList.append((hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3],hardSpaceLineList[4][:-1],hardSpaceLineList[5]))
        lastHarsSpaceLine=hardSpaceLine
    if len(hardSpaceList)>0: #ɾ����һ���Ǳ��⣬��ʹ��
        del hardSpaceList[0]
    return hardSpaceList
def getCpuIdle():
    """
     Get System Cpu Information.
    """
    if psutilUsed==False: return None
    usedPercent=psutil.cpu_percent(.2)
    return round(100-usedPercent,3)
def getMemoryInfo():
    """ return a tuple(total_phymen,avi_phymen.used_phymen) KB .get System Memory Inforation"""
    if psutilUsed==False: return None
    totalPhymen=psutil.TOTAL_PHYMEM
    aviPhymen=psutil.avail_phymem()
    usedPhymen=psutil.used_phymem()
    return (totalPhymen/1024,aviPhymen/1024,usedPhymen/1024)

def getCPUUsedByPidName(pidNameList):
    """ return a list [(name,pid,usedCpu,usedMemory)]"""
    pidObjectList=[]
    if psutilUsed==False: return None
    if len(pidNameList)==0:
        return pidObjectList
    pidStrList=psutil.get_pid_list()
    for pidStr in pidStrList:
    	try: p=psutil.Process(pidStr)
    	except psutil.NoSuchProcess: continue
        #print 'pid:%s,cpu:%d'%(pidStr,p.get_cpu_percent(0.2))
        if p.name in pidNameList:
            cpuPercent=p.get_cpu_percent(0.1)
            name=p.name
            pid=p.pid
            memoryPercent=p.get_memory_percent()
            pidObjectList.append((name,pid,cpuPercent,memoryPercent))

    return pidObjectList
def getdiskByPath(path):
    """
     ����Tuple(total,used,free,usedPercent)
    """
    if  psutilUsed==True and psutil.version_info>=(0,3,0):#0.3���ϰ汾֧��������ܡ�
        return psutil.disk_usage(path)
    else:return None