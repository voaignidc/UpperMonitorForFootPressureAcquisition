#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

class SignInDlg(QDialog):
    def __init__(self):
        super().__init__()
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

    # 获得账号名及密码
    def getAccount(self):
        accountName = self.accountNameLineEdit.text()
        accountPassword = self.accountPasswordLineEdit.text()
        print(accountName)
        print(accountPassword)

    # 登录
    def signIn(self):
        self.getAccount()
        self.signInButton.setChecked(False)

    def setupUi(self):
        self.titleLabel = QLabel("足部压力采集系统", self)
        self.titleLabel.setFont(QFont("Roman times", 12, QFont.Bold))
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.accountNameLabel = QLabel("账号:  ", self)
        self.accountNameLineEdit = QLineEdit(self)
        self.accountNameLineEdit.setPlaceholderText("3-18个英文或数字")

        self.accountPasswordLabel = QLabel("密码:  ", self)
        self.accountPasswordLineEdit = QLineEdit(self)
        self.accountPasswordLineEdit.setEchoMode(QLineEdit.Password) # 用小黑点覆盖你所输入的字符
        self.accountPasswordLineEdit.setPlaceholderText("3-18个英文或数字")

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