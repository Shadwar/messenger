from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUserChat
from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class ChatLeavePacketHandler(PacketHandler):
    """ Выход пользователя из чата """
    def run(self, server, protocol, command):
        chat_name = command['room']
        chat = server.chats[chat_name]
        chat.users.remove(protocol)
        session = sessionmaker(bind=self.db_engine)()
        session.query(SQLUserChat).filter_by(chat=chat.gid).filter_by(user=protocol.user.gid).delete()
        session.close()
        protocol.send_packet(ResponsePacket(202, command[id]))

