import abc

from server.chat import Chat
from shared.generate import get_hash
from shared.lib import login_required
from server.alchemy import *
from sqlalchemy import or_, and_

from shared.packets import ResponsePacket, MessagePacket, AlertPacket, ErrorPacket
from shared.packets.contact_packet import ContactPacket


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
        login = command['account_name']
        password = command['password']
        public_key = command['public_key']
        hashed_password = get_hash(login, password)

        session = sessionmaker(bind=self.db_engine)()
        db_user = session.query(SQLUser).filter_by(login=login).first()
        if db_user:
            if db_user.password == hashed_password:
                user.gid = db_user.gid
                user.login = login
                user.public_key = db_user.public_key
                # Загрузка всех чатов, в которых участвует пользователь
                db_user_chats = session.query(SQLUserChat).filter_by(user=user.gid).all()
                for uc in db_user_chats:
                    db_chat = session.query(SQLChat).filter_by(gid=uc.chat).first()
                    if db_chat:
                        if db_chat.name not in server.chats:
                            chat = Chat(title=db_chat.name)
                            chat.gid = db_chat.gid
                            server.chats[chat.title] = chat
                user.send_message(ResponsePacket(202, command['id']))
            else:
                user.send_message(ResponsePacket(402, command['id']))
        else:
            db_user = SQLUser(login=login, password=hashed_password, public_key=public_key)
            session.add(db_user)
            session.commit()
            user.gid = db_user.gid
            user.login = login
            user.public_key = db_user.public_key
            user.send_message(ResponsePacket(202, command['id']))
        session.close()


class QuitMessageHandler(MessageHandler):
    """ Выход пользователя """
    @login_required
    def run(self, server, user, command):
        # TODO: отправить статус оффлайн всем пользователям,
        # у которых данный пользователь в контакт-листе
        user.send_message(ResponsePacket(200, command['id']))


class PresenceMessageHandler(MessageHandler):
    """ Обработка сообщения о нахождении пользователя на сервере"""
    @login_required
    def run(self, server, user, command):
        user.send_message(ResponsePacket(200, command['id']))


class TextMessageHandler(MessageHandler):
    """ Обработка текстового сообщения """
    @login_required
    def run(self, server, user, command):
        sender = command['from']
        receiver = command['to']
        message = command['message']
        text_message = MessagePacket(sender, receiver, message)

        session = sessionmaker(bind=self.db_engine)()
        db_message = None

        if receiver.startswith('#'):
            if receiver in server.chats:
                server.chats[receiver].send_message(text_message)

            db_receiver = session.query(SQLChat).filter_by(name=receiver).first()
            if db_receiver:
                db_message = SQLChatMessage(
                        u_from=user.gid,
                        u_to=db_receiver.gid,
                        time=command['time'],
                        message=message)
        else:
            receiver_user = server.get_online_user_by_login(receiver)
            if receiver_user:
                receiver_user.send_message(text_message)

            db_receiver = session.query(SQLUser).filter_by(login=receiver).first()
            if db_receiver:
                db_message = SQLMessage(
                        u_from=user.gid,
                        u_to=db_receiver.gid,
                        time=command['time'],
                        message=message
                )
        if db_message:
            session.add(db_message)
            session.commit()

        session.close()
        user.send_message(ResponsePacket(202, command['id']))


class ChatJoinMessageHandler(MessageHandler):
    @login_required
    def run(self, server, user, command):
        """ Подключение к чату """
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.append(user)

        session = sessionmaker(bind=self.db_engine)()
        db_chat_user = SQLUserChat(user=user.gid, chat=chat.gid)
        session.add(db_chat_user)
        session.commit()
        session.close()
        user.send_message(ResponsePacket(202, command['id']))


class ChatLeaveMessageHandler(MessageHandler):
    @login_required
    def run(self, server, user, command):
        """ Отключение от чата """
        """ TODO: Отправить другим пользователям чата сообщение об отключении данного пользователя"""
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.remove(user)
        session = sessionmaker(bind=self.db_engine)()
        session.query(SQLUserChat).filter_by(chat=chat.gid).filter_by(user.user.gid).delete()
        session.close()
        user.send_message(ResponsePacket(202, command[id]))


class ChatCreateMessageHandler(MessageHandler):
    """ Создание нового чата, текущий пользователь сразу добавляется """
    @login_required
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        chat_name = command['room']
        db_chat = session.query(SQLChat).filter_by(name=chat_name).first()
        if db_chat:
            user.send_message(AlertPacket(400, command['id'], message='Чат с таким названием уже существует'))
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

            user.send_message(ResponsePacket(202, command['id']))
        session.close()


class GetContactsMessageHandler(MessageHandler):
    """ Отправить все контакты пользователю """
    @login_required
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        db_contacts = session.query(SQLContact).filter_by(user=user.gid).all()
        for db_c in db_contacts:
            contact = session.query(SQLUser).filter_by(gid=db_c.contact).first()
            contact_message = ContactPacket(contact.login, contact.public_key)
            user.send_message(contact_message)
        session.close()


class AddContactMessageHandler(MessageHandler):
    """ Добавить контакт пользователя """
    @login_required
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        contact = session.query(SQLUser).filter_by(login=command['contact']).first()
        if contact:
            db_contact = session.query(SQLContact).filter_by(user=user.gid).filter_by(contact=contact.gid).first()
            if db_contact:
                user.send_message(ErrorPacket(400, command['id'], message='Такой контакт уже существует'))
            else:
                db_contact = SQLContact(user=user.gid, contact=contact.gid)
                session.add(db_contact)
                other_contact = SQLContact(user=contact.gid, contact=user.gid)
                session.add(other_contact)
                session.commit()
                user.send_message(AlertPacket(200, command['id'], contact.public_key))
                other = server.get_online_user_by_login(contact.login)
                if other:
                    command = ContactPacket(user.login, user.public_key)
                    other.send_message(command)
        else:
            user.send_message(ErrorPacket(400, command['id'], message='Такой пользователь не найден.'))
        session.close()


class DelContactMessageHandler(MessageHandler):
    """ Удалить контакт пользователя """
    @login_required
    def run(self, server, user, command):
        session = sessionmaker(bind=self.db_engine)()
        db_other = session.query(SQLUser).filter_by(name=command['name']).first()
        session.query(SQLContact).filter(
                or_(
                        and_(user=user.gid, contact=db_other.gid),
                        and_(user=db_other.gid, contact=user.gid)
                )
        )
        user.send_message(ResponsePacket(202, command['id']))
        session.close()


class GetTextMessagesHandler(MessageHandler):
    """ Запрос на все сообщения для определенного контакта """
    @login_required
    def run(self, server, user, command):
        contact = command['contact']
        last_time = int(command['time'])

        session = sessionmaker(bind=self.db_engine)()
        if contact.startswith('#'):
            pass
        else:
            db_contact = session.query(SQLUser).filter_by(login=contact).first()
            if db_contact:
                db_messages = session.query(SQLMessage)\
                    .filter(SQLMessage.u_to == user.gid)\
                    .filter(SQLMessage.time >= last_time).all()
                for db_message in db_messages:
                    sender_gid = db_message.u_from
                    receiver_gid = db_message.u_to
                    db_sender = session.query(SQLUser).filter_by(gid=sender_gid).first()
                    db_receiver = session.query(SQLUser).filter_by(gid=receiver_gid).first()
                    user.send_message(MessagePacket(db_sender.login, db_receiver.login, db_message.message))
        session.close()
