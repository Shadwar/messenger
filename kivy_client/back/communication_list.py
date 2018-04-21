import rsa
import time
from sqlalchemy.orm import sessionmaker

from kivy_client.db import SQLChatMessage, SQLMessage, SQLContact, SQLChat
from shared.packets import MessagePacket


class CommunicationList(object):
    """ Класс, отвечающий за работу окна сообщений """
    def __init__(self, client):
        self.client = client
        self.db_engine = client.db_engine
        self.client.handlers['add_message'] = self.add_message_handler
        self.client.handlers['send_message'] = self.send_message_handler

    def add_message_handler(self, command, response):
        if response is None:
            sender = command['from']
            receiver = command['to']
            message = command['message']
            m_time = command['time']

            session = sessionmaker(bind=self.db_engine)()
            if receiver.startswith('#'):
                db_message = SQLChatMessage(login=self.client.login, name=receiver, contact=sender, message=message, time=m_time)
                session.add(db_message)
                session.commit()
                chat = receiver
                # client.signals['text_message'].emit(db_message.name, db_message.contact, message)
            else:
                message = rsa.decrypt(bytes.fromhex(message), rsa.key.PrivateKey.load_pkcs1(bytes.fromhex(self.client.private_key), format='DER'))
                db_message = SQLMessage(user=self.client.login, u_from=sender, u_to=receiver, message=message.decode(), time=m_time)
                session.add(db_message)
                session.commit()
                chat = db_message.u_from if db_message.u_from != self.client.login else db_message.u_to
                # client.signals['text_message'].emit(chat, db_message.u_from, message.decode())
            session.close()

    def send_message_handler(self, command, response):
        contact = command['contact']
        message = command['message']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=self.client.login).filter_by(contact=contact).first()
        if db_contact:
            db_message = SQLMessage(user=self.client.login, u_from=self.client.login, u_to=db_contact.contact, message=message,
                                    time=int(time.time()))
            session.add(db_message)
            session.commit()

            public_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(db_contact.public_key), format='DER')
            crypted_text = rsa.encrypt(message.encode(), public_key)
            text_message = MessagePacket(self.client.login, contact, crypted_text.hex())
            # client.signals['text_message'].emit(contact, client.login, message)
            self.client.send_message(text_message)
        else:
            db_chat = session.query(SQLChat).filter_by(name=contact).first()
            if db_chat:
                db_message = SQLChatMessage(login=self.client.login, name=contact, contact=self.client.login, time=int(time.time()), message=message)
                session.add(db_message)
                session.commit()

                # client.signals['text_message'].emit(contact, client.login, message)
                text_message = MessagePacket(self.client.login, contact, message)
                self.client.send_message(text_message)

        session.close()
