from sqlalchemy import or_, and_
from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLContact
from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class DelContactPacketHandler(PacketHandler):
    def run(self, server, protocol, command):
        session = sessionmaker(bind=self.db_engine)()
        db_other = session.query(SQLUser).filter_by(name=command['name']).first()
        session.query(SQLContact).filter(
                or_(
                        and_(user=protocol.user.gid, contact=db_other.gid),
                        and_(user=db_other.gid, contact=protocol.user.gid)
                )
        )
        protocol.send_packet(ResponsePacket(202, command['id']))
        session.close()

