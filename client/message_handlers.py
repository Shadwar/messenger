import abc

from shared.responses import *
from shared.messages import *
from client.alchemy import *


class MessageHandler(object):
    """ Обработчик команд """
    def __init__(self):
        self.db_engine = create_engine('sqlite:///client.db')

    @abc.abstractmethod
    def run(self, client, command, response):
        """ Обработка команды и возврат значения """
        pass


class AuthenticateHandler(MessageHandler):
    """ Аутентификация на сервере """
    def run(self, client, command, response):
        if response and response['response'] == 202:
            client.login = command['user']['account_name']
            # Загрузить все данные
            session = sessionmaker(bind=self.db_engine)()
            db_contacts = session.query(SQLContact).filter_by(login=client.login).all()
            for db_contact in db_contacts:
                client.contacts.append(db_contact.contact)

            db_messages = session.query(SQLMessage).filter_by(user=client.login).all()
            for db_message in db_messages:
                chat = db_message.u_from if db_message.u_from == client.login else db_message.u_to
                if chat not in client.messages:
                    client.messages[chat] = []
                client.messages[chat].append(db_message)
            client.signals['login_ok'].emit()
            get_contacts = GetContactsMessage()
            client.send_message(get_contacts)
            for db_contact in db_contacts:
                get_messages = GetTextMessages(db_contact.contact)
                client.send_message(get_messages)
        else:
            client.signals['login_error'].emit()


class AddContactHandler(MessageHandler):
    """ Обработчик ответа добавленного контакта """
    def run(self, client, command, response):
        print("AddContactHandler", command)
        if response and response['response'] == 200:
            contact = command['contact']
            session = sessionmaker(bind=self.db_engine)()
            db_contact = SQLContact(login=client.login, contact=contact)
            session.add(db_contact)
            session.commit()
            client.contacts.append(contact)


class ContactHandler(MessageHandler):
    """ Обработчик полученных контактов """
    def run(self, client, command, response):
        print("ContactHandler", command)
        contact = command['contact']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=client.login).filter_by(contact=contact).first()
        if db_contact:
            pass
        db_contact = SQLContact(login=client.login, contact=contact)
        session.add(db_contact)
        session.commit()
        print(db_contact)


class ProbeHandler(MessageHandler):
    def run(self, client, command, response):
        presence = PresenceMessage(client.login, 'online')
        client.send_message(presence)
