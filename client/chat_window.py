from PyQt5.QtWidgets import QMainWindow
from client.chat_ui import Ui_chat_window as ChatUI


class ChatWindow(QMainWindow):
    """ Главное окно с чатом и списком контактов """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ChatUI()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
