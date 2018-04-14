from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser
from shared.generate import get_hash
from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class AuthenticatePacketHandler(PacketHandler):
    def run(self, server, protocol, command):
        login = command['account_name']
        password = command['password']
        public_key = command['public_key']
        hashed_password = get_hash(login, password)

        session = sessionmaker(bind=self.db_engine)()
        db_user = session.query(SQLUser).filter_by(login=login).first()
        if db_user:
            if db_user.password != hashed_password:
                protocol.send_packet(ResponsePacket(402, command['id']))
                session.close()
                return
        else:
            db_user = SQLUser(login=login, password=hashed_password, public_key=public_key)
            session.add(db_user)
            session.commit()

        user = protocol.User()
        user.gid = db_user.gid
        user.login = db_user.login
        user.public_key = db_user.public_key
        user.protocol = protocol
        protocol.user = user

        server.logged_users.update({
            user.login: user
        })
        protocol.send_packet(ResponsePacket(202, command['id']))
