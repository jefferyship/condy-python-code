#!/usr/bin/env python
# -*- coding: GBK -*-
import os
import sys,ConfigParser
import glob
xpath=''
area=''
def QDR(lineList):
    lineList.insert(3,'0001')
    if not lineList[-2].isspace() and len(lineList[-2].strip())<5:
                lineList[-2]=str(int(area))+lineList[-2].strip()
                lineList[-2]=''+lineList[-2].rjust(24)
    if not lineList[-1].isspace() and len(lineList[-1].strip())<5:
                lineList[-1]=str(int(area))+lineList[-1].strip()
                lineList[-1]=lineList[-1].rjust(24)+'\n'
def CDR(lineList):
    if not lineList[-2].isspace() and len(lineList[-2].rstrip())<5:
                lineList[-2]=str(int(area))+lineList[-2].rstrip()
                lineList[-2]=''+lineList[-2].ljust(24)
def ADR(lineList):
    if not lineList[0].isspace() and len(lineList[0].rstrip())<5:
                lineList[0]=str(int(area))+lineList[0].rstrip()
                lineList[0]=''+lineList[0].ljust(24)

def readXmlConfig(nodeName='CDR'):
    """
     从xml配置文件中读取xpath,area的配置数据.
    """
    global xpath
    global area
    config=ConfigParser.ConfigParser()
    config.readfp(open(os.getcwd()+os.sep+'config.ini'))
    xpath=config.get(nodeName,'xpath')
    area=config.get(nodeName,'area')


if len(sys.argv)==2 :
    readXmlConfig(sys.argv[1])
    print 'read config OK. converting path is %s,area is %s'%(xpath,area)
    fileList=glob.glob(xpath)
    for fileName in fileList:
        newFileName=fileName.replace(sys.argv[1]+os.sep,sys.argv[1]+'NEW'+os.sep)
        if not os.path.exists(os.path.dirname(newFileName)):
            print 'create directory:'+os.path.dirname(newFileName)
            os.makedirs(os.path.dirname(newFileName))
        print newFileName;
        newFile=open(newFileName,'w');
        f=open(fileName)
        for line in f:
            lineList=line.split(';')
            if sys.argv[1]=='QDR' :
                QDR(lineList)
            elif sys.argv[1]=='CDR':
                CDR(lineList)
            elif sys.argv[1]=='ADR':
                ADR(lineList)
            newFile.write(';'.join(lineList))
        newFile.close()
        f.close()
    print '^_^! have converted %s Log!'%sys.argv[1]
else :
   print 'correct param is : convert.py CDR or convert.py QDR or convert.py ADR'
