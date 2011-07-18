# -*- coding: utf-8 -*-
import unittest
from com.telthink.link.ServiceUtil import *

class Test(unittest.TestCase):


    def setUp(self):
        self.tables=Tables()
        table=Table()
        table.set_table_index('0')
        row=Row()
        row.set_row_id('0')
        column=Column()
        #column.set_local_index(0)
        column.set_remote_index(0)
        column.set_local_name("aaaaaaaaa")
        #column.set_is_multi('N')
        column.set_what_column('INPUT')
        column.set_service_local_name('column_01')
        column.set_value('aaaaaaaa')
        column1=column.copy()
        column1.set_value('bbbbbb')
        row.set_column_list([column,column1])
        table.set_row_list([row])
        self.tables.set_table_list([table])


    def tearDown(self):
        pass


    def testPrint(self):
        #print self.tables.print_tables()
        inputParam=InputParam()
        serviceInfo=ServiceInfo()
        serviceInfo.set_service_local_name("getServiceInfo")
        serviceInfo.set_service_remote_name("getServiceInfo")
        inputParam.set_service_info(serviceInfo)
        inputParam.set_tables(self.tables)
        print inputParam.print_input_param()
        outputParam=OutputParam()
        outputParam.set_result_code(0)
        outputParam.set_result_message('success')
        outputParam.set_tables(self.tables)
        print outputParam.print_output_param()
        
    def testtablesTostr(self):
        print self.tables.table_to_str()
    def testtablesGetColumn(self):
        print self.tables.get_first_column()
        print self.tables.get_column(0, 0, 1)
    
    def testXmlToInputParam(self):
        xmlString=u'<?xml version="1.0" encoding="GBK"?>  <input_params><service_name>Agent_GetHttpInfo</service_name><company_id>0</company_id><params><tables><table><r><c>059110139</c><c>10139</c></r></table></tables></params></input_params>'
        paramUtil=ParamUtil()
        inputParam=paramUtil.xml_to_input_param(xmlString)
        print inputParam.print_input_param()
    def testXmlToOutputParam(self):
        """
         python不支持GBK的xml,所以都更改成utf-8进行编码
        """
        xmlString='<?xml version="1.0" encoding="GBK"?><output_params> <result_code>0</result_code> <result_msg>调用成功</result_msg> <request_serial>T1292553863703R1081</request_serial> <service_name>Agent_GetHttpInfo</service_name> <params>  <tables>   <table row_num="1">    <r>     <c name="IS_VALID">0</c>     <c name="COMPANY_ID">1</c>     <c name="NEW_TERM_ID" />     <c name="NEW_TERM_SERIAL" />    </r>   </table>   <table row_num="2">    <r>     <c name="SERIAL_NO">0</c>     <c name="SERVICE_IP">134.128.196.10</c>     <c name="SERVICE_PORT">9081</c>     <c name="SERVICE_URL">/iservuc/ServiceGate/SimpleXMLGate</c>     <c name="SERVICE_TEST_URL">/iservuc/soa/test/refreshLink.jsp</c>     <c name="INTERNET_FLAG">0</c>    </r>    <r>     <c>1</c>     <c>134.128.196.10</c>     <c>9081</c>     <c>/iservuc/ServiceGate/SimpleXMLGate</c>     <c>/iservuc/soa/test/refreshLink.jsp</c>     <c>0</c>    </r>   </table>   <table row_num="2">    <r>     <c name="SERIAL_NO">1</c>     <c name="WEB_IP">134.128.196.10</c>     <c name="WEB_PORT">9081</c>     <c name="WEB_URL">/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>     <c name="WEB_TEST_URL">/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>     <c name="INTERNET_FLAG">0</c>     <c name="LOGOUT_URL">http://134.128.196.10:9081/eccuc/login/login.jsp</c>    </r>    <r>     <c>2</c>     <c>134.128.196.10</c>     <c>9081</c>     <c>/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>     <c>/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>     <c>0</c>     <c>http://134.128.196.10:9081/eccuc/login/login.jsp</c>    </r>   </table>   <table row_num="0" />  </tables> </params></output_params>'
        paramUtil=ParamUtil()
        outputParam=paramUtil.xml_to_ouput_param(xmlString)
        print outputParam.print_output_param()
    def testOutputParamToXml(self):
        xmlString='<?xml version="1.0" encoding="GBK"?><output_params> <result_code>0</result_code> <result_msg>调用成功</result_msg> <request_serial>T1292553863703R1081</request_serial> <service_name>Agent_GetHttpInfo</service_name> <params>  <tables>   <table row_num="1">    <r>     <c name="IS_VALID">0</c>     <c name="COMPANY_ID">1</c>     <c name="NEW_TERM_ID" />     <c name="NEW_TERM_SERIAL" />    </r>   </table>   <table row_num="2">    <r>     <c name="SERIAL_NO">0</c>     <c name="SERVICE_IP">134.128.196.10</c>     <c name="SERVICE_PORT">9081</c>     <c name="SERVICE_URL">/iservuc/ServiceGate/SimpleXMLGate</c>     <c name="SERVICE_TEST_URL">/iservuc/soa/test/refreshLink.jsp</c>     <c name="INTERNET_FLAG">0</c>    </r>    <r>     <c>1</c>     <c>134.128.196.10</c>     <c>9081</c>     <c>/iservuc/ServiceGate/SimpleXMLGate</c>     <c>/iservuc/soa/test/refreshLink.jsp</c>     <c>0</c>    </r>   </table>   <table row_num="2">    <r>     <c name="SERIAL_NO">1</c>     <c name="WEB_IP">134.128.196.10</c>     <c name="WEB_PORT">9081</c>     <c name="WEB_URL">/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>     <c name="WEB_TEST_URL">/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>     <c name="INTERNET_FLAG">0</c>     <c name="LOGOUT_URL">http://134.128.196.10:9081/eccuc/login/login.jsp</c>    </r>    <r>     <c>2</c>     <c>134.128.196.10</c>     <c>9081</c>     <c>/eccuc/webmain/mainAction.do?operate=init&amp;STAFF_ID=$(STAFF_ID)&amp;STAFF_NAME=$(STAFF_NAME)&amp;STAFF_NO=$(STAFF_NO)&amp;COMPANY_ID=$(COMPANY_ID)&amp;COMPANY_NAME=$(COMPANY_NAME)&amp;DEPT_ID=$(DEPT_ID)&amp;DEPT_NAME=$(DEPT_NAME)&amp;AREA_CODE=$(AREA_CODE)&amp;WEBSERVER=$(WEBSERVER)&amp;IMR_STATUS=$(IMR_STATUS)&amp;TERM_NO=$(TERM_NO)&amp;EXTEND_STAFF_ID=$(EXTEND_STAFF_ID)&amp;SKIN=$(SKIN)&amp;TAG_ID=$(TAG_ID)&amp;CTI_NODE=$(CTI_NODE)&amp;AGENT_AREA=$(AGENT_AREA)&amp;STAFF_AREA=$(STAFF_AREA)&amp;TAG_NAME=$(TAG_NAME)&amp;STAFF_GROUP_ID=$(STAFF_GROUP_ID)&amp;STAFF_GROUP_NAME=$(STAFF_GROUP_NAME)&amp;IS_MONITOR=$(IS_MONITOR)&amp;CTI_AREA=$(CTI_AREA)</c>     <c>/iservuc/soa/interfaceAction.do?operate=init&amp;detailOpt=query</c>     <c>0</c>     <c>http://134.128.196.10:9081/eccuc/login/login.jsp</c>    </r>   </table>   <table row_num="0" />  </tables> </params></output_params>'
        paramUtil=ParamUtil()
        outputParam=paramUtil.xml_to_ouput_param(xmlString)
        print paramUtil.ouput_param_to_xml(outputParam)
    def testInputParamToXml(self):
        xmlString=u'<?xml version="1.0" encoding="GBK"?>  <input_params><service_name>Agent_GetHttpInfo</service_name><company_id>0</company_id><params><tables><table><r><c>059110139</c><c>10139</c></r></table></tables></params></input_params>'
        paramUtil=ParamUtil()
        inputParam=paramUtil.xml_to_input_param(xmlString)
        print paramUtil.input_param_to_xml(inputParam)
    def testFileOutputParamToXml(self):
        f=open('D:\\temp\\outputParam.xml')
        xmlString=''.join(f.readlines())
        paramUtil=ParamUtil()
        outputParam=paramUtil.xml_to_ouput_param(xmlString)
        print outputParam.get_first_column_value()
        print outputParam.get_column_value(1, 0, 1)
        print outputParam.print_output_param();
        xmlString=paramUtil.ouput_param_to_xml(outputParam)
        print paramUtil.convert_encode(xmlString, 'GBK', 'UTF-8')
    def testServiceInputParam(self):
        url="http://134.128.196.10:9081/iservuc/ServiceGate/SimpleXMLGate"
        paramUtil=ParamUtil()
        #outputParam=paramUtil.invoke("GetServiceInfoUnion", '18959130026', url)
        outputParam=paramUtil.invoke("Agent_GetHttpInfo", '059110139'+LinkConst.SPLIT_COLUMN+'10139', url)
        
        print outputParam.is_success()
        print 'resultCode:%s,resultMsg:%s'%(outputParam.get_result_code(),outputParam.get_result_message())
        #print outputParam.get_column_value(0, 0, 7)
        #print paramUtil.ouput_param_to_xml(outputParam)
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()