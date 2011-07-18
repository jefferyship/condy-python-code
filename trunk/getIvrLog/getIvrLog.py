#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#   IVR流程日志获取工具。
#   原理：
#       1.根据输入的号码，telnet到CTI服务器上，到CTI的日志中去查找转接到哪一台IVR上。
#       2.然后根据CTI日志上显现的IVR地址，telnet到IVR的服务器上。采用grep '>端口号<'
#         日志文件的方式在IVR上生成日志>sessionNo.log
#       3.FTP到IVR的服务器上，将sessionNo.log下载到本机，并且在IVR上删除sessionNo.log
# Author:      林桦
#
# Created:     12/03/2011
# Copyright:   (c) 林桦 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: GBK -*-


import wx                  # This module uses the new wx namespace
import wx.lib.masked           as masked
import urllib2
import telnetlib
import re
import ConfigParser
import datetime
from ftplib import FTP

#----------------------------------------------------------------------
gbsDescription = u"""\
获取流程日志。先到CTI上查询IVR服务器，然后再telnet到IVR上获取相关端口的流程日志最后，通过FTP将流程日志取回本机.
"""


class TestFrame(wx.Frame):
    def __init__(self):
        self._version='1.0.2'
        tempPath=os.path.split(sys.argv[0])#取文件名的路径。
        if tempPath[0]=='':#文件名采用绝对路径，而是采用相对路径时，取工作目录下的路径
            self.config_dir=os.getcwd()+os.sep
        else:
            self.config_dir=tempPath[0]+os.sep
        self.configDataMap={}

        self.readConfig(self.configDataMap)
        wx.Frame.__init__(self, None, -1, u"IVR流程日志获取工具")
        p = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
                     | wx.CLIP_CHILDREN
                     | wx.FULL_REPAINT_ON_RESIZE
                     )
        p.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        gbs = self.gbs = wx.GridBagSizer(5, 5)

        gbs.Add( wx.StaticText(p, -1, gbsDescription),
                 (0,0), (1,7), wx.ALIGN_LEFT | wx.ALL, 5)


        configKeyList=self.configDataMap.keys()
        nodeidList=[]
        for configKey in configKeyList:
            if configKey.startswith('node_'):nodeidList.append(configKey[5:])
        nodeIdCombox = wx.ComboBox(p, -1, u"CIT节点", wx.DefaultPosition, (100, -1), nodeidList, wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, nodeIdCombox)

        ctiIp=wx.TextCtrl(p, -1, "")
        ctiUser=wx.TextCtrl(p, -1, "")
        ctiPassword=wx.TextCtrl(p, -1, "")
        searchKey=wx.TextCtrl(p, -1, "")
        ctiType=wx.TextCtrl(p, -1, "")
        searchDay= wx.GenericDatePickerCtrl(p, size=(120,-1),
                                style = wx.DP_DROPDOWN
                                      | wx.DP_SHOWCENTURY
                                      | wx.DP_ALLOWNONE )
        searchTime=masked.TimeCtrl(
                                p, -1, name="spinless control",
                                fmt24hr=True,
                                display_seconds = False
                                )
        spin1 = wx.SpinButton( p, -1, wx.DefaultPosition, (-1,searchTime.GetSize().height), wx.SP_VERTICAL )
        searchTime.BindSpinButton(spin1)
        self.ctiIp=ctiIp
        self.ctiUser=ctiUser
        self.ctiPassword=ctiPassword
        self.searchKey=searchKey
        self.searchDay=searchDay
        self.searchTime=searchTime
        self.ctiType=ctiType
        daytimeBox = wx.BoxSizer( wx.HORIZONTAL )
        daytimeBox.Add( searchDay, 0, wx.ALIGN_CENTRE )
        daytimeBox.Add( searchTime, 0, wx.ALIGN_CENTRE )
        daytimeBox.Add( spin1, 0, wx.ALIGN_CENTRE )
        searchTime.SetValue(wx.DateTime_Now())


        searchButton=wx.Button(p, -1, u"查询")
        self.Bind(wx.EVT_BUTTON, self.searchCTI, searchButton)

        gbs.Add( wx.StaticText(p, -1, u'CTI节点:'), (1,0) )
        gbs.Add( nodeIdCombox, (1,1) )
        gbs.Add( wx.StaticText(p, -1, u'CTI_IP:'), (1,3) )
        gbs.Add( ctiIp, (1,4) )
        gbs.Add( wx.StaticText(p, -1, u'CTI用户名:'), (2,0) )
        gbs.Add( ctiUser, (2,1) )
        gbs.Add( wx.StaticText(p, -1, u'CTI密码:'), (2,3) )
        gbs.Add( ctiPassword, (2,4) )
        gbs.Add( wx.StaticText(p, -1, u'查询时间:'), (3,0) )
        gbs.Add( daytimeBox, (3,1) )
        gbs.Add( wx.StaticText(p, -1, u'号码/callSeq:'), (3,3) )
        gbs.Add( searchKey, (3,4) )
        gbs.Add( wx.StaticText(p, -1, u'CTI类型:'), (4,0) )
        gbs.Add( ctiType, (4,1) )
        gbs.Add( searchButton, (4,2) )

        listCtrl = wx.ListCtrl(p, -1, style=wx.LC_REPORT)
        listCtrl.InsertColumn(0, u'呼叫时间', width=60)
        listCtrl.InsertColumn(1, u'呼叫流水',  width=100)
        listCtrl.InsertColumn(2, u'IP地址', width=100)
        listCtrl.InsertColumn(3, u'IVR端口', width=60)
        listCtrl.InsertColumn(4, u'电话号码', width=100)
        listCtrl.InsertColumn(5, u'被叫号码', width=100)
        listCtrl.InsertColumn(6, u'日志时间', width=100)
        self.listCtrl=listCtrl
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listCtrl)
        gbs.Add( listCtrl, (5,0),(6,6),flag=wx.EXPAND )


        self.sessionNo=wx.TextCtrl(p, -1, "")
        self.ivrIp=wx.TextCtrl(p, -1, u"")
        self.ivrUser=wx.TextCtrl(p, -1, u"")
        self.ivrPassword=wx.TextCtrl(p, -1, u"")
        self.ivrPort=wx.TextCtrl(p, -1, '')
        self.ivrLogTime=wx.TextCtrl(p, -1, u"")
        getIvrLogButton=wx.Button(p, -1, u"获取日志")
        self.Bind(wx.EVT_BUTTON, self.getIvrLog, getIvrLogButton)

        gbs.Add( wx.StaticText(p, -1, u'呼叫流水:'), (11,0) )
        gbs.Add( self.sessionNo, (11,1) )
        gbs.Add( wx.StaticText(p, -1, u'ivr地址:'), (11,3) )
        gbs.Add( self.ivrIp, (11,4) )
        gbs.Add( wx.StaticText(p, -1, u'ivr用户名:'), (12,0) )
        gbs.Add( self.ivrUser, (12,1) )
        gbs.Add( wx.StaticText(p, -1, u'Ivr密码:'), (12,3) )
        gbs.Add( self.ivrPassword, (12,4) )
        gbs.Add( wx.StaticText(p, -1, u'ivr端口:'), (13,0) )
        gbs.Add( self.ivrPort, (13,1) )
        gbs.Add( wx.StaticText(p, -1, u'日志时间:'), (13,3) )
        gbs.Add( self.ivrLogTime, (13,4) )
        gbs.Add( getIvrLogButton, (14,2) )

        outputStr=wx.TextCtrl(p, -1, u'ivr地址:',style=wx.TE_MULTILINE)
        #gbs.Add( ivrPassword, (2,7),(2,3),flag=wx.EXPAND )
        gbs.Add( outputStr, (1,6),(12,9),flag=wx.EXPAND )
        self.outputStr=outputStr
        clearOutputStrButton=wx.Button(p, -1, u"清除输出日志")
        self.Bind(wx.EVT_BUTTON, lambda event:outputStr.SetValue(''), clearOutputStrButton)
        gbs.Add( clearOutputStrButton, (13,6) )


        # Add a spacer at the end to ensure some extra space at the bottom
        #gbs.Add((13,1), (14,7))
##
        gbs.AddGrowableRow(3)
        gbs.AddGrowableCol(2)
##
        box = wx.BoxSizer()
        box.Add(gbs, 0, wx.ALL, 10)
##
        p.SetSizerAndFit(box)
        self.SetClientSize(p.GetSize())
        self.version()

    def version(self):
        self.outputStr.SetValue('  getIvrLog.py current version is'+self._version+'\n')
        self.outputStr.AppendText('  author:Condy create time:2011.03.15 modify time:2011.04.26 ')

    def convertUnicodeToStr(self,unicodeMap):
        for key in unicodeMap.keys():
            if isinstance(unicodeMap[key],unicode):#遇到中文关键字，要把unicode类型转换为str类型.
                unicodeMap[key]=unicodeMap[key].encode('GBK')

    def EvtComboBox(self, evt):
        """
          根据选择的CTI列表，自动关联CTI的IP，用户名、密码
        """
        cb = evt.GetEventObject()
        data = cb.GetValue()
        try:
            configData=self.configDataMap['node_'+data]
            self.ctiIp.SetValue(configData['ip'])
            self.ctiUser.SetValue(configData['user'])
            self.ctiPassword.SetValue(configData['password'])
            if configData.has_key('cti_type'):self.ctiType.SetValue(configData['cti_type'])
            else:self.ctiType.SetValue('ctserver')
        except KeyError:
            self.ctiIp.SetValue('')
            self.ctiUser.SetValue('')
            self.ctiPassword.SetValue('')
            self.outputStr.SetValue(u'getIvrLog.ini中找不到node_'+data+u'的配置项,或者是项目没有配置全。必须配置的项目有ip,user,password.')


    def OnItemSelected(self, event):
        """
          将CTI的数据现在在IVR的文本框中.
        """
        currentItem = event.m_itemIndex
        #self.outputStr.SetValue(str(currentItem))
        self.sessionNo.SetValue(self.listCtrl.GetItem(currentItem, 1).GetText())
        self.ivrIp.SetValue(self.listCtrl.GetItem(currentItem, 2).GetText())
        self.ivrPort.SetValue(self.listCtrl.GetItem(currentItem, 3).GetText())
        self.ivrLogTime.SetValue(self.listCtrl.GetItem(currentItem, 6).GetText())
        try:
            configData=self.configDataMap[self.ivrIp.GetValue()]
            print configData
            self.ivrUser.SetValue(configData['user'])
            self.ivrPassword.SetValue(configData['password'])
        except KeyError:
            self.ivrUser.SetValue('')
            self.ivrPassword.SetValue('')
        event.Skip()
    def getIvrLog(self,evt):
        callObject={}
        callObject['ivr_ip']=self.ivrIp.GetValue()
        callObject['ivr_port']=self.ivrPort.GetValue()
        callObject['ivr_user']=self.ivrUser.GetValue()
        callObject['ivr_password']=self.ivrPassword.GetValue()
        callObject['log_time']=self.ivrLogTime.GetValue()
        callObject['sessionNo']=self.sessionNo.GetValue()
        self.convertUnicodeToStr(callObject)
        print callObject
        bResult=self.connectIVR(callObject)
        if bResult:
            bStartReadFlag=False
            bIsFlowDataEndFlag=False
            flowdataLineList=[]
            for lineStr in open(callObject['sessionNo']+'.log','rb').readlines():
                if lineStr.find('RECV UNCC_IAI')<>-1 and lineStr.find(callObject['sessionNo'])<>-1:
                    bStartReadFlag=True
                if bStartReadFlag:
                    flowdataLineList.append(lineStr)
                if bStartReadFlag and lineStr.find('FLOW-END--')<>-1:
                    bIsFlowDataEndFlag=True
                    break
            if bStartReadFlag==True and bIsFlowDataEndFlag==False:#流程日志还未结束
                #在从IVR上获取下一个节点的日志.
                callObject['log_time']=self.getNextLogTime(callObject['log_time'])
                print "callObject['log_time']:"+callObject['log_time']
                bResult=self.connectIVR(callObject)
                if bResult:
                    for lineStr in open(callObject['sessionNo']+'.log','rb').readlines():
                        flowdataLineList.append(lineStr)
                        if lineStr.find('FLOW-END--')<>-1:
                            break
            if len(flowdataLineList)>0:
                flowDataFileObject=open(self.config_dir+callObject['sessionNo']+'.log','wb')
                flowDataFileObject.writelines(flowdataLineList)
                flowDataFileObject.close()


    def getNextLogTime(self,currLogTime):
        """
          获取下个时间片。currLogTime,表示当前时间片，例如:03221330
        """
        currTime=datetime.datetime.today()
        logTimeStr=currTime.strftime('%Y')+currLogTime #yyyymmddhh24mi
        min10=datetime.timedelta(minutes=10)
        logTime=currTime.strptime(logTimeStr,'%Y%m%d%H%M')+min10 #加10分钟
        nextLogTimeStr=logTime.strftime('%m%d%H%M')[:-1]+'0'
        return nextLogTimeStr


    def connectIVR(self,callObject):
        """
        根据呼叫记录，获取IVR上的日志文件。
         callObject['ivr_ip'] :ivr的IP地址
         callObject['ivr_port']:端口
         callObject['ivr_user']:用户名
         callObject['ivr_password']：密码
         callObject['log_time']:日志文件时间
         callObject['sessionNo']:sessionNo


        """
        logPath='/home/'+callObject['ivr_user']+'/LOG/svcsmgr/'
        tn = telnetlib.Telnet(callObject['ivr_ip'])
        tn.set_debuglevel(0)
        tn.read_until("login: ")
        tn.write(callObject['ivr_user'] + "\n")
        expectedList=[]
        expectedList.append("Password:")
        expectedList.append("Password for "+callObject['ivr_user']+": ")
        tn.expect(expectedList,5)
        tn.write(callObject['ivr_password'] + "\n")
        commands=['cd '+logPath,"grep '>"+callObject['ivr_port']+"<' svcsmgr"+callObject['log_time']+".log >"+callObject['sessionNo']+'.log']
        for command in commands:
            tn.write(command+'\n')
        tn.write("exit\n")
        ivrStr= tn.read_all()
        #IVR telnet的新打印到输出窗口
        self.outputStr.SetValue(ivrStr)
        ftp=FTP(callObject['ivr_ip'],callObject['ivr_user'],callObject['ivr_password'])
        fileName=logPath+callObject['sessionNo']+'.log'
        #将保持的路径写到输出窗口
        self.outputStr.AppendText('save file to:'+self.config_dir+os.path.split(fileName)[1])
        ftp.retrbinary('RETR '+fileName,open(self.config_dir+os.path.split(fileName)[1],'wb').writelines)
        ftp.delete(fileName)
        ftp.quit()
        return True
    def readConfig(self,configDataMap):
        """
         从getIvrLog.ini中获取配置信息
         configDataMap必须是dict类型.
        """
        config=ConfigParser.ConfigParser()
        fileObject=open(self.config_dir+'getIvrLog.ini')
        config.readfp(fileObject)
        for section in config.sections():
            configData={}
            for option in config.options(section): configData[option]=config.get(section,option)
            configDataMap[section]=configData


    def connectCTI(self,host):
        """
         从CTI获取IVR的地址，及呼叫的记录
        """
        callObjectList=[]
        tn = telnetlib.Telnet(host['ip'])
        tn.set_debuglevel(0)

        tn.read_until("login: ")
        tn.write(host['user'] + "\n")
        expectedList=[]
        expectedList.append("Password:")
        expectedList.append("Password for "+host['user']+": ")

        tempStr=tn.expect(expectedList,5)
##        tn.read_until("Password for "+host['user']+": ",2)
        tn.write(host['password'] + "\n")

        for command in host['commands']:
            tn.write(command+'\n')

        tn.write("exit\n")
        ctiStr= tn.read_all()
        #将连接的过程写到输出结果框去.
        self.outputStr.SetValue(ctiStr)
        for ctiString in ctiStr.split('\r'):
            if ctiString.find('UNCC_IAI')<>-1 or ctiString.find('UNCC_HLD')<>-1:
                callObject={}
                print ctiString
                callObject['ivr_ip']=re.findall('(\d+\.\d+\.\d+\.\d+)',ctiString)[0]
                callObject['ivr_port']=re.findall('(/\d+)',ctiString)[0].replace('/','')
                callObject['call_time']=re.findall('(\d\d:\d\d)',ctiString)[0]
                callObject['sessionNo']=re.findall('(SessionNo=\d+)',ctiString)[0].replace('SessionNo=','')
                callObject['log_time']=host['log_time']
                try:
                    callObject['call_nbr']=re.findall('(ANI=\d+)',ctiString)[0].replace('ANI=','')
                except IndexError:
                    callObject['call_nbr']=''
                try:
                    callObject['callee_nbr']=re.findall('(DNIS2=\d+)',ctiString)[0].replace('DNIS2=','')
                except IndexError:
                    callObject['callee_nbr']=''
                callObjectList.append(callObject)
        return callObjectList

    def searchCTI(self, evt):
        """
         获取telnet到CTI上的必要信息，及需要在CTI上查询的关键字
        """

        host={}
        host['ip']=self.ctiIp.GetValue()
        host['user']=self.ctiUser.GetValue()
        host['password']=self.ctiPassword.GetValue()
        keyValue=self.searchKey.GetValue()
        if self.searchKey.IsEmpty():
            self.outputStr.SetValue(u"输入查询的号码或流水号.")
            return False
        if self.ctiIp.IsEmpty():
            self.outputStr.SetValue(u"CTI的IP地址为空.")
            return False
        if self.ctiUser.IsEmpty():
            self.outputStr.SetValue(u"CTI的用户名为空")
            return False
        if self.ctiPassword.IsEmpty():
            self.outputStr.SetValue(u"CTI的密码为空")
            return False

        keyDay=self.searchDay.GetValue()
        #生成字符串:yyyymmdd
        log_time=str(keyDay.GetMonth()+1).zfill(2)+str(keyDay.GetDay()).zfill(2)
        keyTime=self.searchTime.GetValue(as_wxDateTime=True)
        #生成字符串:yyyymmddhh24mi
        log_time+=str(keyTime.GetHour()).zfill(2)+str(keyTime.GetMinute()).zfill(2)
        log_time=log_time[:-1]+'0'#分钟的位置更改为10，20分钟等.
        if len(log_time)<>12:
            self.outputStr.SetValue(u"选择查询的日期和时间不对.")

        host['commands']=['cd /home/tnsmcc/LOG/'+self.ctiType.GetValue().encode('GBK'), 'grep '+keyValue.encode('GBK')+' '+self.ctiType.GetValue().encode('GBK')+log_time+'.log']
        host['log_time']=log_time
        self.convertUnicodeToStr(host)
        print host
        callObjectList=self.connectCTI(host)
        self.listCtrl.DeleteAllItems()
        for callObject in callObjectList:
            itemData=(callObject['call_time'],callObject['sessionNo'],callObject['ivr_ip'],callObject['ivr_port'],callObject['call_nbr'],callObject['callee_nbr'],callObject['log_time'])
            print itemData
            self.listCtrl.Append(itemData)



        #测试数据.
##        for i in range(4):
##            itemData=('201103110201','20001110','134.128.196.8','2010','18959130024',log_time)
##            self.listCtrl.Append(itemData)


    def OnHideButton(self, evt):
        self.gbs.Hide(self.hideTxt)
        self.hideBtn.Disable()
        self.showBtn.Enable()
        self.gbs.Layout()


    def OnShowButton(self, evt):
        self.gbs.Show(self.hideTxt)
        self.hideBtn.Enable()
        self.showBtn.Disable()
        self.gbs.Layout()


    def OnMoveButton(self, evt):
        btn = evt.GetEventObject()
        curPos = self.gbs.GetItemPosition(btn)

        # if it's already at the "other" spot then move it back
        if curPos == (3,6):
            self.gbs.SetItemPosition(btn, self.lastPos)
            btn.SetLabel("Move this to (3,6)")
        else:
            if self.gbs.CheckForIntersectionPos( (3,6), (1,1) ):
                wx.MessageBox("""\
wx.GridBagSizer will not allow items to be in the same cell as
another item, so this operation will fail.  You will also get an
assert when compiled in debug mode.""",
                              "Warning", wx.OK | wx.ICON_INFORMATION)

            try:
                if self.gbs.SetItemPosition(btn, (3,6)):
                    self.lastPos = curPos
                    btn.SetLabel("Move it back")
            except wx.PyAssertionError:
                pass

        self.gbs.Layout()


    def OnLeftDown(self, evt):
        pt = evt.GetPosition()
        item = self.gbs.FindItemAtPoint(pt)
        if item is None:
            print "no item at", `pt`
        else:
            print "item found: ", `item.GetPos()`, "--", `item.GetSpan()`





overview = """<html><body>
<h2><center>wx.GridBagSizer</center></h2>

The wx.GridBagSizer is more or less a port of the the RowColSizer (that
has been in the wxPython.lib package for quite some time) to C++.  It
allows items to be placed at specific layout grid cells, and items can
span across more than one row or column.
</body></html>
"""
class MyApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        self.SetTopWindow(frame)

        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True


if __name__ == '__main__':
    import sys,os
##    #fileObject=open('F:\\python_code\\getIvrLog\\00110315145233261381.log','r')
##    fileObject=open('d:\\temp\\1.txt','w')
##    fileObject.write('22222222222222\r\n')
##    fileObject.write(chr(26)+'\r\n')
##    fileObject.write('33333333333333')
##    fileObject.close()
##    fileObject=open('d:\\temp\\1.txt','rb')
##    i=0
##    for line in fileObject:
##        i+=1
##        print str(i)+'******'+line
##    fileObject.close()
    app = MyApp(redirect=True)
    app.MainLoop()



