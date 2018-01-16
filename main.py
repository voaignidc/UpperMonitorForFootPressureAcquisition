#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

"""主函数"""
app = QApplication(sys.argv)
app.setApplicationName("足部压力采集系统")
app.setQuitOnLastWindowClosed(True)

from ui import *

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)  
pathName = rootPath+"/dataBaseFile"
fileName = rootPath+"/dataBaseFile/footdata.db"
print(fileName)
adminDataBase.connectDataBaseFile(pathName, fileName)

class MainWindow(QMainWindow, QWidget):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self._adminPermission = False # 管理员权限标志
        self.ifNewAccount = False # 新账户标志
        self.nowAccountName = '' # 当前账户名
        self.setupDataBaseUI()
        self.setupSignInDlg()

    def setupSignInDlg(self):
        """初始化登录界面"""
        self.signInDlg = signIn.SignInDlg()
        self.signInDlg.closeSignInDlgSignal.connect(self.setupMainWindow) # 只有登录了,才能显示主窗口
        self.signInDlg.adminPermissionSignal.connect(self.getAdminPermission)
        self.signInDlg.newUserSignUpSignal.connect(self.signUpAsNewUser)
        self.signInDlg.nowAccountNameSignal[str].connect(self.getNowAccountName)

    def getNowAccountName(self, name):
        """获得当前用户的名字"""
        self.nowAccountName = name
        print('nowAccountName =',name)

    def signUpAsNewUser(self):
        '''新用户注册'''
        self.ifNewAccount = True

    def getAdminPermission(self):
        '''获得管理员权限'''
        self._adminPermission = True
        print('getAdminPermission')

    def setupMainWindow(self):
        '''初始化主窗口'''
        self.signInDlg.close()
        self.setupUserInputDlg()
        self.serialPortObject = serialPort.SerialPortClass()
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()
        if self.ifNewAccount:
            self.userInputDlg.show()
            self.userInputDlg.collectTimeLineEdit.setText(currentTime.getCurrentTime())
        self.setupPressureAnalysisDlg()

    def setupUi(self):
        '''初始化主窗口Ui'''
        self.showButton()
        self.setupScaleImageAndFootImage()
        self.showScaleImageAndFootImage()

    def showUi(self):
        """显示主窗口"""
        self.show()
        self.setWindowIcon(QIcon("./icons/foot32.png"))

    def connectSignalSlot(self):
        """连接信号与槽"""
        self.showUserInputDlgButton.clicked.connect(self.showUserInputDlg)  # 连 显示用户录入对话框
        self.showAdminDataBaseDlgButton.clicked.connect(self.showAdminDataBaseDlg)
        self.serialPortObject.finishSavingPNGSingal.connect(self.refreshFootImageFromPNG)  # '保存完毕'信号
        # 连 刷新图像
        self.clearFootImageButton.clicked.connect(self.clearFootImage)
        self.saveFootImageButton.clicked.connect(self.saveFootDataToDataBase)
        self.loadFootImageButton.clicked.connect(self.loadFootImageButtonPressed)
        self.selectUserBox.activated[int].connect(self.refreshFootImageAndVoltageTxtAfterChangeUserBox) # activated是用户点击
        # QComboBox后才产生的信号,程序改变QComboBox则不产生此信号
        self.showPressureAnalysisButton.clicked.connect(self.showPressureAnalysisDlg)
        self.selectUserBox.activated.connect(self.refreshPressureAnalysisDlg)

    def setupDataBaseUI(self):
        """初始化数据库"""
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

    def refreshUserNameBox(self):
        """刷新用户Box"""
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

    def getCurrentUserId(self):
        """获得当前是哪个ID"""
        currentUserName = self.selectUserBox.currentText()
        currentUserId = currentUserName.split('=')[1]
        return currentUserId

    def showButton(self):
        """显示按钮"""
        self.showUserInputDlgButton = QPushButton("信息录入", self)
        self.showUserInputDlgButton.setCheckable(True)
        self.showAdminDataBaseDlgButton = QPushButton("用户管理", self)  # 数据库按钮在这里
        self.showAdminDataBaseDlgButton.setCheckable(True)

        self.clearFootImageButton = QPushButton("清除压力图", self)
        self.clearFootImageButton.setCheckable(True)
        self.saveFootImageButton = QPushButton("保存压力图", self)
        self.saveFootImageButton.setCheckable(True)
        self.loadFootImageButton = QPushButton("读取压力图", self)
        self.loadFootImageButton.setCheckable(True)
        self.showPressureAnalysisButton = QPushButton("压强分析", self)
        self.showPressureAnalysisButton.setCheckable(True)

        
    def loadFootImageButtonPressed(self):
        """读取imgRead.png, 刷新UI上的脚印压力图"""
        self.loadFootImageButton.setChecked(False)
        successfullyLoad = False
        if self.footImage.load("./footPrints/imgRead.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            successfullyLoad = True
        return successfullyLoad
        
        
    def setupUserInputDlg(self):
        """初始化 用户录入 对话框"""
        self.userInputDlg = userInput.UserInputDlg(self.nowAccountName, self.ifNewAccount)
        self.userInputDlg.dataBaseRecordChangeSignal.connect(self.refreshDataBase)

    def refreshDataBase(self):
        """用户录入 对话框 点完保存后, 再重新载入数据库"""
        self.adminDataBaseDlg.setupSqlTableModel()
        self.adminDataBaseDlg.setupTableView()
        self.refreshUserNameBox()

    def showUserInputDlg(self):
        """显示 用户录入 对话框"""
        self.showUserInputDlgButton.setChecked(False)
        self.userInputDlg.show()
        self.userInputDlg.collectTimeLineEdit.setText(currentTime.getCurrentTime())

    def setupScaleImageAndFootImage(self):
        """初始化两个图, 左侧的刻度图, 和右侧足底压力图"""
        self.scaleImageLabel = QLabel(self) # 左侧的刻度图
        self.scaleImage = QImage()
        self.footImageLabel = QLabel(self) # 足底压力图
        self.footImage = QImage()

    def showScaleImageAndFootImage(self):
        """显示两个图, 左侧的刻度图, 和右侧足底压力图"""
        if self.scaleImage.load("./icons/arr.png"):
            self.scaleImageLabel.setPixmap(QPixmap.fromImage(self.scaleImage))

        if self.footImage.load("./footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            self.resize(self.footImage.width(), self.footImage.height())

        self.refreshFootImageAndVoltageTxtAfterChangeUserBox(0)

    def refreshFootImageFromPNG(self):
        """读取png, 刷新UI上的脚印压力图"""
        successfullyLoad = False
        if self.footImage.load("./footPrints/tempBig.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            successfullyLoad = True
        return successfullyLoad

    def refreshBlankImageFromPNG(self):
        """读取空白的那个png, 刷新UI上的脚印压力图"""
        successfullyLoad = False
        if self.footImage.load("./footPrints/blank.png"):
            self.footImageLabel.setPixmap(QPixmap.fromImage(self.footImage))
            successfullyLoad = True
        return successfullyLoad

    def refreshFootImageAndVoltageTxtAfterChangeUserBox(self, uselessVar):
        """改变用户Box之后(人为鼠标点击改变,而不是程序改变), 刷新UI上的脚印压力图, 刷新txt
        Return:
            True: if 成功刷新
            False: if 刷新失败
        """
        currentUserName = self.getCurrentUserName()  # 获得用户名+id
        if (currentUserName == ''):
            print('no users')
            return False
        currentUserId = self.getCurrentUserId()  # 获得用户id
        if self.loadAndRefreshFootImgFromDataBase(currentUserId): # 刷新UI上的脚印压力图
            return self.loadFootVoltageFromDataBase(currentUserId) # 刷新txt
        else:
            return False

    def loadAndRefreshFootImgFromDataBase(self, currentUserId):
        """从数据库读取脚印压力图像的二进制数据,
           转换成png
           并保存到footPrints文件夹
           再显示到主窗口UI
        """
        self.query.prepare(""" SELECT footImg FROM footdata WHERE id=(?) """)
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()
        while self.query.next():
            byteDataReaded = self.query.value(0)
            try: # 此用户数据库中有压力图
                imgSmall = Image.frombytes('RGB', (32, 44), byteDataReaded)
                imgSmall.save('./footPrints/tempSmall.png')
                imgBig = imgSmall.resize((320, 440))
                imgBig.save('./footPrints/tempBig.png')
                return self.refreshFootImageFromPNG()
            except: # 此用户数据库中没有压力图(还未采集)
                self.refreshBlankImageFromPNG()
                return False

    def loadFootVoltageFromDataBase(self, currentUserId):
        """从数据库读取脚印压力电压值的字符串
           转换成txt
           并保存到footPrints文件夹
        """
        self.query.prepare(""" SELECT footVoltage FROM footdata WHERE id=(?) """)
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()
        successfullyRead = False
        successfullyWrite = False
        while self.query.next():
            stringReaded = self.query.value(0)
            successfullyRead = True
        if successfullyRead:
            with open('./footPrints/voltageArr.txt', 'w+') as f:
                f.write(stringReaded)
            successfullyWrite = True
        return successfullyRead and successfullyWrite

    def clearFootImage(self):
        '''清空脚印压力图'''
        self.clearFootImageButton.setChecked(False)
        try:
            os.remove("./footPrints/tempBig.png")
            os.remove("./footPrints/tempSmall.png")
            os.remove("./footPrints/voltageArr.txt")
        except:
            pass
        self.refreshBlankImageFromPNG()

    def saveFootDataToDataBase(self):
        '''保存脚印压力图像及电压向量到数据库
        Return:
            True: if 成功保存压力图的二进制数据 及 电压值的字符串
            False: if 保存失败
        '''
        self.saveFootImageButton.setChecked(False)
        try:
            imgRead = Image.open("./footPrints/tempSmall.png")
            imgByteDataToWrite = imgRead.tobytes()

            with open("./footPrints/voltageArr.txt",'r+') as f:
                voltageByteDataToWrite = f.readline()

            currentUserName = self.getCurrentUserName()  # 获得用户名+id
            if currentUserName == '':
                QMessageBox.warning(self, "警告", "没有用户!无法保存压力图数据!\n请先在数据库里建立用户!", QMessageBox.Ok)
                return False

            currentUserId = self.getCurrentUserId()  # 获得用户id
            self.saveFootImgToDataBase(currentUserId, imgByteDataToWrite) # 保存脚印压力图像到数据库
            self.saveFootVoltageToDataBase(currentUserId, voltageByteDataToWrite) # 保存脚印压力图像到数据库

            QMessageBox.information(self, "成功", "成功保存压力图数据", QMessageBox.Ok)
            return True
        except:
            QMessageBox.warning(self, "警告", "没有可以用来保存的压力图数据!", QMessageBox.Ok)
            return False

    def saveFootImgToDataBase(self, currentUserId, byteDataToWrite):
        '''保存脚印压力图像到数据库'''
        self.query.prepare(""" UPDATE footdata SET footImg=NULL WHERE id=(?) """)  # 清空压力图的二进制数据
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()

        self.query.prepare(""" UPDATE footdata SET footImg=(?) WHERE id=(?) """)  # 写入压力图的二进制数据
        self.query.addBindValue(QByteArray(byteDataToWrite))
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()

    def saveFootVoltageToDataBase(self, currentUserId, byteDataToWrite):
        '''保存脚印电压字符串到数据库'''
        self.query.prepare(""" UPDATE footdata SET footVoltage=NULL WHERE id=(?) """)  # 清空电压值的字符串
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()

        self.query.prepare(""" UPDATE footdata SET footVoltage=(?) WHERE id=(?) """)  # 写入电压值的字符串
        self.query.addBindValue(byteDataToWrite)
        self.query.addBindValue(QVariant(currentUserId))
        self.query.exec_()

    def setupPressureAnalysisDlg(self):
        """初始化压强分析的对话框"""
        self.pressureAnalysisDlg = pressureAnalysis.PressureAnalysisDlg()

    def showPressureAnalysisDlg(self):
        """显示压强分析的对话框"""
        self.showPressureAnalysisButton.setChecked(False)
        self.pressureAnalysisDlg.refreshAll()
        self.pressureAnalysisDlg.show()

    def refreshPressureAnalysisDlg(self):
        """刷新压强分析的对话框"""
        self.showPressureAnalysisButton.setChecked(False)
        self.pressureAnalysisDlg.refreshAll()

    def setupLayout(self):
        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(1)
        leftSideLayout.setSpacing(12)

        leftSideLayout.addWidget(self.showUserInputDlgButton)
        leftSideLayout.addWidget(self.showAdminDataBaseDlgButton)
        leftSideLayout.addWidget(self.selectUserLabel)
        leftSideLayout.addWidget(self.selectUserBox)

        self.serialPortObject.setupLayout(leftSideLayout)
        leftSideLayout.addWidget(self.clearFootImageButton)
        leftSideLayout.addWidget(self.saveFootImageButton)
        leftSideLayout.addWidget(self.loadFootImageButton)
        leftSideLayout.addWidget(self.showPressureAnalysisButton)

        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.scaleImageLabel)
        mainLayout.addWidget(self.footImageLabel)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)


"""主函数"""
window = MainWindow()
sys.exit(app.exec_())
