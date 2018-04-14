from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLContact, SQLUser
from shared.packets.contact_packet import ContactPacket
from .packet_handler import PacketHandler


class GetContactsPacketHandler(PacketHandler):
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        db_contacts = session.query(SQLContact).filter_by(user=protocol.user.gid).all()
        for db_c in db_contacts:
            contact = session.query(SQLUser).filter_by(gid=db_c.contact).first()
            contact_message = ContactPacket(contact.login, contact.public_key)
            protocol.send_packet(contact_message)
        session.close()
