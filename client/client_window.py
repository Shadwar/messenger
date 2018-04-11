import io

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from client.ui import LoginUI, ChatUI
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
        self.client.contacts = QStandardItemModel(self.ui.contacts)
        self.ui.add_contact_button.pressed.connect(self.add_contact_clicked)
        self.ui.contacts.doubleClicked.connect(self.item_contact_clicked)
        self.ui.send_button.pressed.connect(self.send_text_message)
        self.ui.user_image.pressed.connect(self.change_user_image)

        self.client.load_user_avatar(self.ui.user_image)
        # TODO: Запростить изображение пользователя с сервера

    def login_clicked(self):
        """ Обработчик нажатия кнопки логина """
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()
        self.client.authenticate(login, password)

    def add_contact_clicked(self):
        """ Обработчик нажатия кнопки добавления нового контакта """
        contact = self.ui.add_contact_input.text()
        message = AddContactMessage(contact, self.client.public_key)
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
        if sender == self.client.login:
            message_item.setBackground(QColor().fromRgb(255, 100, 255, 30))
        else:
            message_item.setBackground(QColor().fromRgb(100, 255, 255, 30))
        self.client.messages[chat].appendRow(message_item)
        #
        # if self.selected_contact == chat:
        #     self.ui.chat.setModel(self.client.messages[chat])

    def send_text_message(self):
        """ Отправление сообщения выбранному контакту """
        if self.selected_contact:
            text = self.ui.text_input.toPlainText()
            self.ui.text_input.setPlainText('')
            self.client.send_text_message(self.selected_contact, text)

    def item_contact_clicked(self, item):
        """ Обработчик выбора контакта в списке контактов """
        contact = item.data()
        self.selected_contact = contact
        self.ui.chat.setModel(self.client.messages[contact])

    def change_user_image(self):
        """ Изменение картинки пользователя """
        filename = QFileDialog.getOpenFileName(self, 'Выбрать аватарку', '/home')[0]
        if filename:
            file = open(filename, 'rb')
            image = Image.open(file)

            x_center = image.width // 2
            y_center = image.height // 2

            size = image.height if image.width > image.height else image.width
            x_left = x_center - size // 2
            x_right = x_center + size // 2
            y_top = y_center - size // 2
            y_bottom = y_center + size // 2
            image = image.crop((x_left, y_top, x_right, y_bottom))

            image = image.resize((50, 50), Image.NEAREST)
            pixmap = QPixmap.fromImage(ImageQt(image.convert('RGBA')))
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            self.ui.user_image.setIcon(icon)
            self.client.save_avatar(filename)

        # TODO: Отправить файл на сервер