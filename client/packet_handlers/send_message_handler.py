import time

import rsa
from sqlalchemy.orm import sessionmaker

from client.db import SQLContact, SQLMessage, SQLChat, SQLChatMessage
from client.packet_handlers import MessageHandler
from shared.packets import MessagePacket


class SendMessageHandler(MessageHandler):
    """ Шифрование и отправка сообщения на сервер """
    def run(self, client, command, response):
        contact = command['contact']
        message = command['message']
        session = sessionmaker(bind=self.db_engine)()
        db_contact = session.query(SQLContact).filter_by(login=client.login).filter_by(contact=contact).first()
        if db_contact:
            db_message = SQLMessage(user=client.login, u_from=client.login, u_to=db_contact.contact, message=message,
                                    time=int(time.time()))
            session.add(db_message)
            session.commit()

            public_key = rsa.PublicKey.load_pkcs1(bytes.fromhex(db_contact.public_key), format='DER')
            crypted_text = rsa.encrypt(message.encode(), public_key)
            text_message = MessagePacket(client.login, contact, crypted_text.hex())
            client.signals['text_message'].emit(contact, client.login, message)
            client.send_message(text_message)
        else:
            db_chat = session.query(SQLChat).filter_by(name=contact).first()
            if db_chat:
                db_message = SQLChatMessage(login=client.login, name=contact, contact=client.login, time=int(time.time()), message=message)
                session.add(db_message)
                session.commit()

                client.signals['text_message'].emit(contact, client.login, message)
                text_message = MessagePacket(client.login, contact, message)
                client.send_message(text_message)

        session.close()
