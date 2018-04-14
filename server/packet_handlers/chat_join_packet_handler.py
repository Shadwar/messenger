from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUserChat
from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class ChatJoinPacketHandler(PacketHandler):
    """ Подключение пользователя к чату """
    def run(self, server, protocol, command):
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.append(protocol)

        session = sessionmaker(bind=self.db_engine)()
        db_chat_user = SQLUserChat(user=protocol.user.gid, chat=chat.gid)
        session.add(db_chat_user)
        session.commit()
        session.close()
        protocol.send_packet(ResponsePacket(202, command['id']))
