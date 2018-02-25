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

        self.ui = None
        self.open_login_window()

    def init_signals(self):
        self.client.signals['login_ok'].connect(self.open_chat_window)

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

    def login_clicked(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        message = AuthenticateMessage(login, password)
        self.client.send_message(message)

    def add_contact_clicked(self):
        contact = self.ui.add_contact_input.text()
        message = AddContactMessage(contact)
        self.client.send_message(message)
