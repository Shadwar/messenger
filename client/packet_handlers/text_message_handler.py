import rsa
from sqlalchemy.orm import sessionmaker

from client.db import SQLMessage, SQLChatMessage
from client.packet_handlers import MessageHandler


class TextMessageHandler(MessageHandler):
    """ Обработчик текстовых сообщений """
    def run(self, client, command, response):
        if response is None:
            sender = command['from']
            receiver = command['to']
            message = command['message']
            m_time = command['time']

            session = sessionmaker(bind=self.db_engine)()
            if receiver.startswith('#'):
                db_message = SQLChatMessage(login=client.login, name=receiver, contact=sender, message=message, time=m_time)
                session.add(db_message)
                session.commit()
                chat = receiver
                client.signals['text_message'].emit(db_message.name, db_message.contact, message)
            else:
                message = rsa.decrypt(bytes.fromhex(message), rsa.key.PrivateKey.load_pkcs1(bytes.fromhex(client.private_key), format='DER'))
                db_message = SQLMessage(user=client.login, u_from=sender, u_to=receiver, message=message.decode(), time=m_time)
                session.add(db_message)
                session.commit()
                chat = db_message.u_from if db_message.u_from != client.login else db_message.u_to
                client.signals['text_message'].emit(chat, db_message.u_from, message.decode())
            session.close()
