# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client/login.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_login_window(object):
    def setupUi(self, login_window):
        login_window.setObjectName("login_window")
        login_window.resize(800, 601)
        login_window.setFocusPolicy(QtCore.Qt.TabFocus)
        self.loginWidget = QtWidgets.QWidget(login_window)
        self.loginWidget.setObjectName("loginWidget")
        self.connectButton = QtWidgets.QPushButton(self.loginWidget)
        self.connectButton.setGeometry(QtCore.QRect(340, 320, 111, 27))
        self.connectButton.setObjectName("connectButton")
        self.login_input = QtWidgets.QLineEdit(self.loginWidget)
        self.login_input.setGeometry(QtCore.QRect(300, 240, 200, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_input.sizePolicy().hasHeightForWidth())
        self.login_input.setSizePolicy(sizePolicy)
        self.login_input.setObjectName("login_input")
        self.password_input = QtWidgets.QLineEdit(self.loginWidget)
        self.password_input.setGeometry(QtCore.QRect(300, 280, 200, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_input.sizePolicy().hasHeightForWidth())
        self.password_input.setSizePolicy(sizePolicy)
        self.password_input.setObjectName("password_input")
        self.label_3 = QtWidgets.QLabel(self.loginWidget)
        self.label_3.setGeometry(QtCore.QRect(230, 285, 60, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.loginWidget)
        self.label_4.setGeometry(QtCore.QRect(230, 245, 60, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.label_4.setObjectName("label_4")
        login_window.setCentralWidget(self.loginWidget)

        self.retranslateUi(login_window)
        QtCore.QMetaObject.connectSlotsByName(login_window)

    def retranslateUi(self, login_window):
        _translate = QtCore.QCoreApplication.translate
        login_window.setWindowTitle(_translate("login_window", "Чат"))
        self.connectButton.setText(_translate("login_window", "Подключиться"))
        self.label_3.setText(_translate("login_window", "password"))
        self.label_4.setText(_translate("login_window", "login"))

