#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, serial, time

import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import database, convert

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
        self.portTestButton.clicked.connect(self.testPort)

    def showDatabase(self,pressed):
        self.showDatabaseButton.setChecked(False)
        form = database.DataBaseDlg()
        form.setWindowIcon(QIcon("../icons/foot32.png"))
        form.show()

    #初始化串口
    def setupPort(self):
        self.portStatus = False # 端口正在被使用标志
        self.serial = serial.Serial()#初始化serial类

        # 串口号选择
        self.portLabel = QLabel("串口选择",self)
        self.portBox = QComboBox(self)
        for i in range(8)[::-1]:
            self.portBox.addItem("COM" + str(i))

        # 波特率选择
        self.baudRateLabel = QLabel("波特率选择", self)
        self.baudRateBox = QComboBox(self)
        self.baudRateBox.addItem("9600")
        self.baudRateBox.addItem("115200")

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

    def testPort(self):
        self.portTestButton.setChecked(False)
        portName = self.portBox.currentText()  # str  "COM8"
        bandRate = int(self.baudRateBox.currentText())  # int    9600
        try:
            self.serial = serial.Serial(portName)  # 设置串口号
            self.serial.baudrate = bandRate  # 设置波特率
            self.serial.close()
            QMessageBox.warning(None, '端口', "端口可用", QMessageBox.Ok)
        except:
            QMessageBox.warning(None, '端口警告', "端口无效或者不存在", QMessageBox.Ok)

    #开始采集
    def startCollect(self, pressed):
        if pressed and self.portStatus == False:
            self.startCollectButton.setChecked(False)
            self.startCollectButton.setEnabled(False)# 禁用一下
            portName = self.portBox.currentText()  # str  "COM8"
            bandRate = int(self.baudRateBox.currentText())  # int    9600

            try:#打开串口
                self.serial = serial.Serial(portName)  # 设置串口号
                self.serial.baudrate = bandRate  # 设置波特率
            except:
                QMessageBox.warning(None, '端口警告', "端口无效或者不存在", QMessageBox.Ok)

            self.portStatus = True
            self.saveData()
        else:
            pass

    #保存脚印
    def saveData(self):
        convert.saveImg(self.serial)
        QMessageBox.warning(None, '成功', "脚印采集成功", QMessageBox.Ok)
        self.serial.close() # 最后,关掉
        self.portStatus = False
        self.startCollectButton.setEnabled(True)

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
        mainLayout.addWidget(self.scaleImageLabel)
        mainLayout.addWidget(self.footImageLabel)

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)
    #显示足底图
    def showImage(self):
        #左侧的刻度图
        self.scaleImageLabel = QLabel(self)
        self.scaleImage = QImage()
        if self.scaleImage.load("../icons/arr.png"):
            self.scaleImageLabel.setPixmap(QPixmap.fromImage(self.scaleImage))

        self.footImageLabel = QLabel(self)
        # self.footImageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.footImageLabel.setScaledContents(True)
        # self.setCentralWidget(self.footImageLabel)
        self.footImage = QImage()
        if self.footImage.load("../footPrints/timg.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
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
