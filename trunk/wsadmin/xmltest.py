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
		maxConnections='10'
		try:
			maxConnections=getText(childNode.getElementsByTagName('maxConnections')[0].childNodes)
		except IndexError:
			maxConnections='10'
		minConnections='1'
		try:
			minConnections=getText(childNode.getElementsByTagName('minConnections')[0].childNodes)
		except IndexError:
			minConnections='1'
		connectionTimeout='180'
		try:
			connectionTimeout=getText(childNode.getElementsByTagName('connectionTimeout')[0].childNodes)
		except IndexError:
			connectionTimeout='180'
		print 'nodename=%s,servername=%s,jdbcprovider=%s,jndiName=%s,authDataAlias=%s,url=%s,connectionTimeout=%s'%(nodename,servername,jdbcprovider,jndiName,authDataAlias,url,connectionTimeout)

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
serverName=''
#managerCellName='qzas2CellManager01'
managerCellName='fjastestCellManager01'
jdbcProviderName='Oracle JDBC Driver for 10g'
createFromXml('F:\\python_code\\wsadmin\\websphere.xml')
