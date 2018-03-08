from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal

from client.login_ui import Ui_login_window as LoginUI
from client.chat_ui import Ui_chat_window as ChatUI
from shared.messages import *


class ClientWindow(QMainWindow):
    """ Окно клиента """
    def __init__(self, client, parent=None):
        super().__init__(parent)
        self.client = client

        self.selected_contact = None
        self.ui = None
        self.open_login_window()

    def init_signals(self):
        self.client.signals['login_ok'].connect(self.open_chat_window)
        self.client.signals['add_contact'].connect(self.add_contact_signal)
        self.client.signals['text_message'].connect(self.add_text_message_signal)

    def open_login_window(self):
        """ Создать окно с вводом пароля """
        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.connectButton.pressed.connect(self.login_clicked)

    def open_chat_window(self):
        """ Создать окно с чатом """
        self.ui = ChatUI()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.add_contact_button.pressed.connect(self.add_contact_clicked)
        self.client.contacts = QStandardItemModel(self.ui.contacts)
        self.ui.contacts.doubleClicked.connect(self.item_contact_clicked)
        self.ui.send_button.pressed.connect(self.send_text_message)

    def login_clicked(self):
        """ Обработчик нажатия кнопки логина """
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        message = AuthenticateMessage(login, password)
        self.client.send_message(message)

    def add_contact_clicked(self):
        """ Обработчик нажатия кнопки добавления нового контакта """
        contact = self.ui.add_contact_input.text()
        message = AddContactMessage(contact)
        self.client.send_message(message)

    def add_contact_signal(self, contact):
        """ Сигнал по добавлению нового контакта,
            добавляет контакт в отображаемый список контактов
        """
        if contact not in self.client.messages:
            self.client.messages[contact] = QStandardItemModel(self.ui.chat)

        contact = QStandardItem(contact)
        contact.setCheckable(False)
        contact.setEditable(False)
        self.client.contacts.appendRow(contact)
        self.ui.contacts.setModel(self.client.contacts)

    def add_text_message_signal(self, chat, sender, message):
        """ Сигнал по добавлению нового сообщения """
        if chat not in self.client.messages:
            self.client.messages[chat] = QStandardItemModel(self.ui.chat)

        message_item = QStandardItem(sender + ': ' + message)
        message_item.setCheckable(False)
        message_item.setEditable(False)
        self.client.messages[chat].appendRow(message_item)
        #
        # if self.selected_contact == chat:
        #     self.ui.chat.setModel(self.client.messages[chat])

    def send_text_message(self):
        """ Отправление сообщения выбранному контакту """
        if self.selected_contact:
            text = self.ui.text_input.toPlainText()
            message = TextMessage(self.client.login, self.selected_contact, text)
            self.client.send_message(message)

    def item_contact_clicked(self, item):
        """ Обработчик выбора контакта в списке контактов """
        contact = item.data()
        self.selected_contact = contact
        self.ui.chat.setModel(self.client.messages[contact])
