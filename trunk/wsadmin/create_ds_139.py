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
serverList=['uc13Server1','uc13Server2','uc14Server1','uc14Server2','uc15Server1','uc15Server2','uc16Server1','uc16Server2']
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
