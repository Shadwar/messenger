from sqlalchemy.orm import sessionmaker

from client.db import SQLContact
from client.packet_handlers import MessageHandler


class AddContactHandler(MessageHandler):
    """ Обработчик ответа добавленного контакта """
    def run(self, client, command, response):
        contact = command['contact']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=client.login).filter(SQLContact.contact.ilike(contact)).first()
        if db_contact:
            pass

        if response and response['response'] == 200:
            login = response['alert_0']
            public_key = response['alert_1']
            db_contact = SQLContact(login=client.login, contact=contact, public_key=public_key)
            session.add(db_contact)
            session.commit()
            client.signals['add_contact'].emit(login)

        session.close()