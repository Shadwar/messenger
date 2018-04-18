from sqlalchemy.orm import sessionmaker

from client.db import SQLContact, SQLChat
from client.packet_handlers import MessageHandler
from shared.packets import GetMessagesPacket


class ChatContactHandler(MessageHandler):
    """ Обработчик полученных контактов чата """
    def run(self, client, command, response):
        chat_name = command['room']
        print(chat_name)
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter_by(login=client.login).filter_by(name=chat_name).first()
        if db_chat:
            session.close()
            return
        db_chat = SQLChat(login=client.login, name=chat_name)
        session.add(db_chat)
        session.commit()
        get_messages = GetMessagesPacket(chat_name)
        client.send_message(get_messages)
        client.signals['add_contact'].emit(chat_name)
        session.close()
