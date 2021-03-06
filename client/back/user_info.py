import io

import rsa
from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from client.back.db import SQLUser, SQLContact, SQLMessage, SQLChat, SQLChatMessage
from shared.generate import get_hash
from shared.packets import GetContactsPacket, GetMessagesPacket, AuthenticatePacket, PresencePacket


class UserInfo(object):
    """ Класс, отвечающий за работу информации о пользователе """
    def __init__(self, client):
        """
        :param client: Client
        """
        self.client = client
        self.db_engine = client.db_engine
        self.client.handlers['load_avatar'] = self.load_avatar_handler
        self.client.handlers['save_avatar'] = self.save_avatar_handler
        self.client.handlers['authenticate'] = self.send_authentication_handler
        self.client.handlers['authenticate_user'] = self.client_authentication_handler
        self.client.handlers['user_status'] = self.user_status_handler

    def load_avatar_handler(self, command, response):
        session = sessionmaker(bind=self.db_engine)()
        db_user = session.query(SQLUser).filter_by(login=self.client.login).first()
        if db_user:
            avatar_data = db_user.avatar

            if avatar_data:
                image = Image.open(io.BytesIO(avatar_data))
                pixmap = QPixmap.fromImage(ImageQt(image.convert('RGBA')))
                icon = QIcon()
                icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
                command['container'].setIcon(icon)
        session.close()

    def save_avatar_handler(self, command, response):
        session = sessionmaker(bind=self.db_engine)()
        filename = command['filename']
        avatar_data = open(filename, 'rb').read()
        db_user = session.query(SQLUser).filter_by(login=self.client.login).first()
        if db_user:
            db_user.avatar = avatar_data
            session.add(db_user)
            session.commit()
        session.close()

    def send_authentication_handler(self, command, response):
        if response and response['response'] == 202:
            self.client.login = command['account_name']
            # Загрузить все данные
            session = sessionmaker(bind=self.db_engine)()

            # Загрузка контактов из локальной базы
            db_contacts = session.query(SQLContact).filter_by(login=self.client.login).all()
            for db_contact in db_contacts:
                self.client.contacts.append(db_contact.contact)

            # Загрузка сообщений из локальной базы
            db_messages = session.query(SQLMessage).filter_by(user=self.client.login).all()
            for db_message in db_messages:
                chat = db_message.u_from if db_message.u_from != self.client.login else db_message.u_to
                self.client.messages[chat].append({
                    'u_from': db_message.u_from,
                    'message': db_message.message,
                    'time': db_message.time
                })

            # Запрос сообщений с сервера
            for db_contact in db_contacts:
                get_messages = GetMessagesPacket(db_contact.contact)
                db_last_message = session.query(SQLMessage).filter_by(user=self.client.login).order_by('-gid').first()
                if db_last_message:
                    get_messages.data['time'] = db_last_message.time
                else:
                    get_messages.data['time'] = 0
                self.client.send_message(get_messages)

            # Загрузка чатов из локальной базы
            db_chats = session.query(SQLChat).filter_by(login=self.client.login).all()
            for db_chat in db_chats:
                self.client.contacts.append(db_chat.name)

            # Загрузка сообщений чатов из локальной базы
            db_messages = session.query(SQLChatMessage).filter_by(login=self.client.login).all()
            for db_message in db_messages:
                self.client.messages[db_message.name].append({'u_from': db_message.contact, 'message': db_message.message, 'time': db_message.time})

            # Загрузка сообщений с сервера
            for db_chat in db_chats:
                get_messages = GetMessagesPacket(db_chat.name)
                db_last_message = session.query(SQLChatMessage).filter(and_(SQLChatMessage.login == self.client.login, SQLChatMessage.name == db_chat.name)).order_by('-gid').first()
                if db_last_message:
                    get_messages.data['time'] = db_last_message.time
                else:
                    get_messages.data['time'] = 0
                self.client.send_message(get_messages)

            # Запрос контактов с сервера
            get_contacts = GetContactsPacket()
            self.client.send_message(get_contacts)

            session.close()

            self.client.send_event({'action': 'ui_login_ok'})
        else:
            self.client.send_event({'action': 'ui_login_error'})

    def client_authentication_handler(self, command, response):
        session = sessionmaker(bind=self.db_engine)()
        login = command['login']
        password = command['password']
        hashed_password = get_hash(login, password)

        db_user = session.query(SQLUser).filter_by(login=login).filter_by(password=hashed_password).first()
        if db_user:
            pass
        else:
            (public_key, private_key) = rsa.newkeys(512)
            db_user = SQLUser(
                    login=login,
                    password=hashed_password,
                    public_key=public_key.save_pkcs1('DER').hex(),
                    private_key=private_key.save_pkcs1('DER').hex()
            )
            session.add(db_user)
            session.commit()

        client = command['client']
        client.private_key = db_user.private_key
        client.public_key = db_user.public_key

        session.close()
        message = AuthenticatePacket(login, password, db_user.public_key)
        client.send_message(message)

    def user_status_handler(self, command, response):
        presence = PresencePacket(self.client.login, 'online')
        self.client.send_message(presence)
