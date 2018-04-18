from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLContact, SQLUser, SQLChat, SQLUserChat
from shared.packets import ChatContactPacket, ContactPacket
from .packet_handler import PacketHandler


class GetContactsPacketHandler(PacketHandler):
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        db_contacts = session.query(SQLContact).filter_by(user=protocol.user.gid).all()
        for db_c in db_contacts:
            contact = session.query(SQLUser).filter_by(gid=db_c.contact).first()
            contact_message = ContactPacket(contact.login, contact.public_key)
            protocol.send_packet(contact_message)
        db_chats = session.query(SQLUserChat, SQLChat)\
                          .join(SQLChat, SQLUserChat.chat == SQLChat.gid)\
                          .filter(SQLUserChat.user == protocol.user.gid).all()
        if db_chats:
            for db_user_chat, db_chat in db_chats:
                chat_name = db_chat.name
                chat_contact_message = ChatContactPacket(chat_name)
                protocol.send_packet(chat_contact_message)
        session.close()
