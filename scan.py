# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import cv2
import utils


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.text = ''
        self.dir = ''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(474, 282)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_file = QtWidgets.QPushButton(self.centralwidget)
        self.button_file.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.button_file.setObjectName("button_file")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(100, 10, 75, 23))
        self.button_start.setObjectName("button_start")
        self.text_console = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_console.setGeometry(QtCore.QRect(40, 61, 361, 171))
        self.text_console.setObjectName("text_console")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 71, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.init_event()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_file.setText(_translate("MainWindow", "选择文件夹"))
        self.button_start.setText(_translate("MainWindow", "开始渲染"))
        self.label.setText(_translate("MainWindow", "控制台输出"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))

    def init_event(self):
        """
        初始化控件事件
        :return:
        """

        # 初始化选择文件的按钮
        self.button_file.clicked.connect(self.select_dic)

        # 开始批量处理目录下的图片
        self.button_start.clicked.connect(self.start_scann)

    def write_console(self, text):
        """
        想控制台输出语句
        :param text:
        :return:
        """
        self.text += text
        self.text += '\n'
        self.text_console.setText(self.text)

    def select_dic(self):
        """
        选择工作目录
        :return:
        """
        # 获取文件保存路径
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "F:/pycharm/ScanVision/img_test/")
        self.dir = dir_path
        self.write_console('选择文件夹：' + dir_path)

    class WorkThread(QThread):
        trigger = pyqtSignal()

        def __int__(self):
            super(Ui_MainWindow.WorkThread, self).__init__()

        def run(self):
            self.parent().scann(self)
            self.trigger.emit()

    def scann(self, thread):
        for path in os.listdir(self.dir):
            file_type = path.split('.')[-1]
            print(file_type)
            if file_type == 'jpg' or file_type == 'png':
                utils.scan(self.dir + '/' + path)
                self.text += ('成功渲染：' + self.dir + '/' + path)
                self.text += '\n'
                thread.trigger.emit()

    def start_scann(self):
        work_thread = self.WorkThread()
        work_thread.setParent(self)
        work_thread.trigger.connect(self.update_console)
        work_thread.start()

    def update_console(self):
        self.text_console.setText(self.text)
