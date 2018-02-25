from PyQt5.QtWidgets import QMainWindow
from client.login_ui import Ui_login_window as LoginUI


class LoginWindow(QMainWindow):
    """ Окно логина """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
