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
    def __init__(self, nowAccountName, ifNewAccount):
        super().__init__()
        self.query = QSqlQuery()
        self.nowAccountName = nowAccountName # 现在登录的账户名
        self.ifNewAccount = ifNewAccount # 新账户标志
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()
        if (self.nowAccountName != '') and (self.nowAccountName != 'admin'):
            self.showAllFromDataBase()

    def connectSignalSlot(self):
        self.saveToDataBaseButton.clicked.connect(self.addRecord)
        self.clearButton.clicked.connect(self.showAllFromDataBase)

    def ifAccountNameAndPasswordValid(self):
        '''检查账户名,账户密码,姓名是否合法'''
        valid = len(self.accountNameLineEdit.text()) >= 3 and len(self.accountPasswordLineEdit.text()) >= 3 \
                and len(self.userNameLineEdit.text()) > 0
        return valid

    def ifAccountNameRepeat(self, name):
        '''检查账户名是否与已有账户名重复'''
        isRepeated = False # 返回真,则重复
        if name == 'admin':
            isRepeated = True
        self.query.prepare(""" SELECT accountName FROM footdata WHERE accountName = (?)""")
        self.query.addBindValue(QVariant(name))
        self.query.exec_()
        if self.query.next():
            isRepeated = True
        return isRepeated

    def addRecord(self):
        '''向数据库加数据'''
        self.saveToDataBaseButton.setChecked(False)
        if not self.ifAccountNameAndPasswordValid():
            QMessageBox.warning(self, "警告", "账户名,账户密码,姓名是必填项!", QMessageBox.Ok)
        all = self.getAllFromLineEdit()

        if not self.ifAccountNameRepeat(self.accountNameLineEdit.text()): # 新建账号
            self.query.prepare(""" INSERT INTO footdata (accountName, accountPassword, userName, sex, age, height, weight, 
                    phoneNumber, qqNumber, collectTime, collectorName) VALUES (?,?,?,?,?,?,?,?,?,?,?) """)
            for i in range(11):
                self.query.addBindValue(QVariant(all[i]))
            self.query.exec_()
            self.dataBaseRecordChangeSignal.emit()
            QMessageBox.information(self, "成功", "用户信息录入成功!", QMessageBox.Ok)
            self.ifNewAccount = False
            self.nowAccountName = all[0]
            self.close()
        else: # 已有账号
            if self.ifNewAccount:
                QMessageBox.warning(self, "警告", "此账号已存在,请换一个账号名!", QMessageBox.Ok)
                return
            if (QMessageBox.question(self, "用户信息录入", "确认覆盖?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
                return
            self.query.prepare(""" UPDATE footdata SET accountPassword=(?), userName=(?), sex=(?), age=(?), height=(?), weight=(?),
                      phoneNumber=(?), qqNumber=(?), collectTime=(?), collectorName=(?) WHERE accountName=(?)""")
            for i in range(10):
                self.query.addBindValue(QVariant(all[i+1]))
            self.query.addBindValue(QVariant(all[0]))
            self.query.exec_()
            QMessageBox.information(self, "成功", "用户信息覆盖成功!", QMessageBox.Ok)
            self.close()


    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("用户信息录入")

    def getAllFromLineEdit(self):
        '''获得LineEdit里的全部信息'''
        return self.accountNameLineEdit.text(), self.accountPasswordLineEdit.text(), self.userNameLineEdit.text(),\
               self.sexBox.currentText(), self.ageLineEdit.text(), self.heightLineEdit.text(), self.weightLineEdit.text(),\
               self.phoneNumberLineEdit.text(), self.qqNumberLineEdit.text(), self.collectTimeLineEdit.text(), \
               self.collectorNameLineEdit.text()

    def showAllFromDataBase(self):
        '''获得数据库里的信息,放到LineEdit里'''
        self.query.prepare(""" SELECT accountName, accountPassword, userName, sex, age, height, weight, 
                phoneNumber, qqNumber, collectTime, collectorName FROM footdata WHERE accountName=(?) """)
        self.query.addBindValue(self.nowAccountName)
        self.query.exec_()
        while self.query.next():
            info = []
            for i in range(11):
                info.append(self.query.value(i))
            self.accountNameLineEdit.setText(info[0])
            self.accountPasswordLineEdit.setText(info[1])
            self.userNameLineEdit.setText(info[2])
            if info[3] == '男':
                self.sexBox.setCurrentIndex(0)
            else:
                self.sexBox.setCurrentIndex(1)
            self.ageLineEdit.setText(info[4])
            self.heightLineEdit.setText(info[5])
            self.weightLineEdit.setText(info[6])
            self.phoneNumberLineEdit.setText(info[7])
            self.qqNumberLineEdit.setText(info[8])
            self.collectTimeLineEdit.setText(info[9])
            self.collectorNameLineEdit.setText(info[10])

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
