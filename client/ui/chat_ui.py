# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client/chat.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_chat_window(object):
    def setupUi(self, chat_window):
        path = os.path.dirname(os.path.abspath(__file__))
        chat_window.setObjectName("chat_window")
        chat_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(chat_window)
        self.centralwidget.setStyleSheet("background-color: rgb(76, 135, 202);")
        self.centralwidget.setObjectName("centralwidget")
        self.contacts = QtWidgets.QListView(self.centralwidget)
        self.contacts.setGeometry(QtCore.QRect(10, 70, 280, 480))
        self.contacts.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.contacts.setObjectName("contacts")
        self.chat = QtWidgets.QListView(self.centralwidget)
        self.chat.setGeometry(QtCore.QRect(300, 10, 491, 501))
        self.chat.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.chat.setObjectName("chat")
        self.text_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_input.setGeometry(QtCore.QRect(300, 517, 401, 71))
        self.text_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.text_input.setObjectName("text_input")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(710, 520, 85, 71))
        self.send_button.setStyleSheet("background-color: rgba(50, 127, 198, 100);font: 19pt;")
        self.send_button.setObjectName("send_button")
        self.add_contact_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_contact_button.setGeometry(QtCore.QRect(170, 560, 121, 31))
        self.add_contact_button.setStyleSheet("background-color: rgba(50, 127, 198, 100);")
        self.add_contact_button.setObjectName("add_contact_button")
        self.add_contact_input = QtWidgets.QLineEdit(self.centralwidget)
        self.add_contact_input.setGeometry(QtCore.QRect(10, 560, 151, 31))
        self.add_contact_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.add_contact_input.setObjectName("add_contact_input")
        self.user_name = QtWidgets.QLabel(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(70, 10, 221, 51))
        self.user_name.setStyleSheet("font: 19pt;")
        self.user_name.setObjectName("user_name")
        self.user_image = QtWidgets.QPushButton(self.centralwidget)
        self.user_image.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.user_image.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(path, "assets/no_user_avatar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.user_image.setIcon(icon)
        self.user_image.setIconSize(QtCore.QSize(50, 50))
        self.user_image.setFlat(True)
        self.user_image.setObjectName("user_image")
        chat_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(chat_window)
        QtCore.QMetaObject.connectSlotsByName(chat_window)

    def retranslateUi(self, chat_window):
        _translate = QtCore.QCoreApplication.translate
        chat_window.setWindowTitle(_translate("chat_window", "Chat"))
        self.send_button.setText(_translate("chat_window", "Send"))
        self.add_contact_button.setText(_translate("chat_window", "Добавить контакт"))
        self.user_name.setText(_translate("chat_window", "UserName"))

