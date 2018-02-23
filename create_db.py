import sqlite3


def server_db():
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()

    # Удаление старых таблиц
    cursor.execute('drop table if exists users')
    cursor.execute('drop table if exists messages')
    cursor.execute('drop table if exists chats')
    cursor.execute('drop table if exists chat_messages')
    cursor.execute('drop table if exists users_chats')
    cursor.execute('drop table if exists contacts')

    # Создание новых таблиц
    cursor.execute("""
      create table users (
        gid integer primary key autoincrement,
        login varchar(30) UNIQUE,
        password varchar(30)
      )
    """)

    cursor.execute("""
      create table messages (
        gid integer primary key autoincrement,
        u_from integer references users (gid),
        u_to integer references users (gid),
        message text
      )
    """)

    cursor.execute("""
      create table chat_messages (
        gid integer primary key autoincrement,
        u_from integer references users (gid),
        u_to integer references chats (gid),
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


def user_db():
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor()

    # Удаление старых таблиц
    cursor.execute('drop table if exists contacts')
    cursor.execute('drop table if exists chats')
    cursor.execute('drop table if exists users_chats')
    cursor.execute('drop table if exists messages')

    cursor.execute("""
      create table messages (
        gid integer primary key autoincrement,
        u_from integer references users (gid),
        u_to integer references users (gid),
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
        user integer references users (gid),
        chat integer references chats (gid)
      )
    """)

    cursor.execute("""
      create table contacts (
        user integer references users (gid),
        contact integer references users (gid)
      )
    """)


def main():
    server_db()


if __name__ == '__main__':
    main()
