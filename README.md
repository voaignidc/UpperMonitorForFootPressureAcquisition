# UpperMonitorForFootPressureAcquisiton 
## Introduction 
* An upper monitor code by py3.6 and pyqt5 
* Acquire information & display graphs from pressure sensor, through serial port
* Record the information of each user with sqlite database
* Pressure analysis

## OS
* Windows 10 x64

## Requirements
* python 3.6
* PyQt5
* Pillow
* pyserial
* numpy
* matplotlib

## How to run
* main.py

## How to build
* pyinstaller.exe -F -y main.spec
* pyinstaller.exe --paths D:\Programfiles\Python36\Lib\site-packages\PyInstaller\loader\rthooks -F -y main.spec

## Screenshot
![Screenshot](https://github.com/voaignidc/UpperMonitorForFootPressureAcquisition/blob/master/screenshot.png)



# 足部压力采集上位机
## 简介
* 用py3.6以及pyqt5写的上位机
* 通过串口, 可以完成对压力传感器信息的采集与图形化显示
* 附带sqlite数据库, 可以记录各个用户的信息
* 压力分析

## 支持的系统
* Windows 10 x64


## 需求
* python 3.6
* PyQt5
* Pillow
* pyserial
* numpy
* matplotlib

## 运行方法
* main.py

## 打包方法
* pyinstaller.exe -F -y main.spec
* pyinstaller.exe --paths D:\Programfiles\Python36\Lib\site-packages\PyInstaller\loader\rthooks -F -y main.spec

## 截图
![Screenshot](https://github.com/voaignidc/UpperMonitorForFootPressureAcquisition/blob/master/screenshot.png)