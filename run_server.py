import sqlite3
import sys
import sqlalchemy.sql.default_comparator
from pathlib import Path

from server.server import Server
import shared.log_config


def create_db():
    db_file = Path('server.db')
    if db_file.is_file():
        return
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()
    # Создание новых таблиц
    cursor.execute("""
      create table users (
        gid integer primary key autoincrement,
        login varchar(30) UNIQUE,
        password varchar(30),
        public_key varchar(1024)
      )
    """)

    cursor.execute("""
      create table messages (
        gid integer primary key autoincrement,
        u_from integer references users (gid),
        u_to integer references users (gid),
        time integer,
        message text
      )
    """)

    cursor.execute("""
      create table chat_messages (
        gid integer primary key autoincrement,
        u_from integer references users (gid),
        u_to integer references chats (gid),
        time integer,
        message text
      )
    """)

    cursor.execute("""
      create table chats (
        gid integer primary key autoincrement,
        name varchar(30) unique
      )
    """)

    cursor.execute("""
      create table users_chats (
        gid integer primary key autoincrement,
        user integer references users (gid),
        chat integer references chats (gid)
      )
    """)

    cursor.execute("""
      create table contacts (
        gid integer primary key autoincrement,
        user integer references users (gid),
        contact integer references users (gid)
      )
    """)

    connection.commit()


if __name__ == '__main__':
    args = sys.argv
    # Получаем ip и port из коммандной строки,
    # показывать ошибку, если ip не указан
    if len(args) not in (3, 5):
        print("Ошибка запуска сервера:")
        print("server.py -a addr [-p port]")
        sys.exit()

    create_db()

    addr = '127.0.0.1'
    port = 7777
    for i, s in enumerate(args):
        if s == '-a':
            addr = args[i+1]
        elif s == '-p':
            port = int(args[i+1])

    shared.log_config.init()
    server = Server(addr, port)
