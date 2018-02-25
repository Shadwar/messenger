import sys
from PyQt5.QtWidgets import QApplication
from client.login_window import LoginWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = LoginWindow()
    wnd.show()

    exit(app.exec_())
