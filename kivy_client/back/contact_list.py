from sqlalchemy.orm import sessionmaker

from kivy_client.back.db import SQLContact, SQLChat
from shared.packets import GetMessagesPacket


class ContactList(object):
    """ Класс, отвечающий за работу контакт-листа """
    def __init__(self, client):
        self.client = client
        self.db_engine = client.db_engine
        self.client.handlers['add_contact'] = self.add_contact_handler
        self.client.handlers['remove_contact'] = self.remove_contact_handler
        self.client.handlers['chat_create'] = self.chat_create_handler
        self.client.handlers['chat_join'] = self.chat_join_handler
        self.client.handlers['chat_contact'] = self.chat_contact_handler
        self.client.handlers['contact'] = self.contact_handler

    def add_contact_handler(self, command, response):
        contact = command['contact']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=self.client.login).filter(SQLContact.contact.ilike(contact)).first()
        if db_contact:
            pass

        if response and response['response'] == 200:
            login = response['alert_0']
            public_key = response['alert_1']
            db_contact = SQLContact(login=self.client.login, contact=contact, public_key=public_key)
            session.add(db_contact)
            session.commit()
            # client.signals['add_contact'].emit(login)

        session.close()

    def remove_contact_handler(self, command, response):
        pass

    def chat_create_handler(self, command, response):
        chat_name = command['room']
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter_by(login=self.client.login).filter(SQLChat.name.ilike(chat_name)).first()
        if db_chat:
            pass

        if response and response['response'] == 202:
            name = response['alert']
            db_chat = SQLChat(login=self.client.login, name=name)
            session.add(db_chat)
            session.commit()
            # client.signals['add_contact'].emit(name)

        session.close()

    def chat_join_handler(self, command, response):
        chat_name = command['room']
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter_by(login=self.client.login).filter(SQLChat.name.ilike(chat_name)).first()
        if db_chat:
            pass

        if response and response['response'] == 202:
            name = response['alert']
            db_chat = SQLChat(login=self.client.login, name=name)
            session.add(db_chat)
            session.commit()
            # client.signals['add_contact'].emit(name)

        session.close()

    def chat_contact_handler(self, command, response):
        chat_name = command['room']
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter_by(login=self.client.login).filter_by(name=chat_name).first()
        if db_chat:
            session.close()
            return
        db_chat = SQLChat(login=self.client.login, name=chat_name)
        session.add(db_chat)
        session.commit()
        get_messages = GetMessagesPacket(chat_name)
        self.client.send_message(get_messages)
        # client.signals['add_contact'].emit(chat_name)
        session.close()

    def contact_handler(self, command, response):
        contact = command['contact']
        public_key = command['public_key']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=self.client.login).filter_by(contact=contact).first()
        if db_contact:
            session.close()
            return
        db_contact = SQLContact(login=self.client.login, contact=contact, public_key=public_key)
        session.add(db_contact)
        session.commit()
        get_messages = GetMessagesPacket(db_contact.contact)
        self.client.send_message(get_messages)
        # client.signals['add_contact'].emit(contact)
        session.close()
