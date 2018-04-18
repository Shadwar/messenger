import sqlite3
import sqlalchemy.sql.default_comparator
import sys
from pathlib import Path
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


def create_db():
    db_file = Path('client.db')
    if db_file.is_file():
        return
    connection = sqlite3.connect('client.db')
    cursor = connection.cursor()

    cursor.execute("""
      create table users (
        gid integer primary key autoincrement,
        login varchar(30),
        password varchar(64),
        private_key varchar(1024),
        public_key varchar(1024),
        avatar blob
      )
    """)

    cursor.execute("""
      create table messages (
        gid integer primary key autoincrement,
        user varchar(30),
        u_from varchar(30),
        u_to varchar(30),
        time integer,
        message text
      )
    """)

    cursor.execute("""
      create table contacts (
        gid integer primary key autoincrement,
        login varchar(30),
        contact varchar(30),
        public_key varchar(1024)
      )
    """)

    cursor.execute("""
      create table chats (
        gid integer primary key autoincrement,
        login varchar(30),
        name varchar(30)
      )
    """)

    cursor.execute("""
      create table chat_messages (
        gid integer primary key autoincrement,
        login varchar(30),
        name varchar(30),
        contact varchar(30),
        time integer,
        message text
      )
    """)
    connection.commit()


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

    create_db()

    app = QApplication(sys.argv)
    client = Client(addr, port)
    thr = ClientThread(client)

    wnd = ClientWindow(client)
    wnd.show()
    wnd.init_signals()

    thr.start()

    sys.exit(app.exec_())
