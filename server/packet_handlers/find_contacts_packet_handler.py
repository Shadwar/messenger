from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLContact, SQLChat
from shared.packets import ErrorPacket, AlertPacket, FoundContactPacket
from .packet_handler import PacketHandler


class FindContactsPacketHandler(PacketHandler):
    """ Поиск контактов """
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        contacts = session.query(SQLUser).filter(SQLUser.login.ilike('%'+command['name']+'%')).all()
        chats = session.query(SQLChat).filter(SQLChat.name.ilike('%'+command['name']+'%')).all()
        if contacts or chats:
            protocol.send_packet(AlertPacket(200, command['id'], message='ok'))
            for contact in contacts:
                protocol.send_packet(FoundContactPacket(contact.login))
            for chat in chats:
                protocol.send_packet(FoundContactPacket(chat.name))
        else:
            protocol.send_packet(AlertPacket(400, command['id'], message='не найдено'))
        session.close()
