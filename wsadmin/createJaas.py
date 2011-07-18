# -*- coding: GBK -*
import os
def createJDBCProvider(providerName):
    node = AdminConfig.getid('/Cell:'+cellName+'/Node:'+nodeName+'/')
    description=['description',providerName]
    providerType=['providerType','Oracle JDBC Driver']
    implementationClassName=['implementationClassName','oracle.jdbc.pool.OracleConnectionPoolDataSource']
    name=['name',providerName]
    jdbcAttrs = [classpath,description,implementationClassName,name,providerType]
    AdminConfig.create('JDBCProvider', node, jdbcAttrs)
    AdminConfig.save()

def createDataSource(providerName,authDataAlias,jndi,url,maxConn=10,minConn=1,connectionTimeout=3):
    description=''
    jdbcid=''
    if servername=='':
	    jdbcid='/Cell:'+cellName+'/Node:'+nodeName+'/JDBCProvider:'+providerName+'/'
    else:
	    jdbcid='/Cell:'+cellName+'/Node:'+nodeName+'/Server:'+servername+'/JDBCProvider:'+providerName+'/'
    newjdbc = AdminConfig.getid(jdbcid)
    datasourceHelperClassname=['datasourceHelperClassname','com.ibm.websphere.rsadapter.Oracle10gDataStoreHelper']
    dsAttrs = [['description',description],['jndiName',jndi],['name',jndi],['authDataAlias',authDataAlias],['authMechanismPreference','BASIC_PASSWORD'],datasourceHelperClassname]
    newds = AdminConfig.create('DataSource', newjdbc, dsAttrs)
    connectionTimeout=['connectionTimeout',connectionTimeout]
    AdminConfig.create('ConnectionPool', newds, [['maxConnections',maxConn],['minConnections',minConn],connectionTimeout,['purgePolicy','EntirePool']])
    dsPropAttrib = [["name", "URL"], ["type", "java.lang.String"], ["value", url]]
    dsPropSetId = AdminConfig.create("J2EEResourcePropertySet", newds, [])
    AdminConfig.create("J2EEResourceProperty", dsPropSetId, dsPropAttrib)
    AdminConfig.save()
    print 'create datasource '+jndi+' OK!'
    Sync1 = AdminControl.completeObjectName('type=NodeSync,node='+nodeName+',*')
    AdminControl.invoke(Sync1, 'sync')
    print jndi+' '+AdminControl.testConnection(newds)

def createJAASAuthData(alias,userid,password,description=''):
	security=AdminConfig.getid('/Cell:'+cellName+'/Security:/')
	jaasAttrs=[['alias',managerCellName+'/'+alias],['userId',userid],['password',password],['description',description]]
	print jaasAttrs
	AdminConfig.create('JAASAuthData',security,jaasAttrs)
	print 'create JAASAuthData'+alias+' OK!'
	AdminConfig.save()

def modifyJAASAuthData(alias,userid='',password='',description=''):
	jaasAttrs=[]
	if userid<>'':
		jaasAttrs.append(['userId',userid])
	if password<>'':
		jaasAttrs.append(['password',password])
	if description<>'':
		jaasAttrs.append(['description',description])
	print jaasAttrs
	jaasDataList=AdminConfig.list('JAASAuthData').split(os.linesep)
	for jaasData in jaasDataList:
		jassAuthObject=AdminConfig.show(jaasData)
		if jassAuthObject.find(managerCellName+'/'+alias)<>-1:
			print jassAuthObject
			AdminConfig.modify(jaasData,jaasAttrs)
			AdminConfig.save()
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc.encode('ascii','ignore')

def handleJAASAuthDatas(jAASAuthDatasNode):
	jAASAuthDataChildNode=jAASAuthDatasNode.getElementsByTagName('JAASAuthData')
	for childNode in jAASAuthDataChildNode:
		alias=getText(childNode.getElementsByTagName('alias')[0].childNodes)
		userId=getText(childNode.getElementsByTagName('userId')[0].childNodes)
		password=getText(childNode.getElementsByTagName('password')[0].childNodes)
		description=''
		try:
			description=getText(childNode.getElementsByTagName('description')[0].childNodes)
		except IndexError:
			description=''
		print 'alias=%s,userId=%s,password=%s,descrption=%s'%(alias,userId,password,description)
		#createJAASAuthData(alias,userid,password,description)
                
    
def handleJ2EEResourcePropertys(j2EEResourcePropertysNode):
	j2EEResourcePropertyNode=j2EEResourcePropertysNode.getElementsByTagName('J2EEResourceProperty')
	for childNode in j2EEResourcePropertyNode:
		nodename=getText(childNode.getElementsByTagName('nodename')[0].childNodes)
		try:
			servername=getText(childNode.getElementsByTagName('servername')[0].childNodes)
		except IndexError:
			servername=''
		jdbcprovider=getText(childNode.getElementsByTagName('jdbcprovider')[0].childNodes)
		jndiName=getText(childNode.getElementsByTagName('jndiName')[0].childNodes)
		authDataAlias=managerCellName+getText(childNode.getElementsByTagName('authDataAlias')[0].childNodes)
		url=getText(childNode.getElementsByTagName('url')[0].childNodes)
		description=''
		try:
			description=getText(childNode.getElementsByTagName('description')[0].childNodes)
		except IndexError:
			description=''
		maxConnections=10
		try:
			maxConnections=int(getText(childNode.getElementsByTagName('maxConnections')[0].childNodes))
		except IndexError:
			maxConnections=10
		except ValueError:
			maxConnections=10
		minConnections=1
		try:
			minConnections=int(getText(childNode.getElementsByTagName('minConnections')[0].childNodes))
		except IndexError:
			minConnections=1
		except ValueError:
			minConnections=1
		connectionTimeout=180
		try:
			connectionTimeout=int(getText(childNode.getElementsByTagName('connectionTimeout')[0].childNodes))
		except IndexError:
			connectionTimeout=180
		except ValueError:
			connectionTimeout=180
		print 'nodename=%s,servername=%s,jdbcprovider=%s,jndiName=%s,authDataAlias=%s,url=%s,connectionTimeout=%s'%(nodename,servername,jdbcprovider,jndiName,authDataAlias,url,connectionTimeout)
		#createDataSource(providerName,authDataAlias,jndi,url,maxConnections,minConnections,connectionTimeout)

def createFromXml(configFileName):
	 from xml.dom import minidom
	 xmldoc = minidom.parse(configFileName)
	 cellName=getText(xmldoc.getElementsByTagName('cellname')[0].childNodes) 
	 managerCellName=getText(xmldoc.getElementsByTagName('managernodename')[0].childNodes)
	 print 'cellName=%s,managerCellName=%s'%(cellName,managerCellName)

	 for childNode in xmldoc.getElementsByTagName('websphere')[0].childNodes:
		 if childNode.nodeType==childNode.ELEMENT_NODE and childNode.nodeName=='JAASAuthDatas':
			 handleJAASAuthDatas(childNode)
		 elif childNode.nodeType==childNode.ELEMENT_NODE and childNode.nodeName=='J2EEResourcePropertys':
			 handleJ2EEResourcePropertys(childNode)




	
#cellName='qzas2Cell01'
cellName='Dmgr01Cell'
nodeName='qzas1Node01'
servername=''
#managerCellName='qzas2CellManager01'
managerCellName='fjastestCellManager01'
jdbcProviderName='Oracle JDBC Driver for 10g'
#createJDBCProvider(jdbcProviderName)
#createJAASAuthData('condy','condy','condy','condy_test')
#modifyJAASAuthData('condy',description='aaaaaaaa')
createFromXml('F:\\python_code\\wsadmin\\websphere.xml')
url='jdbc:oracle:thin:@(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.210.198)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.210.196)(PORT = 1521)))(CONNECT_DATA =( SERVICE_NAME = FJ1000)))'
# create ActiveMarketDS  
maxConn=20
minConn=1
jndi='ActiveMarketDS'
authDataAlias=managerCellName+'/tccs595'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)

# create reportDm  
maxConn=20
minConn=3
jndi='ReportDm'
authDataAlias=managerCellName+'/dm'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)


# create ReechoDs  
maxConn=10
minConn=1
jndi='ReechoDs'
authDataAlias=managerCellName+'/tccs'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)

# create CustomDataSource  
maxConn=40
minConn=5
jndi='CustomDataSource'
authDataAlias=managerCellName+'/tccs595'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)


# create iservDS  
maxConn=40
minConn=5
jndi='IservDS'
authDataAlias=managerCellName+'/tccs595'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)



# create RepositoryDS  
maxConn=15
minConn=1
jndi='RepositoryDS'
authDataAlias=managerCellName+'/tccs595'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)

# create QuanZhouDS  
maxConn=40
minConn=5
jndi='QuanZhouDS'
url='jdbc:oracle:thin:@134.140.9.35:1521:ora1'
authDataAlias=managerCellName+'/tccsQuanZhou'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)

# create interfaceCrm  
maxConn=15
minConn=1
jndi='interfaceCrm'
authDataAlias=managerCellName+'/base_10000'
url='jdbc:oracle:thin:@(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.128.22)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.128.19)(PORT = 1521)))(CONNECT_DATA =(SERVICE_NAME = crmint)))'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)

# create 20188DS 
maxConn=10
minConn=1
jndi='20188DS'
authDataAlias=managerCellName+'/intf_10000'
url='jdbc:oracle:thin:@(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.130.5)(PORT = 2006))(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.130.8)(PORT = 2006))(LOAD_BALANCE = yes)(CONNECT_DATA =(SERVER = DEDICATED)(SERVICE_NAME = bill)))'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)


# create interfaceTlc  
maxConn=10
minConn=1
jndi='interfaceTlc'
authDataAlias=managerCellName+'/jfcx'
url='jdbc:oracle:thin:@(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.200.21)(PORT = 1521))(ADDRESS = (PROTOCOL = TCP)(HOST = 134.128.200.23)(PORT = 1521)))(CONNECT_DATA =(SERVICE_NAME = jfdb)))'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)


# create broadband  
maxConn=10
minConn=1
jndi='broadband'
authDataAlias=managerCellName+'/SPEECH'
url='jdbc:oracle:thin:@134.128.160.132:1521:pz1'
#createDataSource(jdbcProviderName,authDataAlias,jndi,url,maxConn,minConn)
