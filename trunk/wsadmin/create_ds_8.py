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
serverList=['fz1server1','fz1server2','fz2server1','fz2server2','fz3server1','fz3server2','fz4server1','fz4server2','fz5server1','ivr-6server1','ivr-6server1']
serverList.append('ivr-6server2')
serverList.append('ivr-6server3')
serverList.append('uc17Server1')
serverList.append('uc17Server2')
serverList.append('uc18Server1')
serverList.append('uc18Server2')
serverList.append('uc19Server1')
serverList.append('uc19Server2')
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
