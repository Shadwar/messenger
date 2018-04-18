from sqlalchemy.orm import sessionmaker

from client.db import SQLChat
from client.packet_handlers import MessageHandler


class ChatJoinHandler(MessageHandler):
    """ Обработчик ответа присоединения к чату """
    def run(self, client, command, response):
        chat_name = command['room']
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter_by(login=client.login).filter(SQLChat.name.ilike(chat_name)).first()
        if db_chat:
            pass

        if response and response['response'] == 202:
            name = response['alert']
            db_chat = SQLChat(login=client.login, name=name)
            session.add(db_chat)
            session.commit()
            client.signals['add_contact'].emit(name)

        session.close()
