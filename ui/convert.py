#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# 图像是 44行 32列
# 转成 440行 320列

class ConvertProcessDlg(QDialog):
    '''读取数据的对话框'''
    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self.setupUi()
        self.setupLayout()
        self.showUi()
        # 开一个新线程来读数据
        self.convertProcessThread = ConvertProcessThread(self.serial) # 注意self.serial的位置
        self.connectSignalSlot()

    def setupUi(self):
        self.alertLabel = QLabel("采集中,请稍后...\n采集成功后记得先按保存!", self)
        self.readingUselessDataBar = QProgressBar(self)
        self.readingUsefulDataBar = QProgressBar(self)
        self.readingUselessDataBar.setValue(0)
        self.readingUsefulDataBar.setValue(0)

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("读取数据")
        self.setWindowIcon(QIcon("./icons/foot32.png"))
        self.resize(400, 100)
        self.show()

    # 连接
    def connectSignalSlot(self):
        self.convertProcessThread.uselessDataIndexSingal[int].connect(self.refreshUselessDataBar)
        self.convertProcessThread.usefulDataIndexSingal[int].connect(self.refreshUsefulDataBar)

    # 刷新上面那个进度条
    def refreshUselessDataBar(self, value):
        self.readingUselessDataBar.setValue(value)

    # 刷新下面那个进度条
    def refreshUsefulDataBar(self, value):
        self.readingUsefulDataBar.setValue(value)

    # 如果用户直接点红叉关闭
    def closeEvent(self, QCloseEvent):
        if  self.convertProcessThread.isRunning():
            self.convertProcessThread.forceQuitSingal.emit() # 发射'强制退出'信号
            self.convertProcessThread.terminate()
            self.convertProcessThread.quit()

    def setupLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.alertLabel)
        mainLayout.addWidget(self.readingUselessDataBar)
        mainLayout.addWidget(self.readingUsefulDataBar)
        self.setLayout(mainLayout)



class ConvertProcessThread(QThread):
    '''读取数据的新线程'''
    finishConvertSingal =  pyqtSignal() # 数据接收完毕信号
    forceQuitSingal =  pyqtSignal() # 强制退出 数据接收 的信号
    uselessDataIndexSingal = pyqtSignal(int)
    usefulDataIndexSingal = pyqtSignal(int)
    def __init__(self, serial):
        super().__init__()
        self.serial = serial

    # strat后会执行这个函数
    def run(self):
        self.saveImgFromSerial()
        self.finishConvertSingal.emit() # 发射'转换结束'信号

    # 从串口读取数据,保存成png
    def saveImgFromSerial(self):
        bgrPix = np.zeros((44,32,3), np.uint8)# 44行32列，3通道
        # 等待接受到开头
        while True:
            text=self.serial.readline().decode("utf-8")
            print(text)
            if len(text) >= 6:
                try:
                    index = int(text.split(' ')[0])
                    self.uselessDataIndexSingal[int].emit(index//14.1)
                except:
                    print('split err')
                if index == 0:
                    self.uselessDataIndexSingal[int].emit(100)
                    break

        # 保存第一个
        voltage = float(text.split(' ')[1].split('\n')[0])
        bgrPix[0,0,:] = self.voltageToBGR(voltage, 4096)

        # 继续接受
        while True:
            text=self.serial.readline().decode("utf-8")
            print(text)
            index = int(text.split(' ')[0])
            self.usefulDataIndexSingal[int].emit(index // 14.1)
            voltage = float(text.split(' ')[1].split('\n')[0])
            bgrPix[int(index/32),int(index%32),:] = self.voltageToBGR(voltage, 4096)
            if index == 1407:
                self.usefulDataIndexSingal[int].emit(100)
                break

        imgSmall = Image.fromarray(bgrPix)
        imgSmall.save('./footPrints/tempSmall.png')
        imgBig = imgSmall.resize((320, 440))
        imgBig.save('./footPrints/tempBig.png')

    # 0-x 转 (0-x, 0-x, 0-x)
    def grayToBGR(self, gray, scale):
        if gray >= 0 and gray <= scale//4:
            B = 255
        elif gray >= scale//4 and gray <= scale//2:
            B = int(510 - 255 / (scale//4) * gray)
        else:
            B = 0
            
        if gray <= scale//4:
            G = int(255 / (scale//4) * gray)
        elif gray >= scale//4 and gray <= (scale//4)*3:
            G = 255
        else:
            G = int(1020 - 255 / (scale//4) * gray)
            
        if gray <= scale//2:
            R = 0
        elif gray >= scale//2 and gray <= (scale//4)*3:
            R = int(-510 + 255 / (scale//4) * gray)
        else:
            R = 255
        return (B, G, R)

    # 0-3.3 转 0-x
    def voltageToGray(self, voltage, scale):
        return voltage * scale / 3.3

    # 电压转彩色
    def voltageToBGR(self, voltage, scale):
        return (self.grayToBGR(self.voltageToGray(voltage, scale), scale))


