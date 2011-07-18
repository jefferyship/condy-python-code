# -*- coding: utf-8 -*-
'''
Created on 2010-2-19

@author: 林桦
'''
from com.telthink.link.Object import Column
from com.telthink.link.Object import Row
from com.telthink.link.Object import InputParam
from com.telthink.link.Object import OutputParam
from com.telthink.link.Object import Table
from com.telthink.link.Object import Tables
from com.telthink.link.Object import LinkConst
from com.telthink.link.Object import ServiceInfo
import urllib2
from xml.dom import minidom
class ParamUtil:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def getText(self,xmlElment):
        """
         获取XML的值
        """
        nodelist=xmlElment.childNodes
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc.decode('utf-8')
    
    def xml_to_ouput_param(self,outputXML):
        """
        <?xml version="1.0" encoding="GBK"?>
<output_params>
 <result_code>0</result_code>
 <result_msg>调用成功</result_msg>
 <request_serial>T1292553863703R1081</request_serial>
 <service_name>Agent_GetHttpInfo</service_name>
 <params>
  <tables>
   <table row_num="1">
    <r>
     <c name="IS_VALID">0</c>
     <c name="COMPANY_ID">1</c>
     <c name="NEW_TERM_ID" />
     <c name="NEW_TERM_SERIAL" />
    </r>
   </table>
   <table row_num="2">
    <r>
     <c name="SERIAL_NO">0</c>
     <c name="SERVICE_IP">134.128.196.10</c>
     <c name="SERVICE_PORT">9081</c>
     <c name="SERVICE_URL">/iservuc/ServiceGate/SimpleXMLGate</c>
     <c name="SERVICE_TEST_URL">/iservuc/soa/test/refreshLink.jsp</c>
     <c name="INTERNET_FLAG">0</c>
    </r>
    <r>
     <c>1</c>
     <c>134.128.196.10</c>
     <c>9081</c>
     <c>/iservuc/ServiceGate/SimpleXMLGate</c>
     <c>/iservuc/soa/test/refreshLink.jsp</c>
     <c>0</c>
    </r>
   </table>
   <table row_num="2">
    <r>
     <c name="SERIAL_NO">1</c>
     <c name="WEB_IP">134.128.196.10</c>
     <c name="WEB_PORT">9081</c>
     <c name="WEB_URL">/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>
     <c name="WEB_TEST_URL">/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>
     <c name="INTERNET_FLAG">0</c>
     <c name="LOGOUT_URL">http://134.128.196.10:9081/eccuc/login/login.jsp</c>
    </r>
    <r>
     <c>2</c>
     <c>134.128.196.10</c>
     <c>9081</c>
     <c>/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>
     <c>/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>
     <c>0</c>
     <c>http://134.128.196.10:9081/eccuc/login/login.jsp</c>
    </r>
   </table>
   <table row_num="0" />
  </tables>
 </params>
</output_params>
        """
        outputParam=OutputParam()
        dom=minidom.parseString(self.convert_encode(outputXML, 'GBK', 'UTF-8'))
        #dom=minidom.parseString(outputXML)
        outputParam.set_request_serial(self.getText(dom.getElementsByTagName('request_serial')[0]))
        outputParam.set_result_code(self.getText(dom.getElementsByTagName('result_code')[0]))
        outputParam.set_result_message(self.getText(dom.getElementsByTagName('result_msg')[0]))
        outputParam.set_service_name(self.getText(dom.getElementsByTagName('service_name')[0]))
        if outputParam.get_result_code()=='0':
            tables=self.xml_to_tables(dom.getElementsByTagName('tables')[0])
            outputParam.set_tables(tables)
        return outputParam
        
    def xml_to_input_param(self,inputXML):
        """
<input_params>
      <service_name></service_name>
      <company_id></company_id>
<params>
 <tables table_num=1>
   <table row_num=1>
    <row  column_num=2>
      <column>
        <column_name></column_name>
        <column_value></column_value>
      </column>
      <column>
        <column_name></column_name>
        <column_value></column_value>
      </column>
    </row>
   <table>
 </tables>
 <params>
</input_params>
     * @param inputXML
        """
        inputParam=InputParam()
        dom=minidom.parseString(self.convert_encode(inputXML, 'GBK', 'UTF-8'))
        serviceInfo=ServiceInfo()
        serviceInfo.set_service_local_name(self.getText(dom.getElementsByTagName('service_name')[0]))
        inputParam.set_service_info(serviceInfo)
        tables=self.xml_to_tables(dom.getElementsByTagName('tables')[0])
        inputParam.set_tables(tables)
        return inputParam
    
    def xml_to_tables(self,tablesElement):
        """
        <tables>
   <table row_num="1">
    <r>
     <c name="IS_VALID">0</c>
     <c name="COMPANY_ID">1</c>
     <c name="NEW_TERM_ID" />
     <c name="NEW_TERM_SERIAL" />
    </r>
   </table>
   <table row_num="2">
    <r>
     <c name="SERIAL_NO">0</c>
     <c name="SERVICE_IP">134.128.196.10</c>
     <c name="SERVICE_PORT">9081</c>
     <c name="SERVICE_URL">/iservuc/ServiceGate/SimpleXMLGate</c>
     <c name="SERVICE_TEST_URL">/iservuc/soa/test/refreshLink.jsp</c>
     <c name="INTERNET_FLAG">0</c>
    </r>
    <r>
     <c>1</c>
     <c>134.128.196.10</c>
     <c>9081</c>
     <c>/iservuc/ServiceGate/SimpleXMLGate</c>
     <c>/iservuc/soa/test/refreshLink.jsp</c>
     <c>0</c>
    </r>
   </table>
   <table row_num="2">
    <r>
     <c name="SERIAL_NO">1</c>
     <c name="WEB_IP">134.128.196.10</c>
     <c name="WEB_PORT">9081</c>
     <c name="WEB_URL">/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>
     <c name="WEB_TEST_URL">/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>
     <c name="INTERNET_FLAG">0</c>
     <c name="LOGOUT_URL">http://134.128.196.10:9081/eccuc/login/login.jsp</c>
    </r>
    <r>
     <c>2</c>
     <c>134.128.196.10</c>
     <c>9081</c>
     <c>/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>
     <c>/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>
     <c>0</c>
     <c>http://134.128.196.10:9081/eccuc/login/login.jsp</c>
    </r>
   </table>
   <table row_num="0" />
  </tables>
  <tables num="1">
   <table index="1" num="1">
    <row index="1" num="4">
     <column index="1" colName="STAFF_NO">000000</column>
     <column index="2" colName="STAFF_PWD">pt10000</column>
     <column index="3" colName="AREA_NO">0595</column>
     <column index="4" colName="TF_NBR"></column>
    </row>
   </table>
  </tables>
     * @param tables
     * @param element
        """
        newTables=Tables()
        tableList=[]
        for tableElement in tablesElement.getElementsByTagName('table'):
            tableList.append(self.xml_to_table(tableElement))
        newTables.set_table_list(tableList)
        return newTables
    def xml_to_table(self,tableElement):
        """
    <table row_num="1">
    <r>
     <c name="IS_VALID">0</c>
     <c name="COMPANY_ID">1</c>
     <c name="NEW_TERM_ID" />
     <c name="NEW_TERM_SERIAL" />
    </r>
   </table>
     * @param tableElement
        """
        table=Table()
        try:
            table.set_row_num(tableElement.attributes['row_num'].value)
        except KeyError:
            table.set_row_num(1)
        rowList=[]
        for rowElement in tableElement.getElementsByTagName('r'):
            rowList.append(self.xml_to_row(rowElement))
        table.set_row_list(rowList)
        return table
    def xml_to_row(self,rowElement):
        """
    <r>
     <c name="IS_VALID">0</c>
     <c name="COMPANY_ID">1</c>
     <c name="NEW_TERM_ID" />
     <c name="NEW_TERM_SERIAL" />
    </r>
        """
        row=Row()
        columnList=[]
        for columnElement in rowElement.getElementsByTagName('c'):
            columnList.append(self.xml_to_column(columnElement))
        row.set_column_list(columnList)
        return row
    def xml_to_column(self,columnElement):
        """
        <c name="IS_VALID">0</c>
        """
        column=Column()
        try:
            column.set_local_name(columnElement.attributes['name'].value)
        except KeyError:
            column.set_local_name('')
        column.set_value(self.getText(columnElement))
        return column
    def input_param_to_xml(self,inputParam):
        """
        
        <?xml version="1.0" encoding="GBK"?>  
          <input_params>
            <service_name>Agent_GetHttpInfo</service_name>
            <company_id>0</company_id>
            <params>
             <tables>
              <table>
               <r>
                <c>059110139</c>
                <c>10139</c>
               </r>
            </table>
        </tables>
     </params>
    </input_params>  
"""
        imp=minidom.getDOMImplementation()
        document=imp.createDocument(None, 'input_params', None)
        rootElement=document.documentElement
        serviceNameElement=document.createElement('service_name')
        serviceNameElement.appendChild(document.createTextNode(str(inputParam.get_service_info().get_service_local_name())))
        rootElement.appendChild(serviceNameElement)
        tablesElement=self.tables_to_xml(inputParam.get_tables(), document)
        paramsElement=document.createElement('params')
        rootElement.appendChild(paramsElement)
        paramsElement.appendChild(tablesElement)
        inputParamXml=rootElement.toxml()
        inputParamXml='<?xml version="1.0" encoding="GBK"?>'+inputParamXml
        return self.convert_encode(inputParamXml, 'UTF-8', 'GBK')
        
    def ouput_param_to_xml(self,outputParam):
        """
        <?xml version="1.0" encoding="GBK"?>
<output_params>
 <request_serial>T1266585475070R1548</request_serial>
 <desc>密码验证</desc>
 <service_name>PwdService</service_name>
 <result_code>0</result_code>
 <result_msg>成功</result_msg>
 <params>
  <tables num="1">
   <table index="1" num="1">
    <row index="1" num="7">
     <column index="1" colName="RESULT">2</column>
     <column index="2" colName="STAFF_ID"></column>
     <column index="3" colName="STAFF_NAME"></column>
     <column index="4" colName="DEPT_ID"></column>
     <column index="5" colName="DEPT_NAME"></column>
     <column index="6" colName="COMPANY_ID"></column>
     <column index="7" colName="COMPANY_NAME"></column>
    </row>
   </table>
  </tables>
 </params>
</output_params>
        """
        imp=minidom.getDOMImplementation()
        document=imp.createDocument(None, 'output_params', None)
        rootElement=document.documentElement
        requestSerialElement=document.createElement('request_serial')
        requestSerialElement.appendChild(document.createTextNode(str(outputParam.get_request_serial())))
        descElement=document.createElement('desc')
        descElement.appendChild(document.createTextNode(str(outputParam.get_desc())))
        serviceNameElement=document.createElement('service_name')
        serviceNameElement.appendChild(document.createTextNode(str(outputParam.get_service_name())))
        resultCodeElement=document.createElement('result_code')
        resultCodeElement.appendChild(document.createTextNode(str(outputParam.get_result_code())))
        resultMsgElement=document.createElement('result_msg')
        resultMsgElement.appendChild(document.createTextNode(str(outputParam.get_result_message())))
        rootElement.appendChild(requestSerialElement)
        rootElement.appendChild(descElement)
        rootElement.appendChild(serviceNameElement)
        rootElement.appendChild(resultCodeElement)
        rootElement.appendChild(resultMsgElement)
        tablesElement=self.tables_to_xml(outputParam.get_tables(), document)
        rootElement.appendChild(tablesElement)
        outputParamXml=rootElement.toxml()
        outputParamXml='<?xml version="1.0" encoding="GBK"?>'+outputParamXml
        return self.convert_encode(outputParamXml, 'UTF-8', 'GBK')
        
        
    def tables_to_xml(self,tables,document):
        """
        <tables>
              <table>
               <r>
                <c>059110139</c>
                <c>10139</c>
               </r>
            </table>
        </tables>
        """
        tablesElement=document.createElement('tables')
        if tables<>None :
            for table in tables.get_table_list():
                tableElement=self.table_to_xml(table,document)
                tablesElement.appendChild(tableElement)
        return tablesElement
    def table_to_xml(self,table,document):
        """
        <table>
               <r>
                <c>059110139</c>
                <c>10139</c>
               </r>
            </table>
        """
        tableElement=document.createElement('table')
        tableElement.setAttribute('row_num',str(table.get_row_num()))
        for row in table.get_row_list():
            rowElement=self.row_to_xml(row,document)
            tableElement.appendChild(rowElement)
        return tableElement
    def row_to_xml(self,row,document):
        """
               <r>
                <c>059110139</c>
                <c>10139</c>
               </r>
        """
        rowElement=document.createElement('r')
        for column in row.get_column_list():
            columnElement=self.column_to_xml(column,document)
            rowElement.appendChild(columnElement)
        return rowElement
    def column_to_xml(self,column,document):
        """
         <c>059110139</c>
        """
        columnElement=document.createElement('c')
        columnElement.appendChild(document.createTextNode(str(column.get_value())))
        return columnElement
    def convert_encode(self,xmlString,srcEncode,destEncode):
        """
        由于minDom不支持GBK编码，所以输入时GBK编码的要求转化为UTF-8
         将xmlString 从原来的GBK,UTF-8编码，转化为UTF-8编码，或GBK编码
        """
        xml=xmlString.replace('encoding="'+srcEncode+'"', 'encoding="'+destEncode+'"')
        xml=xml.decode(srcEncode).encode(destEncode)
        return xml
    def strToTables(self,inputStr):
        tableStrList=inputStr.split(LinkConst.SPLIT_TABLE)
        tableList=[]
        tables=Tables()
        
        for tableStr in tableStrList:
            table=Table()
            tableList.append(table)
            rowStrList=tableStr.split(LinkConst.SPLIT_ROW)
            rowList=[]
            for rowStr in rowStrList:
                row=Row()
                rowList.append(row)
                columnStrList=rowStr.split(LinkConst.SPLIT_COLUMN)
                columnList=[]
                for columnStr in columnStrList:
                    column=Column()
                    column.set_value(columnStr)
                    columnList.append(column)
                row.set_column_list(columnList)
            table.set_row_list(rowList)
        tables.set_table_list(tableList)
        return tables
            
            
    def invoke(self,serviceName,inputStr,serviceUrl):
        """
        调用服务的方法,
        @ serviceName 调用的服务名
        @ inputStr column1||chr(1)||column2||chr(1)||column2||chr(3)||column1
        @ return  OutputParam对象.
        """
        inputParam=InputParam()
        serviceInfo=ServiceInfo()
        serviceInfo.set_service_local_name(serviceName)
        inputParam.set_service_info(serviceInfo)
        tables=self.strToTables(inputStr)
        inputParam.set_tables(tables)
        inputXML=self.input_param_to_xml(inputParam)
        f=urllib2.urlopen(serviceUrl, "xmldata="+inputXML)
        outputXML=f.read()
        outputXML=outputXML.lstrip()
        outputParam=self.xml_to_ouput_param(outputXML)
        return outputParam
        
            
        
        
        
        
    
        