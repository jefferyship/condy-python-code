# -*- coding: utf-8 -*-
#导入三个模块  
import Image,ImageDraw,ImageFont  
import random  
import math
class TDObject:
    def __init__(self,str,tdPercentWidth):
        self.tdPercentWidth=tdPercentWidth
        self.str=str
        self.align='center'
    def setTdPercentWidth(self,data):
        self.tdPercentWidth=data
    def setStr(self,data):
        self.str=data


'''基本功能'''
#图片宽度  
width = 1100
#图片高度  
height = 400
#背景颜色  
bgcolor = (255,255,255)
#生成背景图片  
image = Image.new('RGBA',(width,height),bgcolor)
#加载字体   原为'FreeSans.ttf' ，我改成了下面这个
font = ImageFont.truetype('simsun.ttc',20)
#字体颜色  
fontcolor = (0,0,0)
#产生draw对象，draw是一些算法的集合  
draw = ImageDraw.Draw(image)
#画字体,(0,0)是起始位置
chinacha = '中国电信客户月计费账单'
draw.text((width/2-5.5*20,0),chinacha.decode('utf-8'),font=font,fill=fontcolor)
draw.line([(10,27),(width-50,27)],fill=fontcolor)
draw.text((10,30),'客户名称:'.decode('utf-8'),font=font,fill=fontcolor)
draw.text((width/3,30),'计费帐期:'.decode('utf-8'),font=font,fill=fontcolor)
draw.text((width/3*2,30),'打印日期:'.decode('utf-8'),font=font,fill=fontcolor)
draw.text((10,60),'客户号码:'.decode('utf-8'),font=font,fill=fontcolor)
draw.line([(10,90),(width-50,90)],fill=fontcolor)
def drawTD(tdStart,tdSize,tdObject):
    try:
        s = unicode(tdObject.str,'utf-8')
    except:
        try:
            s = unicode(tdObject.str, "gbk")
        except:
            pass

    
    #draw.line([(tdStart[0],tdStart[1]),(tdStart[0],tdSize[1]+tdStart[1])],fill=fontcolor)
    if tdObject.align=='center':
        i=0
        for drawstr in s.split('\n'):
            strsize=font.getsize(drawstr)
            draw.text((tdStart[0]+(tdSize[0]-strsize[0])/2,tdStart[1]+(tdSize[1]-strsize[1])/2+i), drawstr, font=font,fill=fontcolor)
            i=i+strsize[1]
        
    elif tdObject.align=='left':
        i=0
        for drawstr in s.split('\n'):
            strsize=font.getsize(drawstr)
            draw.text((tdStart[0],tdStart[1]+(tdSize[1]-strsize[1])/2+i), drawstr, font=font,fill=fontcolor)
            i=i+strsize[1]
    elif tdObject.align=='right':
        i=0
        for drawstr in s.split('\n'):
            strsize=font.getsize(drawstr)
            draw.text((tdStart[0]+tdSize[0]-strsize[0],tdStart[1]+(tdSize[1]-strsize[1])/2+i), drawstr, font=font,fill=fontcolor)
            i=i+strsize[1]
    


    
currPoint=(10,95)
##drawTD(currPoint,((1000-60)*0.35,25),'费用项目')
##currPoint=(currPoint[0]+(1000-60)*0.35,95)
##drawTD(currPoint,((1000-60)*0.15,25),'金额(元)')

def drawTR(trstart,trSize,tdList):
    tempWidth=0;
    tdStart=trstart
    tdSize=()
    for tdObject in tdList:
        tdSize=(trSize[0]*tdObject.tdPercentWidth,trSize[1])
        drawTD(tdStart,tdSize,tdObject)
        tdStart=(tdStart[0]+tdSize[0],tdStart[1])
    draw.line([(trstart[0],trstart[1]+trSize[1]),(trstart[0]+trSize[0],trstart[1]+trSize[1])],fill=fontcolor)
        
        
tdList =[]

tdList.append(TDObject('费用项目',0.35))
tdList.append(TDObject('金额(元)',0.15))
tdList.append(TDObject('费用项目',0.35))
tdList.append(TDObject('金额(元)',0.15))
#tdList.append({'str':'金额(元)','tdPercentWidth':0.15})
#tdList.append({'str':'费用项目','tdPercentWidth':0.35})
#tdList.append({'str':'金额(元)','tdPercentWidth':0.15})
drawTR(currPoint,(width-60,25),tdList)

tdContent=[]
tdObject=TDObject('e家套餐\n  套餐月基本费\n	可选包基本费\n	通话费超出费\n本列小计',0.35)
tdObject.align='left'
tdContent.append(tdObject)
tdObject=TDObject('\n129.00\n6.00\n6.60\n141.60',0.15)
tdObject.align='center'
tdContent.append(tdObject)
tdObject=TDObject('天翼手机:18959130026\n	套餐费\n天翼手机:18959130027\n	短信费\n	彩铃费\n	来电显示功能费\n本列小计',0.35)
tdObject.align='left'
tdContent.append(tdObject)
tdObject=TDObject('\n64.00\n\n2.50\n5.00\n6.00\n77.50	',0.15)
tdObject.align='center'
tdContent.append(tdObject)
currPoint=(10,120)
drawTR(currPoint,(width-60,50),tdContent)
##localWidth=width*0.35/2-draw.textsize('费用项目')[0]/2
##localHeight=95
##draw.text((localWidth,localHeight),'费用项目'.decode('utf-8'),font=font,fill=fontcolor)
##draw.line([(width*0.35,localHeight),(width*0.35,localHeight+10)],fill=fontcolor)
##localWidth=width*0.35+(width*0.15-draw.textsize('金额(元)',font)[0])/2
##print draw.textsize('金额(元)')[0]/2
##draw.line([(width*0.5,localHeight),(width*0.5,localHeight+10)],fill=fontcolor)
##print localWidth
##draw.text((localWidth,localHeight),'金额(元)'.decode('utf-8'),font=font,fill=fontcolor)
##draw.line([(localWidth+157,localHeight),(localWidth+157,localHeight+10)],fill=fontcolor)
##print font.getsize('金')
##print width*0.5-localWidth+draw.textsize('金额(元)')[0]
#释放draw  
del draw
#保存原始版本  
image.save('d:\\temp\\1234_1.tif')  
##'''演示扭曲，需要新建一个图片对象'''
###新图片  
##newImage = Image.new('RGB',(width,height),bgcolor)
###load像素  
##newPix = newImage.load()  
##pix = image.load()  
##offset = 0  
##for y in range(0,height):  
##    offset += 1  
##    for x in range(0,width):
##        #新的x坐标点  
##        newx = x + offset
##        #你可以试试如下的效果
##        #newx = x + math.sin(float(y)/10)*10  
##        if newx < width:                         
##            #把源像素通过偏移到新的像素点  
##            newPix[newx,y] = pix[x,y]
###保存扭曲后的版本              
##newImage.save('d:\\temp\\1234_2.jpeg')  
##'''形变一下'''
###x1 = ax+by+c
###y1 = dx+ey+f  
##newImage = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0))  
##newImage.save('d:\\temp\\1234_3.jpeg')  
##'''画干扰线，别画太多，免得用户都看不清楚'''         
###创建draw，画线用  
##draw = ImageDraw.Draw(newImage)
###线的颜色  
##linecolor= (0,0,0)  
##for i in range(0,15):
##    #都是随机的  
##    x1 = random.randint(0,width)  
##    x2 = random.randint(0,width)  
##    y1 = random.randint(0,height)  
##    y2 = random.randint(0,height)  
##    draw.line([(x1, y1), (x2, y2)], linecolor)             
##             
###保存到本地  
##newImage.save('d:\\temp\\1234_4.jpeg')
