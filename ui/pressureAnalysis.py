#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
np.set_printoptions(threshold=np.nan)
import matplotlib.pyplot as plt

class PressureData():
    """计算压力,压强等"""
    def __init__(self):
        self.voltageArr = np.array(self.readVoltageArrFromTxt())
        self.forceArr = self.voltageArrToForceArr(self.voltageArr)
        self.pressureArr = self.forceArrToPressureArr(self.forceArr)

        self.totalForce = self.forceArr.sum() # 总压力
        self.averageForce = int(self.totalForce/(44*32)) # 平均压力
        self.totalPressure = self.pressureArr.sum() # 总压强
        self.averagePressure = int(self.totalPressure/(44*32)) # 平均压强
        self.maxPressure = np.max(self.pressureArr) # 最大压强
        self.minPressure = np.min(self.pressureArr[self.pressureArr != 0]) # 最小有效压强
        self.touchedArea = self.getTouchedArea(self.voltageArr) # 接触面积

    def readVoltageArrFromTxt(self):
        """
        从txt读取电压数据
        Return:
            voltageArrRead: 电压, 0-3.300V
        """
        voltageArrRead = []
        with open("../footPrints/voltageArr.txt", 'r+') as f:
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
    def __init__(self, pressureArr):
        super().__init__()
        X = [0, 1, 2, 3, 4, 5]
        Y = [222, 42, 455, 664, 454, 334]
        fig = plt.figure()
        plt.bar(X, Y, 0.4, color="blue")
        plt.xlabel("pressure(kPa)")
        plt.ylabel("times")
        plt.title("pressure-times hist")
        plt.show()

class PressureAnalysisDlg(QDialog):
    """压力分析的对话框"""
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setupLayout()
        self.showUi()
        pressureData = PressureData()
        pressureDiagram = PressureDiagram(pressureData.pressureArr)



    def setupUi(self):
        self.totalForceLabel = QLabel("总压力(N)", self)
        self.totalForceLineEdit = QLineEdit(self)
        self.totalForceLineEdit.setEnabled(False)
        self.averageForceLabel = QLabel("平均压力(N)", self)
        self.averageForceLineEdit = QLineEdit(self)
        self.totalPressureLabel = QLabel("总压强(kPa)", self)
        self.totalPressureLineEdit = QLineEdit(self)
        self.averagePressureLabel = QLabel("平均压强(kPa)", self)
        self.averagePressureLineEdit = QLineEdit(self)
        self.maxPressureLabel = QLabel("最大压强(kPa)", self)
        self.maxPressureLineEdit = QLineEdit(self)
        self.minPressureLabel = QLabel("最小压强(kPa)", self)
        self.minPressureLineEdit = QLineEdit(self)
        self.touchedAreaLabel = QLabel("接触面积(cm^2)", self)
        self.touchedAreaLineEdit = QLineEdit(self)

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

        self.setLayout(self.gridLayout)

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint) # 关闭问号
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("压力分析")
        self.show()




app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(True)

window = PressureAnalysisDlg()
window.show()

sys.exit(app.exec_())