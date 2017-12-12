#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import matplotlib

class PressureData():
    def __init__(self):
        voltageArrRead = self.readVoltageArrFromTxt()
        self.voltageArr = np.array(voltageArrRead)
        print(self.voltageArr)
        self.forceArr = self.voltageArrToForceArr(self.voltageArr)
        print(self.forceArr)
        self.pressureArr = self.forceArrToPressureArr(self.forceArr)
        print(self.pressureArr)

    def readVoltageArrFromTxt(self):
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
        公式是y=ax+b
        Args:
            voltageArr: 电压, 0-3.300V
        Return:
            forceArr: 压力, 单位牛顿
        """
        a = -10000/3.3
        b = 10000
        forceArr = a * voltageArr + b
        return forceArr.astype(int)

    def forceArrToPressureArr(self, forceArr):
        """
        压力 转 压强
        公式是y=x/s
        Args:
            forceArr: 压力, 单位牛顿
        Return:
            pressureArr: 压强, 单位千帕
        """
        s = 0.0025
        pressureArr = forceArr/(s * 1000)
        return pressureArr


class PressureAnalysisDlg(QDialog):
    """压力分析的对话框"""
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setupLayout()
        self.showUi()
        self.read()

    def setupUi(self):
        self.analysisLabel = QLabel("压力分析", self)

    def setupLayout(self):
        pass

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint) # 关闭问号
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("压力分析")
        self.show()

    def read(self):
        p=PressureData()


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(True)

window = PressureAnalysisDlg()
window.show()

sys.exit(app.exec_())