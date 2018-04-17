from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLContact
from shared.packets import ErrorPacket, AlertPacket
from shared.packets.contact_packet import ContactPacket
from .packet_handler import PacketHandler


class AddContactPacketHandler(PacketHandler):
    """ Добавление нового контакта пользователем """
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        contact = session.query(SQLUser).filter(SQLUser.login.ilike(command['contact'])).first()
        if contact:
            db_contact = session.query(SQLContact).filter_by(user=protocol.user.gid).filter_by(contact=contact.gid).first()
            if db_contact:
                protocol.send_packet(ErrorPacket(400, command['id'], message='Такой контакт уже существует'))
            else:
                db_contact = SQLContact(user=protocol.user.gid, contact=contact.gid)
                session.add(db_contact)
                other_contact = SQLContact(user=contact.gid, contact=protocol.user.gid)
                session.add(other_contact)
                session.commit()
                protocol.send_packet(AlertPacket(200, command['id'], [contact.login, contact.public_key]))
                other = server.logged_users.get(contact.login)
                if other:
                    command = ContactPacket(protocol.user.login, protocol.user.public_key)
                    other.protocol.send_packet(command)
        else:
            protocol.send_packet(ErrorPacket(400, command['id'], message='Такой пользователь не найден.'))
        session.close()
