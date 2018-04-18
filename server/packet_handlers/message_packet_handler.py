from sqlalchemy.orm import sessionmaker

from server.alchemy import SQLUser, SQLChat, SQLChatMessage, SQLMessage, SQLUserChat
from shared.packets import MessagePacket, ResponsePacket
from .packet_handler import PacketHandler


class MessagePacketHandler(PacketHandler):
    """ Добавление нового контакта пользователем """
    def run(self, server, protocol, command):
        sender = command['from']
        receiver = command['to']
        message = command['message']
        text_message = MessagePacket(sender, receiver, message)

        session = sessionmaker(bind=self.db_engine)()
        db_message = None

        if receiver.startswith('#'):
            db_receiver = session.query(SQLChat).filter_by(name=receiver).first()
            if db_receiver:
                db_message = SQLChatMessage(
                        u_from=protocol.user.gid,
                        u_to=db_receiver.gid,
                        time=command['time'],
                        message=message)
                users = session.query(SQLUserChat, SQLUser).join(SQLUser, SQLUser.gid == SQLUserChat.user).filter(SQLUserChat.chat == db_receiver.gid).all()
                if users:
                    for user_chat, user in users:
                        if user.login != sender:
                            receiver_user = server.logged_users.get(user.login)
                            if receiver_user:
                                receiver_user.protocol.send_packet(text_message)

        else:
            receiver_user = server.logged_users.get(receiver)
            if receiver_user:
                receiver_user.protocol.send_packet(text_message)

            db_receiver = session.query(SQLUser).filter_by(login=receiver).first()
            if db_receiver:
                db_message = SQLMessage(
                        u_from=protocol.user.gid,
                        u_to=db_receiver.gid,
                        time=command['time'],
                        message=message
                )
        if db_message:
            session.add(db_message)
            session.commit()

        session.close()
        protocol.send_packet(ResponsePacket(202, command['id']))
