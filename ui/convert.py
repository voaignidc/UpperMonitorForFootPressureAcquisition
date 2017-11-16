#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# 图像是 44行 32列
# 转成 440行 320列

# 读取数据的对话框
class ConvertProcessDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.alertLabel = QLabel("请稍后", self)
        self.readUselessDataBar = QProgressBar(self)
        self.readUsefulDataBar = QProgressBar(self)
        self.readUselessDataBar.setValue(0)
        self.readUsefulDataBar.setValue(0)
        self.setupLayout()
        self.setWindowTitle("读取数据")
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.resize(400, 100)

    def setupLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.alertLabel)
        mainLayout.addWidget(self.readUselessDataBar)
        mainLayout.addWidget(self.readUsefulDataBar)
        self.setLayout(mainLayout)


# 读取数据的新线程
class ConvertProcessThread(QThread):
    finishConvertSingal =  pyqtSignal() # 结束信号
    def __init__(self, serial):
        super().__init__()
        self.serial = serial

    def run(self):
        self.saveImgFromSerial()
        self.finishConvertSingal.emit()

    # 0-255 转 (0-255, 0-255, 0-255)
    def grayToBGR(self, gray):
        if gray >= 0 and gray <= 85:
            B = int(255 / 85 * gray)
        elif gray >= 85 and gray <= 170:
            B = int(510 - 510 / 170 * gray)
        else:
            B = 0
        if gray <= 85:
            G = 0
        elif gray >= 85 and gray <= 170:
            G = int(-255 + 510 / 170 * gray)
        elif gray >= 170 and gray <= 255:
            G = int(765 - 765 / 255 * gray)
        if gray <= 170:
            R = 0
        else:
            R = int(-510 + 510 / 170 * gray)
        return (B, G, R)

    # 0-3.3 转 0-255
    def voltageToGray(self, voltage):
        return voltage*255/3.3

    # 电压转彩色
    def voltageToBGR(self, voltage):
        return(self.grayToBGR(self.voltageToGray(voltage)))

    # 从串口读取数据,返回图像的np.array
    def saveArrayFromSerial(self):
        bgrPix = np.zeros((44, 32, 3), np.uint8)  # 44行32列，3通道
        # 等待接受到开头
        while True:
            text = self.serial.readline().decode("utf-8")
            print(text)
            try:
                index = int(text.split(' ')[0])
            except:
                print('split err')
            if index == 0:
                break

        # 保存第一个
        voltage = float(text.split(' ')[1].split('\n')[0])
        bgrPix[0, 0, :] = self.voltageToBGR(voltage)

        # 继续接受
        while True:
            text = self.serial.readline().decode("utf-8")
            print(text)
            index = int(text.split(' ')[0])
            voltage = float(text.split(' ')[1].split('\n')[0])
            bgrPix[int(index / 32), int(index % 32), :] = self.voltageToBGR(voltage)
            if index == 1407:
                break

        return bgrPix

    # 把np.array转图像并保存
    def saveImgFromArray(self, pixArray):
        imgSmall = Image.fromarray(pixArray)
        imgBig = imgSmall.resize((320, 440))
        imgBig.save('../footPrints/temp.png')

    # 从串口读取数据,保存成png
    def saveImgFromSerial(self):
        bgrPix = np.zeros((44,32,3), np.uint8)# 44行32列，3通道
        # 等待接受到开头
        while True:
            text=self.serial.readline().decode("utf-8")
            print(text)
            try:
                index = int(text.split(' ')[0])
            except:
                print('split err')
            if index == 0:
                break

        # 保存第一个
        voltage = float(text.split(' ')[1].split('\n')[0])
        bgrPix[0,0,:] = self.voltageToBGR(voltage)

        # 继续接受
        while True:
            text=self.serial.readline().decode("utf-8")
            print(text)
            index = int(text.split(' ')[0])
            voltage = float(text.split(' ')[1].split('\n')[0])
            bgrPix[int(index/32),int(index%32),:] = self.voltageToBGR(voltage)
            if index == 1407:
                break

        imgSmall = Image.fromarray(bgrPix)
        imgBig = imgSmall.resize((320, 440))
        imgBig.save('../footPrints/temp.png')

    # 从txt读数据,保存成png,测试用
    def saveImgFromTxt(self):
        bgrPix = np.zeros((44,32,3), np.uint8)# 44行32列，3通道
        with open('./temp.txt','r') as f:
            # 等待接受到开头
            while True:
                text=f.readline()
                print(text)
                index = int(text.split(' ')[0])
                if index == 0:
                    break

            # 保存第一个
            voltage = float(text.split(' ')[1].split('\n')[0])
            bgrPix[0,0,:] = self.voltageToBGR(voltage)

            # 继续接受
            while True:
                text=f.readline()
                print(text)
                index = int(text.split(' ')[0])
                voltage = float(text.split(' ')[1].split('\n')[0])
                bgrPix[int(index/32),int(index%32),:] = self.voltageToBGR(voltage)
                if index == 1407:
                    break

            imgSmall = Image.fromarray(bgrPix)
            imgBig = imgSmall.resize((320, 440))
            imgBig.save('../footPrints/temp.png')
            imgBig.show()

