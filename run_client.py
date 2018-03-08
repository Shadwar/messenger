import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from client.client import Client
from client.client_window import ClientWindow


class ClientThread(QThread):
    login_ok_signal = pyqtSignal()
    login_error_signal = pyqtSignal()
    add_contact = pyqtSignal(str)
    text_message = pyqtSignal(str, str, str)

    def __init__(self, cl):
        QThread.__init__(self)
        self.client = cl
        self.client.signals['login_ok'] = self.login_ok_signal
        self.client.signals['login_error'] = self.login_error_signal
        self.client.signals['add_contact'] = self.add_contact
        self.client.signals['text_message'] = self.text_message


    def __del__(self):
        self.wait()

    def run(self):
        self.client.run()


if __name__ == '__main__':
    args = sys.argv

    if len(args) not in (2, 3):
        print("Ошибка запуска клиента:")
        print("client.py addr [port]")
        sys.exit()
    addr = args[1]

    try:
        port = int(args[2])
    except Exception:
        port = 7777

    app = QApplication(sys.argv)
    client = Client(addr, port)
    thr = ClientThread(client)

    wnd = ClientWindow(client)
    wnd.show()
    wnd.init_signals()

    thr.start()

    print(dir(app))

    exit(app.exec_())
