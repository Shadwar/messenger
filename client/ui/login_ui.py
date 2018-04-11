# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client/login.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_login_window(object):
    def setupUi(self, login_window):
        path = os.path.dirname(os.path.abspath(__file__))
        login_window.setObjectName("login_window")
        login_window.resize(800, 601)
        login_window.setFocusPolicy(QtCore.Qt.TabFocus)
        self.loginWidget = QtWidgets.QWidget(login_window)
        self.loginWidget.setStyleSheet("background-color: rgb(76, 135, 202);")
        self.loginWidget.setObjectName("loginWidget")
        self.connectButton = QtWidgets.QPushButton(self.loginWidget)
        self.connectButton.setGeometry(QtCore.QRect(290, 350, 231, 51))
        self.connectButton.setStyleSheet("font: 19pt;background-color: rgba(50, 127, 198, 100);")
        self.connectButton.setObjectName("connectButton")
        self.login_input = QtWidgets.QLineEdit(self.loginWidget)
        self.login_input.setGeometry(QtCore.QRect(370, 245, 211, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_input.sizePolicy().hasHeightForWidth())
        self.login_input.setSizePolicy(sizePolicy)
        self.login_input.setStyleSheet("font: 19pt;background-color: rgb(255, 255, 255);")
        self.login_input.setObjectName("login_input")
        self.password_input = QtWidgets.QLineEdit(self.loginWidget)
        self.password_input.setGeometry(QtCore.QRect(370, 295, 211, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_input.sizePolicy().hasHeightForWidth())
        self.password_input.setSizePolicy(sizePolicy)
        self.password_input.setStyleSheet("font: 19pt;background-color: rgb(255, 255, 255);")
        self.password_input.setObjectName("password_input")
        self.password_label = QtWidgets.QLabel(self.loginWidget)
        self.password_label.setGeometry(QtCore.QRect(230, 300, 131, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setStyleSheet("font: 19pt;")
        self.password_label.setObjectName("password_label")
        self.login_label = QtWidgets.QLabel(self.loginWidget)
        self.login_label.setGeometry(QtCore.QRect(230, 250, 131, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_label.sizePolicy().hasHeightForWidth())
        self.login_label.setSizePolicy(sizePolicy)
        self.login_label.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.login_label.setStyleSheet("font: 19pt;")
        self.login_label.setObjectName("login_label")
        self.messenger_logo = QtWidgets.QLabel(self.loginWidget)
        self.messenger_logo.setGeometry(QtCore.QRect(230, 30, 341, 201))
        self.messenger_logo.setText("")
        self.messenger_logo.setPixmap(QtGui.QPixmap(os.path.join(path, "assets/messenger_logo.png")))
        self.messenger_logo.setObjectName("messenger_logo")
        self.messenger_logo.raise_()
        self.connectButton.raise_()
        self.login_input.raise_()
        self.password_input.raise_()
        self.password_label.raise_()
        self.login_label.raise_()
        login_window.setCentralWidget(self.loginWidget)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Чат"))
        self.connectButton.setText(_translate("login_window", "Подключиться"))
        self.password_label.setText(_translate("login_window", "password"))
        self.login_label.setText(_translate("login_window", "login"))

