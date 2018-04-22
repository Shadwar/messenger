import rsa
import time
from sqlalchemy.orm import sessionmaker

from client.back.db import SQLChatMessage, SQLMessage, SQLContact, SQLChat
from shared.packets import MessagePacket


class CommunicationList(object):
    """ Класс, отвечающий за работу окна сообщений """
    def __init__(self, client):
        self.client = client
        self.db_engine = client.db_engine
        self.client.handlers['message'] = self.add_message_handler
        self.client.handlers['send_message'] = self.send_message_handler

    def add_message_handler(self, command, response):
        sender = command['from']
        receiver = command['to']
        message = command['message']
        m_time = command['time']

        if response is None:
            session = sessionmaker(bind=self.db_engine)()
            if receiver.startswith('#'):
                db_message = SQLChatMessage(login=self.client.login, name=receiver, contact=sender, message=message, time=m_time)
                session.add(db_message)
                session.commit()
                chat = receiver
                self.client.messages[chat].append({'u_from': db_message.contact, 'message': message, 'time': m_time})

                if self.client.current_contact == chat:
                    self.client.send_event({'action': 'ui_add_message', 'u_from': db_message.contact, 'message': message, 'time': m_time})
            else:
                message_chunks = [bytes.fromhex(message)[i:i+64] for i in range(0, len(bytes.fromhex(message)), 64)]
                decrypted_chunks = []
                for chunk in message_chunks:
                    decrypted_chunks.append(rsa.decrypt(chunk, rsa.key.PrivateKey.load_pkcs1(bytes.fromhex(self.client.private_key), format='DER')))
                message = b''.join(decrypted_chunks)
                db_message = SQLMessage(user=self.client.login, u_from=sender, u_to=receiver, message=message.decode(), time=m_time)
                session.add(db_message)
                session.commit()
                chat = db_message.u_from if db_message.u_from != self.client.login else db_message.u_to
                self.client.messages[chat].append({'u_from': db_message.u_from, 'message': message.decode(), 'time': m_time})

                if self.client.current_contact == chat:
                    self.client.send_event({'action': 'ui_add_message', 'u_from': db_message.u_from, 'message': message, 'time': m_time})
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
            encoded = message.encode()
            message_chunks = [rsa.encrypt(encoded[i:i+40], public_key) for i in range(0, len(encoded), 40)]
            crypted_text = b''.join(message_chunks)
            text_message = MessagePacket(self.client.login, contact, crypted_text.hex())
            self.client.send_message(text_message)
            self.client.messages[db_contact.contact].append({'u_from': self.client.login, 'message': message, 'time': db_message.time})
            self.client.send_event({'action': 'ui_add_message', 'u_from': self.client.login, 'message': message, 'time': db_message.time})
        else:
            db_chat = session.query(SQLChat).filter_by(name=contact).first()
            if db_chat:
                db_message = SQLChatMessage(login=self.client.login, name=contact, contact=self.client.login, time=int(time.time()), message=message)
                session.add(db_message)
                session.commit()

                text_message = MessagePacket(self.client.login, contact, message)
                self.client.send_message(text_message)
                self.client.messages[db_message.name].append({'u_from': self.client.login, 'message': message, 'time': db_message.time})
                self.client.send_event({'action': 'ui_add_message', 'u_from': self.client.login, 'message': message, 'time': db_message.time})

        session.close()
