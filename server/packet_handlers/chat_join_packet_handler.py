from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUserChat, SQLChat
from shared.packets import ResponsePacket, AlertPacket
from .packet_handler import PacketHandler


class ChatJoinPacketHandler(PacketHandler):
    """ Подключение пользователя к чату """
    def run(self, server, protocol, command):
        chat_name = command['room']
        session = sessionmaker(bind=self.db_engine)()
        db_chat = session.query(SQLChat).filter(SQLChat.name.ilike(chat_name)).first()
        if db_chat:
            db_chat_user = SQLUserChat(user=protocol.user.gid, chat=db_chat.gid)
            session.add(db_chat_user)
            session.commit()
            protocol.send_packet(AlertPacket(202, command['id'], message=db_chat.name))
        else:
            protocol.send_packet(AlertPacket(404, command['id'], message="Чата с таким названием не существует."))
        session.close()
