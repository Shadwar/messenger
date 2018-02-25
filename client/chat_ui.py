# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client/chat.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_chat_window(object):
    def setupUi(self, chat_window):
        chat_window.setObjectName("chat_window")
        chat_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(chat_window)
        self.centralwidget.setObjectName("centralwidget")
        self.contacts = QtWidgets.QListView(self.centralwidget)
        self.contacts.setGeometry(QtCore.QRect(5, 10, 251, 501))
        self.contacts.setObjectName("contacts")
        self.chat = QtWidgets.QListView(self.centralwidget)
        self.chat.setGeometry(QtCore.QRect(260, 10, 531, 501))
        self.chat.setObjectName("chat")
        self.text_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_input.setGeometry(QtCore.QRect(260, 517, 441, 71))
        self.text_input.setObjectName("text_input")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(710, 520, 85, 71))
        self.send_button.setObjectName("send_button")
        self.add_contact_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_contact_button.setGeometry(QtCore.QRect(70, 550, 121, 31))
        self.add_contact_button.setObjectName("add_contact_button")
        self.add_contact_input = QtWidgets.QLineEdit(self.centralwidget)
        self.add_contact_input.setGeometry(QtCore.QRect(10, 520, 241, 27))
        self.add_contact_input.setObjectName("add_contact_input")
        chat_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(chat_window)
        QtCore.QMetaObject.connectSlotsByName(chat_window)

    def retranslateUi(self, chat_window):
        _translate = QtCore.QCoreApplication.translate
        chat_window.setWindowTitle(_translate("chat_window", "Chat"))
        self.send_button.setText(_translate("chat_window", "Send"))
        self.add_contact_button.setText(_translate("chat_window", "Добавить контакт"))

