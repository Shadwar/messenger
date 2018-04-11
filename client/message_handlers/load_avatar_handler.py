import io

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon
from sqlalchemy.orm import sessionmaker

from client.db import SQLUser
from client.message_handlers import MessageHandler


class LoadAvatarHandler(MessageHandler):
    """ Загрузка аватара пользователя из базы данных """
    def run(self, client, command, response):
        session = sessionmaker(bind=self.db_engine)()
        db_user = session.query(SQLUser).filter_by(login=client.login).first()
        if db_user:
            avatar_data = db_user.avatar

            if avatar_data:
                image = Image.open(io.BytesIO(avatar_data))
                pixmap = QPixmap.fromImage(ImageQt(image.convert('RGBA')))
                icon = QIcon()
                icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
                command['container'].setIcon(icon)
        session.close()
