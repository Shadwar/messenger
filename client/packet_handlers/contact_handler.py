from sqlalchemy.orm import sessionmaker

from client.db import SQLContact
from client.packet_handlers import MessageHandler
from shared.packets import GetMessagesPacket


class ContactHandler(MessageHandler):
    """ Обработчик полученных контактов """
    def run(self, client, command, response):
        contact = command['contact']
        public_key = command['public_key']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=client.login).filter_by(contact=contact).first()
        if db_contact:
            session.close()
            return
        db_contact = SQLContact(login=client.login, contact=contact, public_key=public_key)
        session.add(db_contact)
        session.commit()
        get_messages = GetMessagesPacket(db_contact.contact)
        client.send_message(get_messages)
        client.signals['add_contact'].emit(contact)
        session.close()
