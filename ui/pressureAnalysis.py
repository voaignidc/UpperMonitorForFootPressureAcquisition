#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt

class PressureData():
    """计算压力,压强等"""
    def __init__(self):
        self.voltageArr = np.array(self.readVoltageArrFromTxt()) # 电压列表
        self.forceArr = self.voltageArrToForceArr(self.voltageArr) # 压力列表
        self.pressureArr = self.forceArrToPressureArr(self.forceArr) # 压强列表

        self.totalForce = self.forceArr.sum() # 总压力
        self.averageForce = int(self.totalForce/(44*32)) # 平均压力
        self.totalPressure = self.pressureArr.sum() # 总压强
        self.averagePressure = int(self.totalPressure/(44*32)) # 平均压强
        self.maxPressure = np.max(self.pressureArr) # 最大压强
        self.minPressure = np.min(self.pressureArr[self.pressureArr != 0]) # 最小有效压强
        self.touchedArea = self.getTouchedArea(self.voltageArr) # 接触面积
        self.pressureDistribution=[]
        for i in range(10):
            bigger = self.pressureArr[self.pressureArr >= i*1000]
            among = bigger[bigger < (i+1)*1000]
            self.pressureDistribution.append(len(among))
        self.pressureDistribution = np.array(self.pressureDistribution) # 压强分布

    def readVoltageArrFromTxt(self):
        """
        从txt读取电压数据
        Return:
            voltageArrRead: 电压, 0-3.300V
        """
        voltageArrRead = []
        with open("./footPrints/voltageArr.txt", 'r+') as f:
            data = f.readline()
            if data != '':
                for numStr in data.split(', '):
                    voltageArrRead.append(float(numStr))
        return voltageArrRead

    def voltageArrToForceArr(self, voltageArr):
        """
        0-3.300V 转 压力
        公式是m=(a0*v^4+a1*v^3+...+a4), F=m*9.8
        Args:
            voltageArr: 电压, 0-3.300V
        Return:
            forceArr: 压力, 单位牛顿
        """
        a = np.array([208.4305, -677.7504, 811.4967, -439.8050, 99.3741]) # 拟合参数
        voltageArr[np.where(voltageArr <= 0.115)] = 0.115
        voltageArr[np.where(voltageArr >= 1.15)] = 1.15 # 限幅

        forceArr=np.zeros_like(voltageArr)
        for i in range(len(a)):
            forceArr = forceArr + a[i] * np.power(voltageArr, 4-i) # 进行拟合

        forceArr = (forceArr * 9.8).astype(int)
        forceArr[np.where(forceArr <= 6)] = 0
        return forceArr

    def forceArrToPressureArr(self, forceArr):
        """
        压力 转 压强
        公式是P=F/s
        Args:
            forceArr: 压力, 单位牛顿
        Return:
            pressureArr: 压强, 单位千帕
        """
        s = 36.4*30.5/(44*32*10000) # 每个像素对应传感器的面积, 单位m^2
        pressureArr = (forceArr/(s * 1000)).astype(int)
        return pressureArr

    def getTouchedArea(self, voltageArr):
        """
        接触面积
        Args:
            voltageArr: 电压, 0-3.300V
        Return:
            touchedArea: 接触面积, 单位cm^2
        """
        untouchedPixNum = len(voltageArr[voltageArr <= 0.115])
        untouchedPixNum = untouchedPixNum + len(voltageArr[voltageArr >= 1.15])
        touchedPixNum = 1408 - untouchedPixNum
        s = 36.4 * 30.5 / (44 * 32)
        touchedArea = int(touchedPixNum*s)
        return touchedArea

class PressureDiagram():
    """压强分析图"""
    def __init__(self, pressureDistribution):
        super().__init__()
        self.pressureDistribution = pressureDistribution
        self.fig = plt.figure(1)
        self.fig.set_size_inches(8, 4) # 设置图片大小
        self.barAx = self.fig.add_subplot(121)
        self.pieAx = self.fig.add_subplot(122)
        self.drawPressureTimesBar()
        self.drawPressureTimesPie()

    def savePressureDiagram(self):
        """保存压强分布图"""
        plt.savefig("./footPrints/pressureDiagram.png")
        plt.close('all')

    def drawPressureTimesBar(self):
        """压强分布柱形图"""
        width = 0.5
        xticks = np.linspace(0.5, 9.5, 10)
        xticklabels = []
        for i in range(10):
            xticklabels.append(str(i+1)+'k') # 获得标签

        self.barAx.bar(xticks-width/2, self.pressureDistribution, width, color="blue")
        self.barAx.set_xticks(xticks)
        self.barAx.set_xticklabels(xticklabels)
        self.barAx.set_xlabel("pressure(kPa)")
        self.barAx.set_ylabel("times")
        self.barAx.set_title("pressure-times bar")

    def drawPressureTimesPie(self):
        """压强分布扇形图"""
        zeroIndex = np.where(self.pressureDistribution == 0)
        labels = []
        for i in np.arange(10): # 获得压强值非0的标签
            if False in np.isnan(np.where(zeroIndex == i)):
                pass
            else:
                labels.append(str(i)+'k-'+str(i+1)+'k')
        self.pieAx.pie(self.pressureDistribution[self.pressureDistribution > 0], labels = labels, autopct='%1.1f%%')
        self.pieAx.set_title("pressure% pie")

class PressureAnalysisDlg(QDialog):
    """压强分析的对话框"""
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setupPressureDiagram()
        self.setupLayout()
        self.showUi()

    def refreshAll(self):
        """刷新全部 (LineEdit和压强分析图)"""
        if os.path.exists("./footPrints/voltageArr.txt"):
            pressureData = PressureData()
            self.refreshLineEdit(pressureData)
            pressureDiagram = PressureDiagram(pressureData.pressureDistribution)
            pressureDiagram.savePressureDiagram()
            self.refreshPressureDiagram()

    def setupPressureDiagram(self):
        """初始化压强分析图"""
        self.pressureImage = QImage()
        self.pressureImageLabel = QLabel(self)

    def refreshPressureDiagram(self):
        """刷新压强分析图"""
        if self.pressureImage.load("./footPrints/pressureDiagram.png"):
            self.pressureImageLabel.setPixmap(QPixmap.fromImage(self.pressureImage))

    def refreshLineEdit(self, pressureData):
        self.totalForceLineEdit.setText(str(pressureData.totalForce))
        self.averageForceLineEdit.setText(str(pressureData.averageForce))
        self.totalPressureLineEdit.setText(str(pressureData.totalPressure))
        self.averagePressureLineEdit.setText(str(pressureData.averagePressure))
        self.maxPressureLineEdit.setText(str(pressureData.maxPressure))
        self.minPressureLineEdit.setText(str(pressureData.minPressure))
        self.touchedAreaLineEdit.setText(str(pressureData.touchedArea))

    def setupUi(self):
        self.totalForceLabel = QLabel("总压力(N)", self)
        self.totalForceLineEdit = QLineEdit(self)
        self.totalForceLineEdit.setFixedWidth(100)
        self.averageForceLabel = QLabel("平均压力(N)", self)
        self.averageForceLineEdit = QLineEdit(self)
        self.averageForceLineEdit.setFixedWidth(100)
        self.totalPressureLabel = QLabel("总压强(kPa)", self)
        self.totalPressureLineEdit = QLineEdit(self)
        self.totalPressureLineEdit.setFixedWidth(100)
        self.averagePressureLabel = QLabel("平均压强(kPa)", self)
        self.averagePressureLineEdit = QLineEdit(self)
        self.averagePressureLineEdit.setFixedWidth(100)
        self.maxPressureLabel = QLabel("最大压强(kPa)", self)
        self.maxPressureLineEdit = QLineEdit(self)
        self.maxPressureLineEdit.setFixedWidth(100)
        self.minPressureLabel = QLabel("最小压强(kPa)", self)
        self.minPressureLineEdit = QLineEdit(self)
        self.minPressureLineEdit.setFixedWidth(100)
        self.touchedAreaLabel = QLabel("接触面积(cm^2)", self)
        self.touchedAreaLineEdit = QLineEdit(self)
        self.touchedAreaLineEdit.setFixedWidth(100)

    def setupLayout(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)

        self.gridLayout.addWidget(self.totalForceLabel, *(0,0))
        self.gridLayout.addWidget(self.totalForceLineEdit, *(0,1))
        self.gridLayout.addWidget(self.averageForceLabel, *(1,0))
        self.gridLayout.addWidget(self.averageForceLineEdit, *(1,1))
        self.gridLayout.addWidget(self.totalPressureLabel, *(2,0))
        self.gridLayout.addWidget(self.totalPressureLineEdit, *(2,1))
        self.gridLayout.addWidget(self.averagePressureLabel, *(3,0))
        self.gridLayout.addWidget(self.averagePressureLineEdit, *(3,1))
        self.gridLayout.addWidget(self.maxPressureLabel, *(4,0))
        self.gridLayout.addWidget(self.maxPressureLineEdit, *(4,1))
        self.gridLayout.addWidget(self.minPressureLabel, *(5,0))
        self.gridLayout.addWidget(self.minPressureLineEdit, *(5,1))
        self.gridLayout.addWidget(self.touchedAreaLabel, *(6,0))
        self.gridLayout.addWidget(self.touchedAreaLineEdit, *(6,1))

        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(self.gridLayout)
        mainLayout.addWidget(self.pressureImageLabel)
        self.setLayout(mainLayout)

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint) # 关闭问号
        self.setWindowIcon(QIcon("./icons/foot32.png"))
        self.setWindowTitle("压力分析")

# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(True)
#
# window = PressureAnalysisDlg()
# window.show()
#
# sys.exit(app.exec_())