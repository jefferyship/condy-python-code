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
serverList=['xm2server1','xm2server2','xm2server3','xm3server1','xm3server2','xm4server1','xm4server2']
dataSourceList=['ECCUCDataSource','ECCIsDataSource','IservUcDS','ReechoDs','ReportDm']
for serverName in serverList:
    for dataSource in dataSourceList:
        print 'start clear serverName:'+serverName+' datasource:'+dataSource
        try:
            conn=AdminControl.completeObjectName('type=DataSource,name='+dataSource+',Server='+serverName+',*');
            AdminControl.invoke(conn,'purgePoolContents','normal');
            print 'end clear serverName:'+serverName+' datasource:'+dataSource+' succss!'
        except:
            print 'end clear serverName:'+serverName+' datasource:'+dataSource+' clear fails!'
