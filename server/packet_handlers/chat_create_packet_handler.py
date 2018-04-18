from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLChat, SQLUserChat
from server.chat import Chat
from shared.packets import AlertPacket, ResponsePacket
from .packet_handler import PacketHandler


class ChatCreatePacketHandler(PacketHandler):
    """ Создание нового чата """
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        chat_name = command['room']
        db_chat = session.query(SQLChat).filter(SQLChat.name.ilike(chat_name)).first()
        if db_chat:
            protocol.send_packet(AlertPacket(400, command['id'], message='Чат с таким названием уже существует'))
        else:
            db_chat = SQLChat(name=chat_name)
            session.add(db_chat)
            session.commit()

            db_user_chat = SQLUserChat(user=protocol.user.gid, chat=db_chat.gid)
            session.add(db_user_chat)
            session.commit()

            protocol.send_packet(AlertPacket(202, command['id'], message=chat_name))
        session.close()
