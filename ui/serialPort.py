#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial

from PyQt5.QtWidgets import *

import convert
class SerialPortClass(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.showButton()
        self.setupPort()
        self.connectSignalSlot()

    #连接信号与槽
    def connectSignalSlot(self):
        self.startCollectButton.clicked[bool].connect(self.startCollect)
        self.portTestButton.clicked.connect(self.testPort)

    #初始化串口
    def setupPort(self):
        self.portStatus = False # 端口正在被使用标志
        self.serial = serial.Serial()# 初始化serial类

        # 串口号选择
        self.portLabel = QLabel("串口选择",self)
        self.portBox = QComboBox(self)
        for i in range(8):
            self.portBox.addItem("COM" + str(i))

        # 波特率选择
        self.baudRateLabel = QLabel("波特率选择", self)
        self.baudRateBox = QComboBox(self)
        self.baudRateBox.addItem("9600")
        self.baudRateBox.addItem("115200")

    def showButton(self):
        # 测试串口按钮
        self.portTestButton= QPushButton("测试串口",self)
        self.portTestButton.setCheckable(True)

        self.startCollectButton = QPushButton("开始采集", self)
        self.startCollectButton.setCheckable(True)
        self.stopCollectButton = QPushButton("停止采集", self)
        self.stopCollectButton.setCheckable(True)
        self.clearDataButton = QPushButton("清除", self)
        self.clearDataButton.setCheckable(True)
        self.saveDataButton = QPushButton("保存", self)
        self.saveDataButton.setCheckable(True)

    #测试串口是否打开
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

    # 保存脚印
    def saveData(self):
        convert.saveImgFromSerial(self.serial)
        QMessageBox.warning(None, '成功', "脚印采集成功", QMessageBox.Ok)
        self.serial.close() # 最后,关掉
        self.portStatus = False
        self.startCollectButton.setEnabled(True)

    def setupLayout(self, fatherLayout):
        fatherLayout.addWidget(self.portLabel)
        fatherLayout.addWidget(self.portBox)
        fatherLayout.addWidget(self.baudRateLabel)
        fatherLayout.addWidget(self.baudRateBox)
        fatherLayout.addWidget(self.portTestButton)

        fatherLayout.addWidget(self.startCollectButton)
        fatherLayout.addWidget(self.stopCollectButton)
        fatherLayout.addWidget(self.clearDataButton)
        fatherLayout.addWidget(self.saveDataButton)