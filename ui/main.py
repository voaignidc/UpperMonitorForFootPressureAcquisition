#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, serial, time

import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import database

class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.showLabel()
        self.showButton()
        self.showImage()
        self.setupPort()
        self.addLayout()
        self.connectSignalSlot()

    #连接信号与槽
    def connectSignalSlot(self):
        self.startCollectButton.clicked[bool].connect(self.startCollect)
        self.showDatabaseButton.clicked.connect(self.showDatabase)

    def showDatabase(self,pressed):
        self.showDatabaseButton.setChecked(False)
        form = database.DataBaseDlg()
        form.setWindowIcon(QIcon("../icons/foot32.png"))
        form.show()

    #初始化串口
    def setupPort(self):
        self.portStatus = False#端口使能标志
        self._serial = serial.Serial()#初始化serial类

        # 串口号选择
        self.portLabel = QLabel("串口选择",self)
        self.portBox = QComboBox(self)
        for i in range(8)[::-1]:
            self.portBox.addItem("COM" + str(i))

        # 波特率选择
        self.baudRateLabel = QLabel("波特率选择", self)
        self.baudRateBox = QComboBox(self)
        self.baudRateBox.addItem("115200")
        self.baudRateBox.addItem("9600")

        # 测试串口按钮
        self.portTestButton= QPushButton("测试串口",self)
        self.portTestButton.setCheckable(True)

    def showButton(self):
        self.showDatabaseButton = QPushButton("数据库", self) # 数据库按钮在这里
        self.showDatabaseButton.setCheckable(True)

        self.startCollectButton = QPushButton("开始采集", self)
        self.startCollectButton.setCheckable(True)
        self.stopCollectButton = QPushButton("停止采集", self)
        self.stopCollectButton.setCheckable(True)
        self.clearDataButton = QPushButton("清除", self)
        self.clearDataButton.setCheckable(True)
        self.saveDataButton = QPushButton("保存", self)
        self.saveDataButton.setCheckable(True)

    def startCollect(self, pressed):
        if pressed:
            self.startCollectButton.setEnabled(False)
            self.sendStartFlag()
            self.readData()
        else:
            pass

    def sendStartFlag(self):
        pass

    def readData(self):
        pass

    def sendStopFlag(self):
        pass

    def showLabel(self):
        self.selectUserLabel = QLabel("选择用户",self)
        self.selectUserBox = QComboBox(self)
        for i in range(8):
            self.selectUserBox.addItem("用户"+str(i))

        self.selectPoiseLabel = QLabel("选择站姿", self)
        self.selectPoiseBox = QComboBox(self)
        self.selectPoiseBox.addItem("双脚")
        self.selectPoiseBox.addItem("左脚")
        self.selectPoiseBox.addItem("右脚")

    #布局
    def addLayout(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(0)

        leftSideLayout.addWidget(self.showDatabaseButton)
        leftSideLayout.addWidget(self.selectUserLabel)
        leftSideLayout.addWidget(self.selectUserBox)
        leftSideLayout.addWidget(self.selectPoiseLabel)
        leftSideLayout.addWidget(self.selectPoiseBox)

        leftSideLayout.addWidget(self.portLabel)
        leftSideLayout.addWidget(self.portBox)
        leftSideLayout.addWidget(self.baudRateLabel)
        leftSideLayout.addWidget(self.baudRateBox)
        leftSideLayout.addWidget(self.portTestButton)

        leftSideLayout.addWidget(self.startCollectButton)
        leftSideLayout.addWidget(self.stopCollectButton)
        leftSideLayout.addWidget(self.clearDataButton)
        leftSideLayout.addWidget(self.saveDataButton)

        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.imageLabel)

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)
    #显示足底图
    def showImage(self):
        self.imageLabel = QLabel(self)
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.imageLabel.setScaledContents(True)
        self.setCentralWidget(self.imageLabel)

        self.footImage = QImage()
        if self.footImage.load("../footPrints/timg.png"):
                self.imageLabel.setPixmap(QPixmap.fromImage(self.footImage))
                # self.resize(self.footImage.width(),self.footImage.height())

'''以下主函数'''
app = QApplication(sys.argv)
app.setApplicationName("脚印采集系统")
app.setQuitOnLastWindowClosed(True)

window = MainWindow()
window.show()
# window.resize(1200, 800)
window.setWindowIcon(QIcon("../icons/foot32.png"))

sys.exit(app.exec_())
