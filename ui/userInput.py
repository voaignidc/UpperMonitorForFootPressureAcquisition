#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

ID, USERNAME, SEX, AGE, FOOTIMG = range(5)

class UserInputDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.setupLayout()
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("用户信息录入")

    def setupUi(self):
        self.basicInfoLabel = QLabel("基本信息  ",self)
        self.userNameLabel = QLabel("姓名", self)
        self.userNameLineEdit = QLineEdit(self)
        self.sexLabel = QLabel("性别", self)
        self.sexBox = QComboBox(self)
        self.sexBox.addItem("男")
        self.sexBox.addItem("女")

        self.ageLabel = QLabel("年龄", self)
        self.ageLineEdit = QLineEdit(self)
        self.heightLabel = QLabel("身高", self)
        self.heightLineEdit = QLineEdit(self)
        self.weightLabel = QLabel("体重", self)
        self.weightLineEdit = QLineEdit(self)

        self.contactInfoLabel = QLabel("联系方式  ", self)
        self.phoneNumberLabel = QLabel("手机", self)
        self.phoneNumberLineEdit = QLineEdit(self)
        self.qqNumberLabel = QLabel("QQ", self)
        self.qqNumberLineEdit = QLineEdit(self)

        self.collectInfoLabel = QLabel("采集信息  ", self)
        self.collectTimeLabel = QLabel("时间", self)
        self.collectTimeLineEdit = QLineEdit(self)
        self.collectorNameLabel = QLabel("操作员", self)
        self.collectorNameLineEdit = QLineEdit(self)

        self.saveToDataBaseButton = QPushButton("保存", self)
        self.clearButton = QPushButton("清除", self)

    def setupLayout(self):
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.gridLayout.addWidget(self.basicInfoLabel, *(0,0))
        self.gridLayout.addWidget(self.userNameLabel, *(0,1))
        self.gridLayout.addWidget(self.userNameLineEdit, *(0,2))
        self.gridLayout.addWidget(self.sexLabel, *(0,3))
        self.gridLayout.addWidget(self.sexBox, *(0,4))

        self.gridLayout.addWidget(self.ageLabel, *(1,1))
        self.gridLayout.addWidget(self.ageLineEdit, *(1,2))
        self.gridLayout.addWidget(self.heightLabel, *(1,3))
        self.gridLayout.addWidget(self.heightLineEdit, *(1,4))
        self.gridLayout.addWidget(self.weightLabel, *(1,5))
        self.gridLayout.addWidget(self.weightLineEdit, *(1,6))

        self.gridLayout.addWidget(self.contactInfoLabel, *(2,0))
        self.gridLayout.addWidget(self.phoneNumberLabel, *(2,1))
        self.gridLayout.addWidget(self.phoneNumberLineEdit, *(2,2))
        self.gridLayout.addWidget(self.qqNumberLabel, *(2,3))
        self.gridLayout.addWidget(self.qqNumberLineEdit, *(2,4))


        self.gridLayout.addWidget(self.collectInfoLabel, *(3,0))
        self.gridLayout.addWidget(self.collectTimeLabel, *(3,1))
        self.gridLayout.addWidget(self.collectTimeLineEdit, *(3,2))
        self.gridLayout.addWidget(self.collectorNameLabel, *(3,3))
        self.gridLayout.addWidget(self.collectorNameLineEdit, *(3,4))

        self.gridLayout.addWidget(self.saveToDataBaseButton, *(4,2))
        self.gridLayout.addWidget(self.clearButton, *(4,4))


# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(True)
#
# window = UserInputDlg()
# window.show()
#
# sys.exit(app.exec_())