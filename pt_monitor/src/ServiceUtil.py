# -*- coding:GBK -*-
'''
Created on 2010-2-19

@author: ����
'''
import copy
class LinkConst:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    SPLIT_COLUMN=chr(1)
    SPLIT_ROW=chr(2)
    SPLIT_TABLE=chr(3)
class Column:
    '''
    �����Column���󡣴�java�汾��com.telthink.link/Column.javaת������.
    '''


    def __init__(self):
        '''
        ���캯��
        '''
        self.init_local_variable()

    def init_local_variable(self):
        self.__service_local_name=None
        self.__remote_name=None
        self.__remote_Index=None
        self.__length=None
        self.__need_decode=None
        self.__table_index=None
        self.__table_name=None
        self.__is_multi=None
        self.__desc=None
        self.__value=None
        self.__what_column=None
        self.__localIndex=None
        self.__localName=None
    def get_service_local_name(self):
        return self.__serviceLocalName


    def set_service_local_name(self, value):
        self.__serviceLocalName = value


    def del_service_local_name(self):
        del self.__serviceLocalName


    def get_remote_name(self):
        return self.__remoteName


    def get_remote_index(self):
        return self.__remote_Index


    def get_length(self):
        return self.__length


    def get_need_decode(self):
        return self.__needDecode


    def get_table_index(self):
        return self.__tableIndex


    def get_table_name(self):
        return self.__tableName


    def get_is_multi(self):
        return self.__isMulti


    def get_desc(self):
        return self.__desc


    def get_value(self):
        return self.__value


    def get_what_column(self):
        return self.__whatColumn


    def set_remote_name(self, value):
        self.__remoteName = value


    def set_remote_index(self, value):
        self.__remote_Index = value


    def set_length(self, value):
        self.__length = value


    def set_need_decode(self, value):
        self.__needDecode = value


    def set_table_index(self, value):
        self.__tableIndex = value


    def set_table_name(self, value):
        self.__tableName = value


    def set_is_multi(self, value):
        self.__isMulti = value


    def set_desc(self, value):
        self.__desc = value


    def set_value(self, value):
        self.__value = value


    def set_what_column(self, value):
        self.__whatColumn = value


    def del_remote_name(self):
        del self.__remoteName


    def del_remote_index(self):
        del self.__remote_Index


    def del_length(self):
        del self.__length


    def del_need_decode(self):
        del self.__needDecode


    def del_table_index(self):
        del self.__tableIndex


    def del_table_name(self):
        del self.__tableName


    def del_is_multi(self):
        del self.__isMulti


    def del_desc(self):
        del self.__desc


    def del_value(self):
        del self.__value


    def del_what_column(self):
        del self.__whatColumn


    def get_local_index(self):
        return self.__localIndex


    def set_local_index(self, value):
        self.__localIndex = value


    def del_local_index(self):
        del self.__localIndex


    def get_local_name(self):
        return self.__localName


    def set_local_name(self, value):
        self.__localName = value


    def del_local_name(self):
        del self.__localName

    localName = property(get_local_name, set_local_name, del_local_name, "�б�������")
    localIndex = property(get_local_index, set_local_index, del_local_index, "�б������")
    remoteName = property(get_remote_name, set_remote_name, del_remote_name, "��Զ������")
    remoteIndex = property(get_remote_index, set_remote_index, del_remote_index, "��Զ�����")
    length = property(get_length, set_length, del_length, "�����ͣ�date,string,int")
    needDecode = property(get_need_decode, set_need_decode, del_need_decode, "���Ƿ���Ҫ����")
    tableIndex = property(get_table_index, set_table_index, del_table_index, "������������")
    tableName = property(get_table_name, set_table_name, del_table_name, "�������������")
    isMulti = property(get_is_multi, set_is_multi, del_is_multi, "���Ƿ����ڶ���")
    desc = property(get_desc, set_desc, del_desc, "������")
    value = property(get_value, set_value, del_value, "��ֵ")
    whatColumn = property(get_what_column, set_what_column, del_what_column, "ʲô�У������л������")
    serviceLocalName = property(get_service_local_name, set_service_local_name, del_service_local_name, "�������ķ��񱾵�����")
    def copy(self):
        """
         * ������
     * @return Column
        """
        newColumn=copy.copy(self)
        newColumn.init_local_variable()
        return newColumn
    def str_to_Column(self,column,columnValue):
        """
        * ���������ַ�����������
     * @param srcColumn ԭ��
     * @param newColumnStr �����ַ���
     * @return ����
        """
        newColumn=column.copy()
        newColumn.set_value(columnValue)
        return newColumn

    def column_to_str(self):
        return str(self.__value)

    def print_column(self):
        printList=[]
        printList.append("local_index="+str(self.get_local_index()))
        printList.append("remote_index="+str(self.get_remote_index()))
        printList.append("local_name="+str(self.get_local_name()))
        printList.append("value="+str(self.get_value()))
        return "\t\t\t\tcolumn: "+','.join(printList)
class Row:
    '''
        �����Row���󡣴�java�汾��com.telthink.link.Row.javaת������.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__columnList=None
        self.__columnNum=None
        self.__rowId=None
        self.__linkConst=LinkConst()

    def get_row_id(self):
        return self.__rowId


    def get_column_num(self):
        return self.__columnNum


    def get_column_list(self):
        if self.__columnList==None:
            return []
        else:
            return self.__columnList


    def set_row_id(self, value):
        self.__rowId = value


    def set_column_num(self, value):
        self.__columnNum = value


    def set_column_list(self, value):
        self.set_column_num(len(value))
        self.__columnList = value


    def del_row_id(self):
        del self.__rowId


    def del_column_num(self):
        del self.__columnNum


    def del_column_list(self):
        del self.__columnList

    rowId = property(get_row_id, set_row_id, del_row_id, "�б��")
    columnNum = property(get_column_num, set_column_num, del_column_num, "������")
    columnList = property(get_column_list, set_column_list, del_column_list, "���б�")

    def add_column(self,column):
        self.get_column_list().append(column)
        self.set_column_list(self.get_column_list())
    def has_column(self):
        """
        * ���Ƿ�����
        * @return �Ƿ�����
        """
        if len(self.__columnList)>0:
            return True
        else:
            return False
    def get_one_column(self,column_index):
        """
         * ������ȡһ��
         * @param column_index �ڼ���
         * @return Column Object
        """
        return self.__columnList[column_index]
    def get_first_column(self):
        """
         * ������ȡ��һ��
         * @return Column����
        """
        return self.get_one_column(0)

    def copy(self):
        """
        * ������
        * @return ����
        """
        newRow=copy.copy(self)
        for column in self.__columnList:
            newColumn=column.copy()
            newRow.add_column(newColumn)
        return newRow

    def str_to_row(self,rowStr):
        aColumnValue=rowStr.split(self.__linkConst.SPLIT_COLUMN)
        i=0
        for column in self.__columnList:
            try:
                column.set_value(aColumnValue[i])
            except IndexError:
                column.set_value('')
            i=i+1
        return i;
    def row_to_str(self):
        strList=[]
        for column in self.__columnList:
            strList.append(column.column_to_str())
        return self.__linkConst.SPLIT_COLUMN.join(strList)

    def print_row(self):
        printList=[]
        printList.append("row_id="+str(self.__rowId)+',')
        printList.append("column_num="+str(self.__columnNum)+'\n')
        for column in self.__columnList:
            printList.append(column.print_column()+'\n')
        return "\t\t\trow: "+''.join(printList)
class Table:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__is_multi=None
        self.__table_Index=None
        self.__table_name=None
        self.__row_num=None
        self.__column_num=None
        self.__row_list=None
        self.__linkConst=LinkConst()

    def get_is_multi(self):
        return self.__isMulti


    def get_table_index(self):
        return self.__table_Index


    def get_table_name(self):
        return self.__tableName


    def get_row_num(self):
        return self.__rowNum


    def get_column_num(self):
        return self.__columnNum


    def get_row_list(self):
        return self.__rowList


    def set_is_multi(self, value):
        if value=='Y':
            self.__isMulti=True
        else:
            self.__isMulti = False


    def set_table_index(self, value):
        self.__table_Index = value


    def set_table_name(self, value):
        self.__tableName = value


    def set_row_num(self, value):
        self.__rowNum = value


    def set_column_num(self, value):
        self.__columnNum = value


    def set_row_list(self, value):
        self.set_row_num(len(value))
        try:
            self.set_column_num(value[0].get_column_num())
        except IndexError:
            self.set_column_num(0)
        self.__rowList = value


    def del_is_multi(self):
        del self.__isMulti


    def del_table_index(self):
        del self.__table_Index


    def del_table_name(self):
        del self.__tableName


    def del_row_num(self):
        del self.__rowNum


    def del_column_num(self):
        del self.__columnNum


    def del_row_list(self):
        del self.__rowList

    isMulti = property(get_is_multi, set_is_multi, del_is_multi, "�Ƿ����")
    tableIndex = property(get_table_index, set_table_index, del_table_index, "�����")
    tableName = property(get_table_name, set_table_name, del_table_name, "������")
    rowNum = property(get_row_num, set_row_num, del_row_num, "����")
    columnNum = property(get_column_num, set_column_num, del_column_num, "����")
    rowList = property(get_row_list, set_row_list, del_row_list, "���б�")

    def has_row(self):
        """
        * ���Ƿ�����
        * @return �Ƿ�����
        """
        if len(self.__rowList)>0:
            return True
        else:
            return False

    def copy(self):
        newTable=copy.copy(self)
        newRowList=[]
        for row in self.__rowList:
            newRowList.append(row.copy())
        newTable.set_row_list(newRowList)
        return newTable
    def str_to_table(self,tablestr):
        aTableStrList=tablestr.split(self.__linkConst.SPLIT_ROW)
        i=0
        newRowList=[]
        if self.__rowNum>0:
            newRow=self.__rowList[0].copy()
        if self.get_is_multi():
            try:
                totalColumnNum=len(aTableStrList[0].split(self.__linkConst.SPLIT_COLUMN))
            except IndexError:
                totalColumnNum=0
            while i<totalColumnNum:
                i=i+newRow.str_to_row(aTableStrList[i:])
                newRowList.append(newRow)
                newRow.set_row_id(i)
                newRow=newRow.copy()
        else:
            newRow.str_to_row(aTableStrList)
            newRowList.append(newRow)
            newRow.set_row_id(0)
    def table_to_str(self):
        tablestrList=[]
        for row in self.__rowList:
            tablestrList.append(row.row_to_str())
        return self.__linkConst.SPLIT_ROW.join(tablestrList)

    def get_one_row(self,rowIndex):
        try:
            return self.__rowList[rowIndex]
        except IndexError:
            return None
    def get_first_row(self):
        return self.get_one_row(0)

    def print_table(self):
        printList=[]
        printList.append("table_index="+str(self.get_table_index())+'\n')
        for row in self.__rowList:
            printList.append(row.print_row())
        return "\t\ttable: "+''.join(printList)
class Tables:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__tableList=''
        self.__tableNum='0'
        self.__linkConst=LinkConst()

    def get_table_num(self):
        return self.__tableNum


    def get_table_list(self):
        return self.__tableList


    def set_table_num(self, value):
        self.__tableNum = value


    def set_table_list(self, value):
        self.set_table_num(len(value))
        self.__tableList = value


    def del_table_num(self):
        del self.__tableNum


    def del_table_list(self):
        del self.__tableList

    tableNum = property(get_table_num, set_table_num, del_table_num, "������")
    tableList = property(get_table_list, set_table_list, del_table_list, "���б�")

    def has_table(self):
        """
        * ���Ƿ��б�
        * @return �Ƿ��б�
        """
        if len(self.__tableList)>0:
            return True
        else:
            return False

    def copy(self):
        newTables=copy.copy(self)
        tableList=[]
        for table in self.__tableList:
            tableList.append(table.copy())
        newTables.set_table_list(tableList)
        return newTables

    def table_to_str(self):
        """
     * ���ݱ�Ⱥ������Ⱥ�ַ���
     * @return ��Ⱥ�ַ���
        """
        tablesStrList=[]
        for table in self.__tableList:
            tablesStrList.append(table.table_to_str())
        return self.__linkConst.SPLIT_TABLE.join(tablesStrList)

    def get_one_table(self,tableIndex):
        try:
            return self.__tableList[tableIndex]
        except IndexError:
            return None

    def get_first_table(self):
        return self.get_one_table(0)

    def print_tables(self):
        printList=[]
        printList.append("table_num="+str(self.get_table_num())+"\n")
        for table in self.__tableList:
            printList.append(table.print_table())
        return "\ttables: "+''.join(printList)

    def get_row(self,tableNo,rowNo):
        try:
            return self.get_one_table(tableNo).get_one_row(rowNo)
        except IndexError:
            return None
        except AttributeError:
            return None
    def get_column(self,tableNo,rowNo,columnNo):
        try:
            return self.get_row(tableNo, rowNo).get_one_column(columnNo)
        except IndexError:
            return None
        except AttributeError:
            return None

    def get_first_column(self):
        return self.get_column(0,0,0)
    def get_first_row(self):
        return self.get_row(0,0)

class ServiceInfo:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.init_local_variable()

    def init_local_variable(self):
        self.__serviceLocalName=None
        self.__serviceRemoteName=None
        self.__serviceClass=None
        self.__serviceAttach=None
        self.__user=None
        self.__pwd=None
        self.__desc=None
        self.__callType='0'
        self.__desc=None
        self.__isLog='0'

    def get_service_local_name(self):
        return self.__serviceLocalName


    def get_service_remote_name(self):
        return self.__serviceRemoteName


    def get_service_class(self):
        return self.__serviceClass


    def get_service_attach(self):
        return self.__serviceAttach


    def get_user(self):
        return self.__user


    def get_pwd(self):
        return self.__pwd


    def get_desc(self):
        return self.__desc


    def get_call_type(self):
        return self.__callType


    def get_is_log(self):
        return self.__isLog


    def set_service_local_name(self, value):
        self.__serviceLocalName = value


    def set_service_remote_name(self, value):
        self.__serviceRemoteName = value


    def set_service_class(self, value):
        self.__serviceClass = value


    def set_service_attach(self, value):
        self.__serviceAttach = value


    def set_user(self, value):
        self.__user = value


    def set_pwd(self, value):
        self.__pwd = value


    def set_desc(self, value):
        self.__desc = value


    def set_call_type(self, value):
        self.__callType = value


    def set_is_log(self, value):
        self.__isLog = value
    serviceLocalName = property(get_service_local_name, set_service_local_name, None, "���񱾵�����")
    serviceRemoteName = property(get_service_remote_name, set_service_remote_name, None, "����Զ������")
    serviceClass = property(get_service_class, set_service_class, None, "�ӿ�ʵ����")
    serviceAttach = property(get_service_attach, set_service_attach, None, "���񸽼Ӳ����������CallFunctionImpl������JNDI")
    user = property(get_user, set_user, None, "�û���")
    pwd = property(get_pwd, set_pwd, None, "����")
    desc = property(get_desc, set_desc, None, "��������")
    callType = property(get_call_type, set_call_type, None, "��������,Ĭ��Ϊ0")
    isLog = property(get_is_log, set_is_log, None, "�Ƿ�д��־��0-��д��־��Ĭ�ϣ���1-д��־")
    def copy(self):
        newServiceInfo=copy.copy(self)
        newServiceInfo.init_local_variable()
        return newServiceInfo
    def print_service_info(self):
        printList=[]
        printList.append("service_local_name="+str(self.get_service_local_name()))
        printList.append("service_remote_name="+str(self.get_service_remote_name())+'\n')
        return "\t"+','.join(printList)

class InputParam:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.init_local_variable()

    def get_request_serial(self):
        return self.__requestSerial


    def get_service_info(self):
        return self.__serviceInfo


    def get_tables(self):
        return self.__tables


    def get_caller_ip(self):
        return self.__callerIp


    def set_request_serial(self, value):
        self.__requestSerial = value


    def set_service_info(self, value):
        self.__serviceInfo = value


    def set_tables(self, value):
        self.__tables = value


    def set_caller_ip(self, value):
        self.__callerIp = value


    def init_local_variable(self):
        self.__requestSerial=None
        self.__serviceInfo=None
        self.__tables=None
        self.__callerIp=None
    requestSerial = property(get_request_serial, set_request_serial, None, "������źţ�T + ʱ��long + R + ��λ�����")
    serviceInfo = property(get_service_info, set_service_info, None, "������Ϣ")
    tables = property(get_tables, set_tables, None, "���������Ⱥ")
    callerIp = property(get_caller_ip, set_caller_ip, None, "������IP")

    def print_input_param(self):
        printList=[]
        printList.append("InputParam: request_serial="+str(self.get_request_serial())+"\n")
        printList.append(self.get_service_info().print_service_info())
        printList.append(self.get_tables().print_tables())
        return ''.join(printList)
class OutputParam:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.init_local_variable()

    def get_tables(self):
        return self.__tables


    def set_tables(self, value):
        self.__tables = value


    def get_request_serial(self):
        return self.__requestSerial


    def set_request_serial(self, value):
        self.__requestSerial = value


    def get_result_code(self):
        return self.__resultCode


    def get_result_message(self):
        return self.__resultMessage


    def get_desc(self):
        return self.__desc


    def get_service_name(self):
        return self.__serviceName


    def set_result_code(self, value):
        self.__resultCode = value


    def set_result_message(self, value):
        self.__resultMessage = value


    def set_desc(self, value):
        self.__desc = value


    def set_service_name(self, value):
        self.__serviceName = value

    resultCode = property(get_result_code, set_result_code, None, "�����")
    resultMessage = property(get_result_message, set_result_message, None, "�����Ϣ")
    desc = property(get_desc, set_desc, None, "����")
    serviceName = property(get_service_name, set_service_name, None, "������")
    requestSerial = property(get_request_serial, set_request_serial, None, "������źţ�T + ʱ��long + R + ��λ�����")
    def is_success(self):
        """
         * �жϵ��÷����Ƿ�ɹ�
         * @return Ture/Fale
            """
        return self.__resultCode=='0';
    def get_first_column_value(self):
        """
        * ��ȡ��һ���е�ֵ
        """
        return self.__tables.get_first_column().get_value()
    def get_column_value(self,tableNo=0,rowNo=0,columnNo=0):
        """
        ��ȡĳ���е�ֵ
        """
        return self.__tables.get_column(tableNo,rowNo,columnNo).get_value()

    def print_output_param(self):
        printList=[]
        printList.append("OutputParam: request_serial="+str(self.get_request_serial())+"\n")
        printList.append("\t result_code="+str(self.get_result_code())+',')
        printList.append("\t result_message=="+str(self.get_result_message()))
        printList.append(self.get_tables().print_tables())
        return ''.join(printList)
    tables = property(get_tables, set_tables, None, "tables's docstring")
    def init_local_variable(self):
        self.__tables=None
        self.__requestSerial=None
        self.__resultCode=None
        self.__resultMessage=None
        self.__serviceName=None
        self.__desc=None

import urllib2
import urllib
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
         ��ȡXML��ֵ
        """
        nodelist=xmlElment.childNodes
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        #return rc
##        try:
##            rc=rc.decode('GBK')
##        except UnicodeDecodeError:
##            pass
        return rc

    def xml_to_ouput_param(self,outputXML):
        """
        <?xml version="1.0" encoding="GBK"?>
<output_params>
 <result_code>0</result_code>
 <result_msg>���óɹ�</result_msg>
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
        #return self.convert_encode(inputParamXml, 'UTF-8', 'GBK')
        return inputParamXml

    def ouput_param_to_xml(self,outputParam):
        """
        <?xml version="1.0" encoding="GBK"?>
<output_params>
 <request_serial>T1266585475070R1548</request_serial>
 <desc>������֤</desc>
 <service_name>PwdService</service_name>
 <result_code>0</result_code>
 <result_msg>�ɹ�</result_msg>
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
        ����minDom��֧��GBK���룬��������ʱGBK�����Ҫ��ת��ΪUTF-8
         ��xmlString ��ԭ����GBK,UTF-8���룬ת��ΪUTF-8���룬��GBK����
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
        ���÷���ķ���,

        @ serviceName ���õķ�����
        @ inputStr encode������Ҫ��GBK���롣column1||chr(1)||column2||chr(1)||column2||chr(3)||column1
        @ return  OutputParam����.
        """
        inputParam=InputParam()
        serviceInfo=ServiceInfo()
        serviceInfo.set_service_local_name(serviceName)
        inputParam.set_service_info(serviceInfo)
        tables=self.strToTables(inputStr)
        inputParam.set_tables(tables)
        inputXML=self.input_param_to_xml(inputParam)
        outputParam=None
        try:
            f=urllib2.urlopen(serviceUrl,urllib.urlencode({'xmldata':inputXML}))
            outputXML=f.read()
            outputXML=outputXML.lstrip()
            #print outputXML
            outputParam=self.xml_to_ouput_param(outputXML)
        except Exception:
            outputParam=OutputParam()
            outputParam.set_result_code('-1')
            outputParam.set_result_message('���÷����ַ:'+serviceUrl+"ʧ��")
            outputParam.set_service_name(serviceName)
        return outputParam
