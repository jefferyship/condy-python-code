#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      林桦
#
# Created:     17/06/2011
# Copyright:   (c) 林桦 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: GBK -*-

from EasyExcel import EasyExcel
import os
import sys
import logging
import logging.handlers
if __name__ == '__main__':
    tempPath=os.path.split(sys.argv[0])#取文件名的路径。
    if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
        config_dir=os.getcwd()+os.sep
    else:
        config_dir=tempPath[0]+os.sep
    # set Logger Config
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler(config_dir+'sql.log',maxBytes=2097152,backupCount=5)
    h1.setLevel(logging.INFO)
    f=logging.Formatter('%(message)s')
    h1.setFormatter(f)
    log.addHandler(h1)
    excelProxy=EasyExcel("D:\\temp\\room\\59901.xls")
    room_id='59901'#房间ID，需要手工更改.
    sql="insert into monitor_agent_info (agent_error_type,agent_no,term_id,term_code,node_id,company_id) values ('0','%s','0591%s','%s','0591','1');\ninsert into monitor_room_agent (term_id,room_id,agent_type) values ('0591%s','"+room_id+"','%s');"
    try:
        for iTuple in excelProxy.getRange('Sheet1',1,1,11,15):
            for position in iTuple:
                if isinstance(position,unicode):
                    aData=position.split(';')
                    if len(aData)<3: print aData
                    else:
                        log.info(sql,aData[1],aData[0],aData[0],aData[0],aData[2])


    finally:
        log.info('commit;')
        excelProxy.close()
        h1.close()

