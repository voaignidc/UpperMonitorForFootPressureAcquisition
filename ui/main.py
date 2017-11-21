#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import adminDataBase, serialPort, userInput, currentTime, signIn

# 主窗口
class MainWindow(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self._adminPermission = False # 管理员权限标志
        self.newAccount = False # 是新账户标志
        self.setupDataBase()
        self.setupSignInDlg()

    # 初始化登录界面
    def setupSignInDlg(self):
        self.signInDlg = signIn.SignInDlg()
        self.signInDlg.signInSignal.connect(self.setupMainWindow) # 只有登录了,才能显示主窗口
        self.signInDlg.adminPermissionSignal.connect(self.getAdminPermission)
        self.signInDlg.newUserSignUpSignal.connect(self.signUpAsNewUser)

    # 新用户注册
    def signUpAsNewUser(self):
        self.newAccount = True

    # 获得管理员权限
    def getAdminPermission(self):
        self._adminPermission = True
        print('getAdminPermission')

    # 初始化主窗口
    def setupMainWindow(self):
        self.signInDlg.close()
        self.setupUserInputDlg()
        self.serialPortObject = serialPort.SerialPortClass()
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()
        if self.newAccount:
            self.userInputDlg.show()
            self.userInputDlg.collectTimeLineEdit.setText(currentTime.getCurrentTime())

    # 初始化主窗口Ui
    def setupUi(self):
        self.showButton()
        self.showImage()

    # 显示主窗口
    def showUi(self):
        self.show()
        self.setWindowIcon(QIcon("../icons/foot32.png"))

    # 连接信号与槽
    def connectSignalSlot(self):
        self.showUserInputDlgButton.clicked.connect(self.showUserInputDlg)  # 连 显示用户录入对话框
        self.showAdminDataBaseDlgButton.clicked.connect(self.showAdminDataBaseDlg)
        self.serialPortObject.finishSavingPNGSingal.connect(self.refreshFootImageAfterSavingPNG)  # '保存完毕'信号 连 刷新图像
        self.clearFootImageButton.clicked.connect(self.clearFootImage)
        self.saveFootImageButton.clicked.connect(self.saveFootImageToDataBase)
        # activated是用户点击QComboBox后才产生的信号,程序改变QComboBox则不产生此信号
        self.selectUserBox.activated[int].connect(self.refreshFootImageAfterChangeUserBox)

    # 初始化数据库
    def setupDataBase(self):
        self.adminDataBaseDlg = adminDataBase.AdminDataBaseDlg()
        self.selectUserLabel = QLabel("选择用户", self)
        self.selectUserBox = QComboBox()

        self.query.exec_("""SELECT id,userName FROM footdata""")
        while self.query.next():
            id = self.query.value(0)
            name = self.query.value(1)
            self.selectUserBox.addItem(name + ' id=' + str(id))
        # 连接
        self.adminDataBaseDlg.dataBaseRecordChangeSignal.connect(self.refreshUserNameBox)

    # 显示数据库
    def showAdminDataBaseDlg(self):
        self.showAdminDataBaseDlgButton.setChecked(False)
        self.adminDataBaseDlg.show()

    # 刷新用户Box
    def refreshUserNameBox(self):
        self.selectUserBox.clear()  # 清空这个QComboBox
        self.query.exec_("""SELECT id,userName FROM footdata""")
        while self.query.next():
            id = self.query.value(0)
            name = self.query.value(1)
            print(id, name)
            self.selectUserBox.addItem(name + ' id=' + str(id))

    # 获得当前是哪个用户
    def getCurrentUserName(self):
        currentUserName = self.selectUserBox.currentText()
        return currentUserName

    # 获得当前是哪个ID
    def getCurrentUserId(self):
        currentUserName = self.selectUserBox.currentText()
        currentUserId = currentUserName.split('=')[1]
        return currentUserId

    # 显示按钮
    def showButton(self):
        self.showUserInputDlgButton = QPushButton("信息录入", self)
        self.showUserInputDlgButton.setCheckable(True)
        self.showAdminDataBaseDlgButton = QPushButton("用户管理", self)  # 数据库按钮在这里
        self.showAdminDataBaseDlgButton.setCheckable(True)
        self.clearFootImageButton = QPushButton("清除压力图", self)
        self.clearFootImageButton.setCheckable(True)
        self.saveFootImageButton = QPushButton("保存压力图", self)
        self.saveFootImageButton.setCheckable(True)

    # 初始化 用户录入 对话框
    def setupUserInputDlg(self):
        self.userInputDlg = userInput.UserInputDlg()
        self.userInputDlg.dataBaseRecordChangeSignal.connect(self.refreshDataBase)

    # 用户录入 对话框 点完保存后, 再重新载入数据库
    def refreshDataBase(self):
        # self.adminDataBaseDlg.model.setTable("footdata")  # 数据库名称
        # self.adminDataBaseDlg.model.select()
        # self.adminDataBaseDlg.view.setModel(self.adminDataBaseDlg.model)
        self.adminDataBaseDlg.setupSqlTableModel()
        self.adminDataBaseDlg.setupTableView()
        self.refreshUserNameBox()

    # 显示 用户录入 对话框
    def showUserInputDlg(self):
        self.showUserInputDlgButton.setChecked(False)
        self.userInputDlg.show()
        self.userInputDlg.collectTimeLineEdit.setText(currentTime.getCurrentTime())

    # 显示两个图
    def showImage(self):
        # 左侧的刻度图
        self.scaleImageLabel = QLabel(self)
        self.scaleImage = QImage()
        if self.scaleImage.load("../icons/arr.png"):
            self.scaleImageLabel.setPixmap(QPixmap.fromImage(self.scaleImage))

        # 足底压力图
        self.footImageLabel = QLabel(self)
        # self.footImageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.footImageLabel.setScaledContents(True)
        # self.setCentralWidget(self.footImageLabel)
        self.footImage = QImage()
        if self.footImage.load("../footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            self.resize(self.footImage.width(), self.footImage.height())
        self.refreshFootImageAfterChangeUserBox(0)

    # 刷新脚印压力图 从串口保存成png之后
    def refreshFootImageAfterSavingPNG(self):
        if self.footImage.load("../footPrints/tempBig.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))

    # 刷新脚印压力图 (人为鼠标点击改变,而不是程序改变)改变用户Box之后
    def refreshFootImageAfterChangeUserBox(self, uselessVar):
        currentUserName = self.getCurrentUserName()  # 获得用户名+id
        if (currentUserName == ''):
            print('没有用户')
            return False
        currentUserId = self.getCurrentUserId()  # 获得用户id

        self.query.prepare(""" SELECT footImg FROM footdata WHERE id=(?) """)
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()
        while self.query.next():
            byteDataReaded = self.query.value(0)
            try:  # 此用户数据库中有压力图
                imgSmall = Image.frombytes('RGB', (32, 44), byteDataReaded)
                imgSmall.save('../footPrints/tempSmall.png')
                imgBig = imgSmall.resize((320, 440))
                imgBig.save('../footPrints/tempBig.png')
                if self.footImage.load("../footPrints/tempBig.png"):
                    self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
                    return True
            except:  # 此用户数据库中没有压力图(还未采集)
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
            byteDataToWrite = imgRead.tobytes()

            currentUserName = self.getCurrentUserName()  # 获得用户名+id
            if (currentUserName == ''):
                QMessageBox.warning(self, "警告", "没有用户!无法保存压力图数据!\n请先在数据库里建立用户!", QMessageBox.Ok)
                return False

            currentUserId = self.getCurrentUserId()  # 获得用户id
            self.query.prepare(""" UPDATE footdata SET footImg=NULL WHERE id=(?) """)  # 清空
            self.query.addBindValue(QVariant(currentUserId))
            self.query.exec_()

            self.query.prepare(""" UPDATE footdata SET footImg=(?) WHERE id=(?) """)  # 写入
            self.query.addBindValue(QByteArray(byteDataToWrite))
            self.query.addBindValue(QVariant(currentUserId))
            self.query.exec_()

            QMessageBox.information(self, "成功", "成功保存压力图数据", QMessageBox.Ok)
            return True
        except:
            QMessageBox.warning(self, "警告", "没有可以用来保存的压力图数据!", QMessageBox.Ok)
            return False

    # 布局
    def setupLayout(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(1)

        leftSideLayout.addWidget(self.showUserInputDlgButton)
        leftSideLayout.addWidget(self.showAdminDataBaseDlgButton)
        leftSideLayout.addWidget(self.selectUserLabel)
        leftSideLayout.addWidget(self.selectUserBox)

        self.serialPortObject.setupLayout(leftSideLayout)
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
app.setApplicationName("足部压力采集系统")
app.setQuitOnLastWindowClosed(True)

window = MainWindow()

sys.exit(app.exec_())
