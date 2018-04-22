import sqlite3
import sys
from kivy import Config
from pathlib import Path

from client.client import Client
from client.client_app import ClientApp


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

    client = Client(addr, port)

    Config.set('graphics', 'width', 1024)
    Config.set('graphics', 'height', 800)
    Config.write()

    ClientApp().run()
