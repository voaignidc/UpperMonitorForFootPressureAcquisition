#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

MAC = False
ID, USERNAME, SEX, AGE , FOOTIMG= range(5)

class AdminDataBaseDlg(QDialog):
    dataBaseRecordChangeSignal = pyqtSignal() # 改变数据库行的信号
    def __init__(self, parent=None):
        super(AdminDataBaseDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable("footdata") # 数据库名称
        self.model.setSort(ID, Qt.AscendingOrder) # 默认用ID排序
        self.model.setHeaderData(ID, Qt.Horizontal, "用户ID")
        self.model.setHeaderData(USERNAME, Qt.Horizontal,"用户名")
        self.model.setHeaderData(SEX, Qt.Horizontal,"性别")
        self.model.setHeaderData(AGE, Qt.Horizontal,"年龄")
        self.model.setHeaderData(FOOTIMG, Qt.Horizontal,"足部压力数据")
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True) # 隐藏ID
        self.view.setColumnHidden(FOOTIMG, True) # 隐藏FOOTIMG
        self.view.resizeColumnsToContents()

        buttonBox = QDialogButtonBox()
        addButton = buttonBox.addButton("添加", QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("删除", QDialogButtonBox.ActionRole)
        sortButton = buttonBox.addButton("排序", QDialogButtonBox.ActionRole)
        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)
            sortButton.setFocusPolicy(Qt.NoFocus)

        menu = QMenu(self)
        sortByIDAction = menu.addAction("按ID排序")
        sortByUserNameAction = menu.addAction("按用户名排序")
        sortBySexAction = menu.addAction("按性别排序")
        sortByAgeAction = menu.addAction("按年龄排序")

        sortButton.setMenu(menu)
        closeButton = buttonBox.addButton("保存并退出", QDialogButtonBox.ActionRole) # 关闭按钮

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        '''以下为连接'''
        addButton.clicked.connect(self.addRecord) #添加数据
        deleteButton.clicked.connect(self.deleteRecord) #删除数据
        
        sortByIDAction.triggered.connect(lambda:self.sort(ID))
        sortByUserNameAction.triggered.connect(lambda:self.sort(USERNAME))
        sortBySexAction.triggered.connect(lambda:self.sort(SEX))
        sortByAgeAction.triggered.connect(lambda:self.sort(AGE))

        closeButton.clicked.connect(self.aboutToQuit)
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("数据库")

    # 按下closeButton按钮会执行这个
    def aboutToQuit(self):
        rowCount = self.model.rowCount()  # 返回当前有几行数据
        newRowSaved=self.model.insertRow(rowCount)  # 插入行,如果的确插入新行,返回Ture并插入新航;当正在新加行未编辑完时,返回False,不插入
        index = self.model.index(rowCount, USERNAME) # 返回QModelIndex对象,rowCount是行的序号(从0开始)
        self.model.removeRow(index.row())
        if newRowSaved == False:
            QMessageBox.warning(self,"警告","还有数据未保存!\n请按添加键保存!\n或者删除未编辑完的数据!", QMessageBox.Ok)
        else:
            self.accept()  # 确定并退出对话框

    # 如果用户直接点红叉关闭
    def closeEvent(self, QCloseEvent):
        rowCount = self.model.rowCount()  # 返回当前有几行数据
        newRowSaved=self.model.insertRow(rowCount)  # 插入行,如果的确插入新行,返回Ture并插入新航;当正在新加行未编辑完时,返回False,不插入
        index = self.model.index(rowCount, USERNAME) # 返回QModelIndex对象,rowCount是行的序号(从0开始)
        self.model.removeRow(index.row())
        if newRowSaved == False:
            QMessageBox.warning(self, "警告", "数据未保存!", QMessageBox.Ok)

    #向数据库添加数据
    def addRecord(self):
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
            print('addRecord Fun in db.py')
            self.dataBaseRecordChangeSignal.emit()

    #删除数据
    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        userName = record.value(USERNAME)
        sex = record.value(SEX)
        if (QMessageBox.question(self, "数据库",
                ("删除此行数据({0}-{1})?"
                .format(userName,sex)),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()
        self.dataBaseRecordChangeSignal.emit()

    #按规则排序
    def sort(self, column):
        self.model.setSort(column, Qt.AscendingOrder)
        self.model.select()

#初始化数据库
def setupDatabase():
    filename = os.path.join(os.path.dirname(__file__), "footdata.db")
    create = not QFile.exists(filename)

    # 连接数据库
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "数据库",
            "Database Error: {0}".format(db.lastError().text()))
        sys.exit(1)

    if create:
        query = QSqlQuery()
        query.exec_("""CREATE TABLE footdata (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                userName VARCHAR(255) NOT NULL,
                sex VARCHAR(255),
                age VARCHAR(255),
                footImg BLOB)""")
    
'''以下主函数'''
setupDatabase()