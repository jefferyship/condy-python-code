#-------------------------------------------------------------------------------
# Name:        EasyExcel
# Purpose:     对Excel常用操作的分子
#
# Author:      林桦
#
# Created:     17/06/2011
# Copyright:   (c) 林桦 2011
# Licence:
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: GBK -*-
from win32com.client import constants, Dispatch
class EasyExcel:
 def __init__(self, filename=None):
    self.xlApp = Dispatch('Excel.Application')
    if filename:
        self.filename = filename
        self.xlBook = self.xlApp.Workbooks.Open(filename)
    else:
       print "please input the filename"

 def close(self):
    self.xlBook.Close(SaveChanges=0)
    del self.xlApp

 def getCell(self, sheet, row, col):
    "获取指定sheet,的指定行，和列的值"
    sht = self.xlBook.Worksheets(sheet)
    return sht.Cells(row, col).Value

 def getRange(self, sheet, row1, col1, row2, col2):
    "返回一个二维数组，return a 2d array (i.e. tuple of tuples)"
    sht = self.xlApp.Worksheets(sheet)
    return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

