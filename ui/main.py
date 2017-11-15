#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, serial

import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import database, serialPort

class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.showLabel()
        self.showButton()
        self.showImage()
        self.serialPortObject = serialPort.SerialPortClass()
        self.setupLayout()
        self.connectSignalSlot()

    #连接信号与槽
    def connectSignalSlot(self):
        self.showDatabaseButton.clicked.connect(self.showDatabase)
        self.refreshFootImageButton.clicked.connect(self.refreshFootImage)
        self.clearFootImageButton.clicked.connect(self.clearFootImage)

    #显示数据库
    def showDatabase(self,pressed):
        self.showDatabaseButton.setChecked(False)
        form = database.DataBaseDlg()
        form.setWindowIcon(QIcon("../icons/foot32.png"))
        form.show()

    #显示按钮
    def showButton(self):
        self.showDatabaseButton = QPushButton("数据库", self) # 数据库按钮在这里
        self.showDatabaseButton.setCheckable(True)

        self.refreshFootImageButton = QPushButton("刷新云图", self)
        self.refreshFootImageButton.setCheckable(True)
        self.clearFootImageButton = QPushButton("清除", self)
        self.clearFootImageButton.setCheckable(True)
        self.saveFootDataButton = QPushButton("保存", self)
        self.saveFootDataButton.setCheckable(True)

    # 标签
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

    #显示两个图
    def showImage(self):
        #左侧的刻度图
        self.scaleImageLabel = QLabel(self)
        self.scaleImage = QImage()
        if self.scaleImage.load("../icons/arr.png"):
            self.scaleImageLabel.setPixmap(QPixmap.fromImage(self.scaleImage))

        #足底压力图
        self.footImageLabel = QLabel(self)
        # self.footImageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.footImageLabel.setScaledContents(True)
        # self.setCentralWidget(self.footImageLabel)
        self.footImage = QImage()
        if self.footImage.load("../footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            # self.resize(self.footImage.width(),self.footImage.height())

    # 刷新脚印压力图
    def refreshFootImage(self):
        self.refreshFootImageButton.setChecked(False)
        if self.footImage.load("../footPrints/temp.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))

    # 清空脚印压力图
    def clearFootImage(self):
        self.clearFootImageButton.setChecked(False)
        if self.footImage.load("../footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))

    #布局
    def setupLayout(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(0)

        leftSideLayout.addWidget(self.showDatabaseButton)
        leftSideLayout.addWidget(self.selectUserLabel)
        leftSideLayout.addWidget(self.selectUserBox)
        leftSideLayout.addWidget(self.selectPoiseLabel)
        leftSideLayout.addWidget(self.selectPoiseBox)

        self.serialPortObject.setupLayout(leftSideLayout)

        leftSideLayout.addWidget(self.refreshFootImageButton)
        leftSideLayout.addWidget(self.clearFootImageButton)
        leftSideLayout.addWidget(self.saveFootDataButton)

        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.scaleImageLabel)
        mainLayout.addWidget(self.footImageLabel)

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)



'''以下主函数'''
app = QApplication(sys.argv)
app.setApplicationName("脚印采集系统")
app.setQuitOnLastWindowClosed(True)

window = MainWindow()
window.show()
# window.resize(1200, 800)
window.setWindowIcon(QIcon("../icons/foot32.png"))

sys.exit(app.exec_())
