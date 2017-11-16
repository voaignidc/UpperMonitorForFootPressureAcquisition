#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

MAC = False
ID, USERNAME, SEX, AGE = range(4)

class DataBaseDlg(QDialog):
    def __init__(self, parent=None):
        super(DataBaseDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable("footdata") # 数据库名称
        self.model.setSort(ID, Qt.AscendingOrder) # 默认用ID排序
        self.model.setHeaderData(ID, Qt.Horizontal, "用户ID")
        self.model.setHeaderData(USERNAME, Qt.Horizontal,"用户名")
        self.model.setHeaderData(SEX, Qt.Horizontal,"性别")
        self.model.setHeaderData(AGE, Qt.Horizontal,"年龄")
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True) # 隐藏ID
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
        closeButton = buttonBox.addButton(QDialogButtonBox.Close)#关闭按钮

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
        
        closeButton.clicked.connect(self.accept)
        self.setWindowIcon(QIcon("../icons/foot32.png"))
        self.setWindowTitle("数据库")

    #向数据库添加数据
    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, USERNAME)
        self.view.setCurrentIndex(index)
        self.view.edit(index)

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
                userName VARCHAR(80) NOT NULL,
                sex VARCHAR(30) NOT NULL,
                age VARCHAR(20))""")
    
'''以下主函数'''
setupDatabase()