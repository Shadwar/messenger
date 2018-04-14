from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLMessage
from shared.packets import MessagePacket
from .packet_handler import PacketHandler


class GetMessagesPacketHandler(PacketHandler):
    """ Обработка запроса на все сообщения для определенного контакта """
    def run(self, server, protocol, command):
        contact = command['contact']
        last_time = int(command['time'])

        session = sessionmaker(bind=self.db_engine)()
        if contact.startswith('#'):
            pass
        else:
            db_contact = session.query(SQLUser).filter_by(login=contact).first()
            if db_contact:
                db_messages = session.query(SQLMessage)\
                    .filter(SQLMessage.u_to == protocol.user.gid)\
                    .filter(SQLMessage.time >= last_time).all()
                for db_message in db_messages:
                    sender_gid = db_message.u_from
                    receiver_gid = db_message.u_to
                    db_sender = session.query(SQLUser).filter_by(gid=sender_gid).first()
                    db_receiver = session.query(SQLUser).filter_by(gid=receiver_gid).first()
                    protocol.send_packet(MessagePacket(db_sender.login, db_receiver.login, db_message.message))
        session.close()
