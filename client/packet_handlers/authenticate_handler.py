from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from client.db import SQLContact, SQLMessage, SQLChat, SQLChatMessage
from client.packet_handlers import MessageHandler
from shared.packets import GetMessagesPacket, GetContactsPacket


class AuthenticateHandler(MessageHandler):
    """ Аутентификация на сервере """
    def run(self, client, command, response):
        if response and response['response'] == 202:
            client.signals['login_ok'].emit()
            client.login = command['account_name']
            # Загрузить все данные
            session = sessionmaker(bind=self.db_engine)()
            db_contacts = session.query(SQLContact).filter_by(login=client.login).all()
            for db_contact in db_contacts:
                client.signals['add_contact'].emit(db_contact.contact)

            get_contacts = GetContactsPacket()
            client.send_message(get_contacts)

            db_messages = session.query(SQLMessage).filter_by(user=client.login).all()
            for db_message in db_messages:
                chat = db_message.u_from if db_message.u_from != client.login else db_message.u_to
                client.signals['text_message'].emit(chat, db_message.u_from, db_message.message)

            for db_contact in db_contacts:
                get_messages = GetMessagesPacket(db_contact.contact)
                db_last_message = session.query(SQLMessage).filter_by(user=client.login).order_by('-gid').first()
                if db_last_message:
                    get_messages.data['time'] = db_last_message.time
                else:
                    get_messages.data['time'] = 0

                client.send_message(get_messages)

            db_chats = session.query(SQLChat).filter_by(login=client.login).all()
            for db_chat in db_chats:
                client.signals['add_contact'].emit(db_chat.name)
                db_messages = session.query(SQLChatMessage).filter(and_(SQLChatMessage.login == client.login, SQLChatMessage.name == db_chat.name)).all()
                for db_message in db_messages:
                    client.signals['text_message'].emit(db_message.name, db_message.contact, db_message.message)

                db_last_message = session.query(SQLChatMessage).filter(and_(SQLChatMessage.login == client.login, SQLChatMessage.name == db_chat.name)).order_by('-gid').first()
                get_messages = GetMessagesPacket(db_chat.name)
                if db_last_message:
                    get_messages.data['time'] = db_last_message.time
                else:
                    get_messages.data['time'] = 0

                client.send_message(get_messages)

            session.close()
        else:
            client.signals['login_error'].emit()
