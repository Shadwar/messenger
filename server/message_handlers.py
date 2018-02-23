import abc

from server.chat import Chat
from shared.responses import *
from shared.messages import *
from server.alchemy import *


class MessageHandler(object):
    """ Обработчик команд """
    def __init__(self):
        self.db_engine = create_engine('sqlite:///server.db')

    @abc.abstractmethod
    def run(self, server, user, command):
        """ Обработка команды и возврат значения """
        pass


class AuthenticateMessageHandler(MessageHandler):
    """ Аутентификация пользователя """
    def run(self, server, user, command):
        login = command['user']['account_name']
        password = command['user']['password']

        session = sessionmaker(bind=self.db_engine)()
        db_user = session.query(SQLUser).filter_by(login=login).first()
        if db_user:
            if db_user.password == password:
                user.gid = db_user.gid
                # Загрузка всех чатов, в которых участвует пользователь
                db_user_chats = session.query(SQLUserChat).filter_by(user=user.gid).all()
                for uc in db_user_chats:
                    db_chat = session.query(SQLChat).filter_by(gid=uc.chat).first()
                    if db_chat:
                        if db_chat.name not in server.chats:
                            chat = Chat(title=db_chat.name)
                            chat.gid = db_chat.gid
                            server.chats[chat.title] = chat
                user.send_message(Response(202))
            else:
                user.send_message(Response(402))
        else:
            db_user = SQLUser(login=login, password=password)
            session.add(db_user)
            session.commit()
            user.gid = db_user.gid
            user.send_message(Response(202))


class QuitMessageHandler(MessageHandler):
    """ Выход пользователя """
    def run(self, server, user, command):
        # TODO: отправить статус оффлайн всем пользователям,
        # у которых данный пользователь в контакт-листе
        user.send_message(Response(200))


class PresenceMessageHandler(MessageHandler):
    """ Обработка сообщения о нахождении пользователя на сервере"""
    def run(self, server, user, command):
        user.send_message(Response(200))


class TextMessageHandler(MessageHandler):
    """ Обработка текстового сообщения """
    def run(self, server, user, command):
        sender = command['from']
        receiver = command['to']
        message = command['message']
        text_message = TextMessage(sender, receiver, message)

        session = sessionmaker(bind=self.db_engine)()
        db_message = None

        if receiver.startswith('#'):
            server.chats[receiver].send_message(text_message)
            db_receiver = session.query(SQLChat).filter_by(name=receiver).first()
            if db_receiver:
                db_message = SQLChatMessage(
                        u_from=user.gid,
                        u_to=db_receiver.gid,
                        message=message)
        else:
            server.users[receiver].send_message(text_message)
            db_receiver = session.query(SQLUser).filter_by(login=receiver).first()
            if db_receiver:
                db_message = SQLMessage(
                        u_from=user.gid,
                        u_to=receiver.gid,
                        message=message
                )
        if db_message:
            session.add(db_message)
            session.commit()

        user.send_message(Response(202))


class ChatJoinMessageHandler(MessageHandler):
    def run(self, server, user, command):
        """ Подключение к чату """
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.append(user)

        session = sessionmaker(bind=self.db_engine)()
        db_chat_user = SQLUserChat(user=user.gid, chat=chat.gid)
        session.add(db_chat_user)
        session.commit()
        user.send_message(Response(202))


class ChatLeaveMessageHandler(MessageHandler):
    def run(self, server, user, command):
        """ Отключение от чата """
        """ TODO: Отправить другим пользователям чата сообщение об отключении данного пользователя"""
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.remove(user)
        session = sessionmaker(bind=self.db_engine)()
        session.query(SQLUserChat).filter_by(chat=chat.gid).filter_by(user.user.gid).delete()
        user.send_message(Response(202))


class ChatCreateMessageHandler(MessageHandler):
    """ Создание нового чата, текущий пользователь сразу добавляется """
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        chat_name = command['room']
        db_chat = session.query(SQLChat).filter_by(name=chat_name).first()
        if db_chat:
            user.send_message(AlertResponse(400, message='Чат с таким названием уже существует'))
        else:
            chat = Chat(chat_name)
            chat.users.append(user)
            server.chats[chat_name] = chat

            db_chat = SQLChat(name=chat_name)
            session.add(db_chat)
            session.commit()
            chat.gid = db_chat.gid

            db_user_chat = SQLUserChat(user=user.gid, chat=db_chat.gid)
            session.add(db_user_chat)
            session.commit()

            user.send_message(Response(202))


class GetContactsMessageHandler(MessageHandler):
    """ Отправить все контакты пользователю """
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        db_contacts = session.query(SQLContact).filter_by(user=user.gid).all()
        for db_c in db_contacts:
            contact = session.query(SQLUser).filter_by(gid=db_c.contact).first()
            contact_message = ContactMessage(contact.login)
            user.send_message(contact_message)


class AddContactMessageHandler(MessageHandler):
    """ Добавить контакт пользователя """
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        contact = session.query(SQLUser).filter_by(name=command['name']).first()
        if contact:
            db_contact = SQLContact(user=user.gid, contact=contact.gid)
            session.add(db_contact)
            session.commit()
            user.send_message(Response(200))
        else:
            user.send_message(ErrorResponse(400, message='Такой пользователь не найден.'))


class DelContactMessageHandler(MessageHandler):
    """ Удалить контакт пользователя """
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        db_other = session.query(SQLUser).filter_by(name=command['name']).first()
        session.query(SQLContact).filter_by(contact=db_other.gid).delete()
        user.send_message(Response(202))
