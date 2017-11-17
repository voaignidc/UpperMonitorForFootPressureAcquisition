#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import convert

# 串口类
class SerialPortClass(QWidget):
    finishSavingSingal = pyqtSignal()  # 结束信号
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

    #按钮
    def showButton(self):
        self.portTestButton= QPushButton("测试串口",self)
        self.portTestButton.setCheckable(True)
        self.startCollectButton = QPushButton("开始采集", self)
        self.startCollectButton.setCheckable(True)

    #初始化串口
    def setupPort(self):
        self.portStatus = False # 端口正在被使用标志
        self.serial = serial.Serial()# 初始化serial类

        # 串口号选择
        self.portLabel = QLabel("串口选择",self)
        self.portBox = QComboBox(self)
        self.portBox.addItem("COM3")
        # for i in range(8):
        #     self.portBox.addItem("COM" + str(i))

        # 波特率选择
        self.baudRateLabel = QLabel("波特率选择", self)
        self.baudRateBox = QComboBox(self)
        self.baudRateBox.addItem("9600")
        self.baudRateBox.addItem("115200")

    # 测试串口是否打开
    def testPort(self):
        self.portTestButton.setChecked(False)
        portName = self.portBox.currentText()  # str  "COM8"
        bandRate = int(self.baudRateBox.currentText())  # int    9600
        try:
            self.serial = serial.Serial(portName)  # 设置串口号
            self.serial.baudrate = bandRate  # 设置波特率
            self.serial.close()
            QMessageBox.information(None, '端口', "端口可用", QMessageBox.Ok)
            return True
        except:
            QMessageBox.warning(None, '端口警告', "端口无效或者不存在", QMessageBox.Ok)
            return False

    # 开始采集
    def startCollect(self, pressed):
        if pressed and self.portStatus == False:
            self.startCollectButton.setChecked(False)
            portName = self.portBox.currentText()  # str  "COM8"
            bandRate = int(self.baudRateBox.currentText())  # int    9600

            try: # 打开串口
                self.serial = serial.Serial(portName)  # 设置串口号
                self.serial.baudrate = bandRate  # 设置波特率
            except:
                self.serial.close()  # 关掉串口
                QMessageBox.warning(None, '端口警告', "端口无效或者不存在", QMessageBox.Ok)
                return False

            self.startCollectButton.setEnabled(False) # 禁用一下
            self.portStatus = True
            self.savingData()
            return True

    # 保存脚印
    def savingData(self):
        # 以下必须加self,不然会卡死,为什么?
        self.convertProcessDlg = convert.ConvertProcessDlg(self.serial)
        # '转换结束'信号连接到 finishSavingData
        self.convertProcessDlg.convertProcessThread.finishConvertSingal.connect(self.finishSavingData)
        self.convertProcessDlg.convertProcessThread.start()

    # 结束保存脚印数据
    def finishSavingData(self):
        self.serial.close()  # 最后,关掉串口
        QMessageBox.information(None, '成功', "脚印采集成功", QMessageBox.Ok)
        self.convertProcessDlg.close() # 关闭这个对话框
        self.portStatus = False
        self.startCollectButton.setEnabled(True)
        self.finishSavingSingal.emit() # 发射'保存完毕'信号

    # 布局
    def setupLayout(self, fatherLayout):
        fatherLayout.addWidget(self.portLabel)
        fatherLayout.addWidget(self.portBox)
        fatherLayout.addWidget(self.baudRateLabel)
        fatherLayout.addWidget(self.baudRateBox)
        fatherLayout.addWidget(self.portTestButton)
        fatherLayout.addWidget(self.startCollectButton)