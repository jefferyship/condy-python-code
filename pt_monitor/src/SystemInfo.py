# -*- coding:GBK -*-
'''
Created on 2011-1-7
modify by Condy 2011.12.15 修改getHardSpace()方法。

@author: 林桦
'''
import os
psutilUsed=True
try:
    import psutil
except Exception:
    psutilUsed=False
def getHardSpace():
    """
    获取文件系统的磁盘空间
    返回值:list对象。包含:tuple类型(文件系统,已用空间,可用空间,已用%,挂载点)。
  空间的单位是KB
     文件系统                                        1K-块        已用                          可用   已用% 挂载点
/dev/sda3            123887420  23195148  94297600  20% /
/dev/sda1              2030736     43240   1882676   3% /boot
tmpfs                  8202300         0   8202300   0% /dev/shm
    """
    hardSpaceStd=os.popen('df')
    hardSpaceList=[]
    lastHarsSpaceLine=''
    for hardSpaceLine in hardSpaceStd.readlines():
        hardSpaceLineList=hardSpaceLine.split()
       #按道理应该是对len(hardSpaceLineList)<6做判断，但有可能存在跨行的现象。len(hardSpaceLineList)<5的判断
        if len(hardSpaceLineList)<5 or hardSpaceLineList[0] in ['tmpfs','none']:
            lastHarsSpaceLine=hardSpaceLine
            continue
        #曾对这种跨行的字符做特殊处理
        #192.168.91.15:/data39
        #               1099538656 757823808 284960416  73% /data15guazai
        if len(lastHarsSpaceLine.split())==1 and len(hardSpaceLineList)==5:
            hardSpaceList.append((lastHarsSpaceLine.split()[0],hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3][:-1],hardSpaceLineList[4]))
        elif len(hardSpaceLineList)>=6:#文件系统,总计大小,已用空间,可用空间,已用%,挂载点
            hardSpaceList.append((hardSpaceLineList[0],hardSpaceLineList[1],hardSpaceLineList[2],hardSpaceLineList[3],hardSpaceLineList[4][:-1],hardSpaceLineList[5]))
        lastHarsSpaceLine=hardSpaceLine
    if len(hardSpaceList)>0: #删除第一行是标题，不使用
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
     返回Tuple(total,used,free,usedPercent)
    """
    if  psutilUsed==True and psutil.version_info>=(0,3,0):#0.3以上版本支持这个功能。
        return psutil.disk_usage(path)
    else:return None