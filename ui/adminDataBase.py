#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

MAC = False
ID, ACCOUNTNAME, ACCOUNTPASSWORD, USERNAME, FOOTIMG, FOOTVOLTAGE, SEX, AGE, HEIGHT, WEIGHT, PHONENUMBER, \
QQNUMBER, COLLECTTIME, COLLECTORNAME = range(14)

class AdminDataBaseDlg(QDialog):
    dataBaseRecordChangeSignal = pyqtSignal() # 改变数据库行的信号
    def __init__(self, parent=None):
        super(AdminDataBaseDlg, self).__init__(parent)
        self.model = QSqlTableModel(self)
        self.view = QTableView()
        self.setupSqlTableModel()
        self.setupTableView()
        self.showButton()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()

    def setupSqlTableModel(self):
        self.model.setTable("footdata") # 数据库名称
        self.model.setSort(ID, Qt.AscendingOrder) # 默认用ID排序
        self.model.setHeaderData(ID, Qt.Horizontal, "ID")
        self.model.setHeaderData(ACCOUNTNAME, Qt.Horizontal, "账户名")
        self.model.setHeaderData(ACCOUNTPASSWORD, Qt.Horizontal, "账户密码")
        self.model.setHeaderData(USERNAME, Qt.Horizontal,"姓名")
        self.model.setHeaderData(FOOTIMG, Qt.Horizontal, "足部压力图像")
        self.model.setHeaderData(FOOTVOLTAGE, Qt.Horizontal, "足部压力电压值")
        self.model.setHeaderData(SEX, Qt.Horizontal,"性别")
        self.model.setHeaderData(AGE, Qt.Horizontal,"年龄")
        self.model.setHeaderData(HEIGHT, Qt.Horizontal,"身高")
        self.model.setHeaderData(WEIGHT, Qt.Horizontal,"体重")
        self.model.setHeaderData(PHONENUMBER, Qt.Horizontal,"手机")
        self.model.setHeaderData(QQNUMBER, Qt.Horizontal,"QQ")
        self.model.setHeaderData(COLLECTTIME, Qt.Horizontal,"时间")
        self.model.setHeaderData(COLLECTORNAME, Qt.Horizontal,"操作员")

        self.model.select()

    def setupTableView(self):
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True) # 隐藏ID
        self.view.setColumnHidden(FOOTIMG, True)
        self.view.setColumnHidden(FOOTVOLTAGE, True)
        self.view.resizeColumnsToContents()

    def showButton(self):
        self.buttonBox = QDialogButtonBox()
        self.addButton = self.buttonBox.addButton("添加", QDialogButtonBox.ActionRole)
        self.deleteButton = self.buttonBox.addButton("删除", QDialogButtonBox.ActionRole)
        self.sortButton = self.buttonBox.addButton("排序", QDialogButtonBox.ActionRole)
        if not MAC:
            self.addButton.setFocusPolicy(Qt.NoFocus)
            self.deleteButton.setFocusPolicy(Qt.NoFocus)
            self.sortButton.setFocusPolicy(Qt.NoFocus)

        self.menu = QMenu(self)
        self.sortByIDAction = self.menu.addAction("按ID排序")
        self.sortByUserNameAction = self.menu.addAction("按用户名排序")
        self.sortBySexAction = self.menu.addAction("按性别排序")
        self.sortByAgeAction = self.menu.addAction("按年龄排序")

        self.sortButton.setMenu(self.menu)
        self.closeButton = self.buttonBox.addButton("保存并退出", QDialogButtonBox.ActionRole) # 关闭按钮

    def setupLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def connectSignalSlot(self):
        '''连接'''
        self.addButton.clicked.connect(self.addRecord) # 添加数据
        self.deleteButton.clicked.connect(self.deleteRecord) # 删除数据

        self.sortByIDAction.triggered.connect(lambda:self.sort(ID))
        self.sortByUserNameAction.triggered.connect(lambda:self.sort(USERNAME))
        self.sortBySexAction.triggered.connect(lambda:self.sort(SEX))
        self.sortByAgeAction.triggered.connect(lambda:self.sort(AGE))

        self.closeButton.clicked.connect(self.aboutToQuit)

    def showUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("./icons/foot32.png"))
        self.setWindowTitle("数据库")
        self.resize(850,700)

    def aboutToQuit(self):
        '''按下closeButton按钮会执行这个'''
        rowCount = self.model.rowCount()  # 返回当前有几行数据
        newRowSaved = self.model.insertRow(rowCount)  # 插入行,如果的确插入新行,返回Ture并插入新航;当正在新加行未编辑完时,返回False,不插入
        index = self.model.index(rowCount, USERNAME) # 返回QModelIndex对象,rowCount是行的序号(从0开始)
        self.model.removeRow(index.row())
        if newRowSaved == False:
            QMessageBox.warning(self,"警告","还有数据未保存!\n请按添加键保存!\n或者删除未编辑完的数据!", QMessageBox.Ok)
        else:
            self.accept()  # 确定并退出对话框

    def closeEvent(self, QCloseEvent):
        '''如果用户直接点红叉关闭'''
        rowCount = self.model.rowCount()  # 返回当前有几行数据
        newRowSaved=self.model.insertRow(rowCount)  # 插入行,如果的确插入新行,返回Ture并插入新航;当正在新加行未编辑完时,返回False,不插入
        index = self.model.index(rowCount, USERNAME) # 返回QModelIndex对象,rowCount是行的序号(从0开始)
        self.model.removeRow(index.row())
        if newRowSaved == False:
            QMessageBox.warning(self, "警告", "数据未保存!", QMessageBox.Ok)


    def addRecord(self):
        '''向数据库添加数据'''
        rowCount = self.model.rowCount() # 返回当前有几行数据
        self.model.insertRow(rowCount) # 插入行,如果的确插入新行,返回Ture并插入新航;当正在新加行未编辑完时,返回False,不插入
        # 如果在这里调用rowCount = self.model.rowCount(),会发现rowCount+1了
        index = self.model.index(rowCount, USERNAME) # 返回QModelIndex对象,rowCount是行的序号(从0开始)
        self.view.setCurrentIndex(index)
        # 如果在这里调用nowRow = self.view.currentIndex().row(),nowRow是 QModelIndex对象所在行的序号(从0开始)
        self.view.edit(index)

        nowRow = self.view.currentIndex().row()
        if nowRow == -1: # 如果新加行未编辑完时按,那么nowRow==-1
            # QMessageBox.information(self,"成功","录入成功", QMessageBox.Ok)
            # print('addRecord Fun in db.py')
            self.dataBaseRecordChangeSignal.emit()


    def deleteRecord(self):
        '''删除数据'''
        index = self.view.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        userName = record.value(USERNAME)
        sex = record.value(SEX)
        if (QMessageBox.question(self, "数据库",("删除此行数据({0}-{1})?".format(userName,sex)),
                                 QMessageBox.Yes|QMessageBox.No) ==QMessageBox.No):
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()
        self.dataBaseRecordChangeSignal.emit()


    def sort(self, column):
        '''按规则排序'''
        self.model.setSort(column, Qt.AscendingOrder)
        self.model.select()


def connectDataBaseFile(fileName):
    '''连接数据库文件, 若不存在则创建一个'''
    create = not QFile.exists(fileName)
    db = QSqlDatabase.addDatabase("QSQLITE") # 连接数据库
    db.setDatabaseName(fileName)

    if not db.open():
        QMessageBox.warning(None, "数据库", "Database Error: {0}".format(db.lastError().text()))
        sys.exit(1)

    if create:
        query = QSqlQuery()
        query.exec_("""CREATE TABLE footdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,      
                accountName VARCHAR(255) NOT NULL,
                accountPassword VARCHAR(255) NOT NULL,
                userName VARCHAR(255) NOT NULL,
                footImg BLOB,
                footVoltage TEXT(65535),
                sex VARCHAR(255),
                age VARCHAR(255),
                height VARCHAR(255),
                weight VARCHAR(255),
                phoneNumber VARCHAR(255),
                qqNumber VARCHAR(255),
                collectTime VARCHAR(255),
                collectorName VARCHAR(255)
                )""")