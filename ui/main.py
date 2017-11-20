#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import adminDataBase, serialPort, userInput

# 主窗口
class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setupDataBase()
        self.setupUserInputDlg()
        # self.showLabel()
        self.showButton()
        self.showImage()
        self.serialPortObject = serialPort.SerialPortClass()
        self.setupLayout()
        self.connectSignalSlot()

    #连接信号与槽
    def connectSignalSlot(self):
        self.showUserInputDlgButton.clicked.connect(self.showUserInputDlg)
        self.showAdminDataBaseDlgButton.clicked.connect(self.showAdminDataBaseDlg)
        self.serialPortObject.finishSavingPNGSingal.connect(self.refreshFootImageAfterSavingPNG) # '保存完毕'信号 连 刷新图像
        # self.refreshFootImageButton.clicked.connect(self.refreshFootImageAfterChangeUserBox)
        self.clearFootImageButton.clicked.connect(self.clearFootImage)
        self.saveFootImageButton.clicked.connect(self.saveFootImageToDataBase)

        # activated是用户点击QComboBox后才产生的信号,程序改变QComboBox则不产生此信号
        self.selectUserBox.activated[int].connect(self.refreshFootImageAfterChangeUserBox)

    # 初始化数据库
    def setupDataBase(self):
        self.adminDataBaseDlg = adminDataBase.AdminDataBaseDlg()
        self.selectUserLabel = QLabel("选择用户",self)
        self.selectUserBox = QComboBox()

        self.query = QSqlQuery()
        self.query.exec_("""select id,userName from footdata""")
        while self.query.next():
            id = self.query.value(0)
            name = self.query.value(1)
            self.selectUserBox.addItem(name+' id='+str(id))
        # 连接
        self.adminDataBaseDlg.dataBaseRecordChangeSignal.connect(self.refreshUserNameBox)

    # 显示数据库
    def showAdminDataBaseDlg(self):
        self.showAdminDataBaseDlgButton.setChecked(False)
        self.adminDataBaseDlg.show()

    # 刷新用户Box
    def refreshUserNameBox(self):
        self.selectUserBox.clear() # 清空这个QComboBox
        self.query = QSqlQuery()
        self.query.exec_("""select id,userName from footdata""")
        while self.query.next():
            id = self.query.value(0)
            name = self.query.value(1)
            print(id,name)
            self.selectUserBox.addItem(name+' id='+str(id))

    # 获得当前是哪个用户
    def getCurrentUserName(self):
        currentUserName = self.selectUserBox.currentText()
        return currentUserName

    # 获得当前是哪个ID
    def getCurrentUserId(self):
        currentUserName = self.selectUserBox.currentText()
        currentUserId = currentUserName.split('=')[1]
        return currentUserId

    #显示按钮
    def showButton(self):
        self.showUserInputDlgButton = QPushButton("信息录入", self)
        self.showUserInputDlgButton.setCheckable(True)
        self.showAdminDataBaseDlgButton = QPushButton("用户管理", self) # 数据库按钮在这里
        self.showAdminDataBaseDlgButton.setCheckable(True)
        # self.refreshFootImageButton = QPushButton("刷新压力图", self)
        # self.refreshFootImageButton.setCheckable(True)
        self.clearFootImageButton = QPushButton("清除压力图", self)
        self.clearFootImageButton.setCheckable(True)
        self.saveFootImageButton = QPushButton("保存压力图", self)
        self.saveFootImageButton.setCheckable(True)

    def setupUserInputDlg(self):
        self.userInputDlg = userInput.UserInputDlg()

    def showUserInputDlg(self):
        self.showUserInputDlgButton.setChecked(False)
        self.userInputDlg.show()

    # 标签
    def showLabel(self):
        # self.selectPoiseLabel = QLabel("选择站姿", self)
        # self.selectPoiseBox = QComboBox(self)
        # self.selectPoiseBox.addItem("双脚")
        # self.selectPoiseBox.addItem("左脚")
        # self.selectPoiseBox.addItem("右脚")
        pass

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
            self.resize(self.footImage.width(),self.footImage.height())
        self.refreshFootImageAfterChangeUserBox(0)

    # 刷新脚印压力图 从串口保存成png之后
    def refreshFootImageAfterSavingPNG(self):
        if self.footImage.load("../footPrints/tempBig.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))

    # 刷新脚印压力图 (人为鼠标点击改变,而不是程序改变)改变用户Box之后
    def refreshFootImageAfterChangeUserBox(self, uselessVar):
        # self.refreshFootImageButton.setChecked(False)
        currentUserName = self.getCurrentUserName()  # 获得用户名+id
        if (currentUserName == ''):
            print('没有用户')
            # QMessageBox.warning(self, "警告", "没有用户!", QMessageBox.Ok)
            return False
        currentUserId = self.getCurrentUserId()  # 获得用户id

        self.query.prepare(""" select footImg from footdata where id=(?) """)
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()
        while self.query.next():
            byteDataReaded = self.query.value(0)
            try: # 此用户数据库中有压力图
                imgSmall = Image.frombytes('RGB', (32, 44), byteDataReaded)
                imgSmall.save('../footPrints/tempSmall.png')
                imgBig = imgSmall.resize((320, 440))
                imgBig.save('../footPrints/tempBig.png')
                if self.footImage.load("../footPrints/tempBig.png"):
                    self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
                    return True
            except: # 此用户数据库中没有压力图(还未采集)
                if self.footImage.load("../footPrints/blank.png"):
                    self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
                return False

    # 清空脚印压力图
    def clearFootImage(self):
        self.clearFootImageButton.setChecked(False)
        try:
            os.remove("../footPrints/tempBig.png")
            os.remove("../footPrints/tempSmall.png")
        except:
            pass
        if self.footImage.load("../footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))

    # 保存脚印压力图到数据库
    def saveFootImageToDataBase(self):
        self.saveFootImageButton.setChecked(False)
        try:
            imgRead = Image.open("../footPrints/tempSmall.png")
            # self.imgSize = imgRead.size  # (320,440)
            # self.imgMode = imgRead.mode  # RGB ,str
            byteDataToWrite = imgRead.tobytes()

            currentUserName = self.getCurrentUserName() # 获得用户名+id
            if(currentUserName==''):
                QMessageBox.warning(self, "警告", "没有用户!无法保存压力图数据!\n请先在数据库里建立用户!", QMessageBox.Ok)
                return False

            currentUserId = self.getCurrentUserId() #获得用户id
            self.query.prepare(""" update footdata set footImg=NULL where id=(?) """) # 清空
            self.query.addBindValue(QVariant(currentUserId))
            self.query.exec_()

            self.query.prepare(""" update footdata set footImg=(?) where id=(?) """) # 写入
            self.query.addBindValue(QByteArray(byteDataToWrite))
            self.query.addBindValue(QVariant(currentUserId))
            self.query.exec_()

            QMessageBox.information(self, "成功", "成功保存压力图数据", QMessageBox.Ok)
            return True
        except:
            QMessageBox.warning(self, "警告", "没有可以用来保存的压力图数据!", QMessageBox.Ok)
            return False

    #布局
    def setupLayout(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(0)

        leftSideLayout.addWidget(self.showUserInputDlgButton)
        leftSideLayout.addWidget(self.showAdminDataBaseDlgButton)
        leftSideLayout.addWidget(self.selectUserLabel)
        leftSideLayout.addWidget(self.selectUserBox)
        # leftSideLayout.addWidget(self.selectPoiseLabel)
        # leftSideLayout.addWidget(self.selectPoiseBox)

        self.serialPortObject.setupLayout(leftSideLayout)

        # leftSideLayout.addWidget(self.refreshFootImageButton)
        leftSideLayout.addWidget(self.clearFootImageButton)
        leftSideLayout.addWidget(self.saveFootImageButton)

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
