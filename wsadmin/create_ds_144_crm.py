#-------------------------------------------------------------------------------
# Name:        clear_datasource
# Purpose:
#
# Author:Condy
#
#WASX7017E: ?????clear_ds_8.py?????????????javax.management.MBeanException
#java.lang.IllegalStateException: java.lang.IllegalStateException: Connection pool is not available.  The connection pool is created at first JNDI lookup of a data source or connection factory.

# Created:     26/04/2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
serverList=['intf1server1','intf1server2','intf1server3','intf2server1','intf2server2','intf2server3']
dataSourceList=['interfaceCrm']
for serverName in serverList:
    for dataSource in dataSourceList:
        print 'start clear serverName:'+serverName+' datasource:'+dataSource
        try:
            conn=AdminControl.completeObjectName('type=DataSource,name='+dataSource+',Server='+serverName+',*');
            AdminControl.invoke(conn,'purgePoolContents','normal');
            print 'end clear serverName:'+serverName+' datasource:'+dataSource+' succss!'
        except:
            print 'end clear serverName:'+serverName+' datasource:'+dataSource+' clear fails!'
