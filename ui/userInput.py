#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

ID, ACCOUNTNAME, ACCOUNTPASSWORD, USERNAME, FOOTIMG, SEX, AGE, HEIGHT, WEIGHT, PHONENUMBER, \
QQNUMBER, COLLECTTIME, COLLECTORNAME = range(13)

class UserInputDlg(QDialog):
    dataBaseRecordChangeSignal = pyqtSignal()  # 改变数据库行的信号
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()

    def connectSignalSlot(self):
        self.saveToDataBaseButton.clicked.connect(self.addRecord)

    # 检查账户名,账户密码,姓名是否合法
    def ifAccountNameAndPasswordValid(self):
        valid = len(self.accountNameLineEdit.text()) >= 3 and len(self.accountPasswordLineEdit.text()) >= 3 \
                and len(self.userNameLineEdit.text()) > 0
        return valid

    # 检查账户名是否与已有账户名重复
    def ifAccountNameRepeat(self):
        isRepeated = False # 返回真,则重复
        nameFromLineEdit = self.accountNameLineEdit.text()
        if nameFromLineEdit == 'admin':
            isRepeated = True
        self.query.prepare(""" SELECT accountName FROM footdata WHERE accountName = (?)""")
        self.query.addBindValue(QVariant(nameFromLineEdit))
        self.query.exec_()

        if self.query.next():
            isRepeated = True
        return isRepeated

    # 向数据库加数据
    def addRecord(self):
        self.saveToDataBaseButton.setChecked(False)
        if not self.ifAccountNameAndPasswordValid():
            QMessageBox.warning(self, "警告", "账户名,账户密码,姓名是必填项!", QMessageBox.Ok)
        all = self.getAllFromLineEdit()
        if not self.ifAccountNameRepeat(): # 新建
            self.query.prepare(""" INSERT INTO footdata (accountName, accountPassword, userName, sex, age, 
                    height, weight, phoneNumber, qqNumber, collectTime, collectorName) VALUES (?,?,?,?,?,?,?,?,?,?,?) """)
            for i in range(11):
                self.query.addBindValue(QVariant(all[i]))
            self.query.exec_()
            self.dataBaseRecordChangeSignal.emit()
            QMessageBox.information(self, "成功", "用户信息录入成功!", QMessageBox.Ok)
            self.close()

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("用户信息录入")



    def getAllFromLineEdit(self):
        return self.accountNameLineEdit.text(), self.accountPasswordLineEdit.text(), self.userNameLineEdit.text(),\
               self.sexBox.currentText(), self.ageLineEdit.text(), self.heightLineEdit.text(), self.weightLineEdit.text(),\
               self.phoneNumberLineEdit.text(), self.qqNumberLineEdit.text(), self.collectTimeLineEdit.text(), \
               self.collectorNameLineEdit.text()


    def setupUi(self):
        self.accountInfoLabel = QLabel("账户信息  ",self)
        self.accountNameLabel = QLabel("账户名", self)
        self.accountNameLineEdit = QLineEdit(self)
        self.accountNameLineEdit.setPlaceholderText("3-18个英文或数字")
        self.accountNameLineEdit.setMaxLength(18)
        self.accountNameLineEdit.setFixedWidth(220)

        self.accountPasswordLabel = QLabel("账户密码", self)
        self.accountPasswordLineEdit = QLineEdit(self)
        self.accountPasswordLineEdit.setPlaceholderText("3-12个英文或数字")
        self.accountPasswordLineEdit.setEchoMode(QLineEdit.Password)  # 用小黑点覆盖你所输入的字符
        self.accountPasswordLineEdit.setFixedWidth(220)
        self.accountPasswordLineEdit.setMaxLength(12)

        self.basicInfoLabel = QLabel("基本信息  ",self)
        self.userNameLabel = QLabel("姓名", self)
        self.userNameLineEdit = QLineEdit(self)
        self.sexLabel = QLabel("  性别", self)
        self.sexBox = QComboBox(self)
        self.sexBox.addItem("男")
        self.sexBox.addItem("女")

        self.ageLabel = QLabel("年龄", self)
        self.ageLineEdit = QLineEdit(self)
        self.heightLabel = QLabel("  身高", self)
        self.heightLineEdit = QLineEdit(self)
        self.weightLabel = QLabel("体重", self)
        self.weightLineEdit = QLineEdit(self)

        self.contactInfoLabel = QLabel("联系方式  ", self)
        self.phoneNumberLabel = QLabel("手机", self)
        self.phoneNumberLineEdit = QLineEdit(self)
        self.qqNumberLabel = QLabel("   QQ", self)
        self.qqNumberLineEdit = QLineEdit(self)

        self.collectInfoLabel = QLabel("采集信息  ", self)
        self.collectTimeLabel = QLabel("时间", self)
        self.collectTimeLineEdit = QLineEdit(self)
        self.collectTimeLineEdit.setEnabled(False)

        self.collectorNameLabel = QLabel(" 操作员", self)
        self.collectorNameLineEdit = QLineEdit(self)

        self.saveToDataBaseButton = QPushButton("保存", self)
        self.clearButton = QPushButton("清除", self)

    def setupLayout(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.setLayout(self.gridLayout)

        self.gridLayout.addWidget(self.accountInfoLabel, *(0,0))
        self.gridLayout.addWidget(self.accountNameLabel, *(0,1))
        self.gridLayout.addWidget(self.accountNameLineEdit, *(0,2))
        self.gridLayout.addWidget(self.accountPasswordLabel, *(0,3))
        self.gridLayout.addWidget(self.accountPasswordLineEdit, *(0,4))

        self.gridLayout.addWidget(self.basicInfoLabel, *(1,0))
        self.gridLayout.addWidget(self.userNameLabel, *(1,1))
        self.gridLayout.addWidget(self.userNameLineEdit, *(1,2))
        self.gridLayout.addWidget(self.sexLabel, *(1,3))
        self.gridLayout.addWidget(self.sexBox, *(1,4))

        self.gridLayout.addWidget(self.ageLabel, *(2,1))
        self.gridLayout.addWidget(self.ageLineEdit, *(2,2))
        self.gridLayout.addWidget(self.heightLabel, *(2,3))
        self.gridLayout.addWidget(self.heightLineEdit, *(2,4))
        self.gridLayout.addWidget(self.weightLabel, *(3,1))
        self.gridLayout.addWidget(self.weightLineEdit, *(3,2))

        self.gridLayout.addWidget(self.contactInfoLabel, *(4,0))
        self.gridLayout.addWidget(self.phoneNumberLabel, *(4,1))
        self.gridLayout.addWidget(self.phoneNumberLineEdit, *(4,2))
        self.gridLayout.addWidget(self.qqNumberLabel, *(4,3))
        self.gridLayout.addWidget(self.qqNumberLineEdit, *(4,4))


        self.gridLayout.addWidget(self.collectInfoLabel, *(5,0))
        self.gridLayout.addWidget(self.collectTimeLabel, *(5,1))
        self.gridLayout.addWidget(self.collectTimeLineEdit, *(5,2))
        self.gridLayout.addWidget(self.collectorNameLabel, *(5,3))
        self.gridLayout.addWidget(self.collectorNameLineEdit, *(5,4))

        self.gridLayout.addWidget(self.saveToDataBaseButton, *(6,2))
        self.gridLayout.addWidget(self.clearButton, *(6,4))


# app = QApplication(sys.argv)
# app.setQuitOnLastWindowClosed(True)
#
# window = UserInputDlg()
# window.show()
#
# sys.exit(app.exec_())