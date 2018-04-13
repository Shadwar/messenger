import rsa
from sqlalchemy.orm import sessionmaker

from client.db import SQLUser
from client.message_handlers import MessageHandler
from shared.generate import get_hash
from shared.packets import AuthenticatePacket


class ClientAuthenticationHandler(MessageHandler):
    """ Загрузка или создание ключей шифрования """
    def run(self, client, command, response):
        session = sessionmaker(bind=self.db_engine)()
        login = command['login']
        password = command['password']
        hashed_password = get_hash(login, password)

        db_user = session.query(SQLUser).filter_by(login=login).filter_by(password=hashed_password).first()
        if db_user:
            pass
        else:
            (public_key, private_key) = rsa.newkeys(512)
            db_user = SQLUser(
                    login=login,
                    password=hashed_password,
                    public_key=public_key.save_pkcs1('DER').hex(),
                    private_key=private_key.save_pkcs1('DER').hex()
            )
            session.add(db_user)
            session.commit()

        client = command['client']
        client.private_key = db_user.private_key
        client.public_key = db_user.public_key

        session.close()
        message = AuthenticatePacket(login, password, db_user.public_key)
        client.send_message(message)
