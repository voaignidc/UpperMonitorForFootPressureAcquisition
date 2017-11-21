#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

class SignInDlg(QDialog):
    signInSignal = pyqtSignal() # 登录 信号
    adminPermissionSignal = pyqtSignal() # 管理员权限 信号
    newUserSignUpSignal = pyqtSignal() # 新用户注册
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint) # 关闭问号
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("登录")
        self.show()

    def connectSignalSlot(self):
        self.signInButton.clicked.connect(self.signIn)
        self.signUpButton.clicked.connect(self.signUp)

    # 获得LineEdit里的账号名及密码
    def getAccountFromLineEdit(self):
        name = self.accountNameLineEdit.text()
        password = self.accountPasswordLineEdit.text()
        return (name, password)

    # 与 数据库里的账号名及密码 进行对比
    def compareAccount(self, nameFromLineEdit, passwordFromLineEdit):
        ifGetPassword = False
        ifPasswordCorrect = False
        self.query.prepare(""" SELECT accountPassword FROM footdata WHERE accountName = (?)""")
        self.query.addBindValue(QVariant(nameFromLineEdit))
        self.query.exec_()

        while self.query.next():
            password = self.query.value(0)
            print('密码:',password)
            ifGetPassword = True
            ifPasswordCorrect = (password == passwordFromLineEdit)

        return (ifGetPassword and ifPasswordCorrect)

    # 登录
    def signIn(self):
        self.signInButton.setChecked(False)
        nameFromLineEdit, passwordFromLineEdit = self.getAccountFromLineEdit()

        if nameFromLineEdit == 'admin':
            if passwordFromLineEdit == '1234':
                self.signInSignal.emit()
                self.adminPermissionSignal.emit()
            else:
                QMessageBox.warning(self, "警告", "密码错误!", QMessageBox.Ok)
        else:
            if self.compareAccount(nameFromLineEdit, passwordFromLineEdit):
                self.signInSignal.emit()
            else:
                QMessageBox.warning(self, "警告", "用户名不存在 或 密码错误!", QMessageBox.Ok)

    # 注册
    def signUp(self):
        self.signUpButton.setChecked(False)
        self.newUserSignUpSignal.emit()
        self.signInSignal.emit()

    def setupUi(self):
        self.titleLabel = QLabel("足部压力采集系统", self)
        self.titleLabel.setFont(QFont("Roman times", 12, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.accountNameLabel = QLabel("账号:  ", self)
        self.accountNameLineEdit = QLineEdit(self)
        # self.accountNameLineEdit.setPlaceholderText("3-18个英文或数字")
        self.accountNameLineEdit.setMaxLength(18)
        self.accountNameLineEdit.setFixedWidth(220)

        self.accountPasswordLabel = QLabel("密码:  ", self)
        self.accountPasswordLineEdit = QLineEdit(self)
        self.accountPasswordLineEdit.setEchoMode(QLineEdit.Password) # 用小黑点覆盖你所输入的字符
        # self.accountPasswordLineEdit.setPlaceholderText("3-12个英文或数字")
        self.accountPasswordLineEdit.setMaxLength(12)

        self.signInButton = QPushButton("登录", self)
        self.signUpButton = QPushButton("注册", self)

    def setupLayout(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.titleLabel, *(0, 0), *(1, 0)) # 前两个数,是起始位置;后两个数,是行跨度和列跨度
        self.gridLayout.addWidget(self.accountNameLabel, *(1, 0))
        self.gridLayout.addWidget(self.accountNameLineEdit, *(1, 1))
        self.gridLayout.addWidget(self.accountPasswordLabel, *(2, 0))
        self.gridLayout.addWidget(self.accountPasswordLineEdit, *(2, 1))

        self.bottomSideLayout = QHBoxLayout()
        self.bottomSideLayout.addWidget(self.signInButton)
        self.bottomSideLayout.addWidget(self.signUpButton)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.gridLayout)
        self.mainLayout.addLayout(self.bottomSideLayout)
        self.setLayout(self.mainLayout)



# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(True)
#
# window = SignInDlg()
# window.show()
#
# sys.exit(app.exec_())