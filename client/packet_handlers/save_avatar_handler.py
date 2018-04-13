from sqlalchemy.orm import sessionmaker

from client.db import SQLUser
from client.packet_handlers import MessageHandler


class SaveAvatarHandler(MessageHandler):
    """ Сохранение аватара пользователя в базе данных """
    def run(self, client, command, response):
        session = sessionmaker(bind=self.db_engine)()
        filename = command['filename']
        avatar_data = open(filename, 'rb').read()
        db_user = session.query(SQLUser).filter_by(login=client.login).first()
        if db_user:
            db_user.avatar = avatar_data
            session.add(db_user)
            session.commit()
        session.close()
