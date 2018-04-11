import rsa
from sqlalchemy.orm import sessionmaker

from client.db import SQLMessage
from client.message_handlers.message_handler import MessageHandler


class TextMessageHandler(MessageHandler):
    """ Обработчик текстовых сообщений """
    def run(self, client, command, response):
        if response is None:
            sender = command['from']
            receiver = command['to']
            message = command['message']
            message = rsa.decrypt(bytes.fromhex(message), rsa.key.PrivateKey.load_pkcs1(bytes.fromhex(client.private_key), format='DER'))
            m_time = command['time']
            session = sessionmaker(bind=self.db_engine)()
            db_message = SQLMessage(user=client.login, u_from=sender, u_to=receiver, message=message.decode(), time=m_time)
            session.add(db_message)
            session.commit()
            chat = db_message.u_from if db_message.u_from != client.login else db_message.u_to
            client.signals['text_message'].emit(chat, db_message.u_from, message.decode())
            session.close()
