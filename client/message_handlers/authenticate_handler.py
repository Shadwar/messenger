from sqlalchemy.orm import sessionmaker

from client.alchemy import SQLContact, SQLMessage
from client.message_handlers.message_handler import MessageHandler
from shared.messages import GetTextMessages, GetContactsMessage


class AuthenticateHandler(MessageHandler):
    """ Аутентификация на сервере """
    def run(self, client, command, response):
        if response and response['response'] == 202:
            client.signals['login_ok'].emit()
            client.login = command['user']['account_name']
            # Загрузить все данные
            session = sessionmaker(bind=self.db_engine)()
            db_contacts = session.query(SQLContact).filter_by(login=client.login).all()
            for db_contact in db_contacts:
                client.signals['add_contact'].emit(db_contact.contact)

            db_messages = session.query(SQLMessage).filter_by(user=client.login).all()
            for db_message in db_messages:
                chat = db_message.u_from if db_message.u_from != client.login else db_message.u_to
                client.signals['text_message'].emit(chat, db_message.u_from, db_message.message)

            for db_contact in db_contacts:
                get_messages = GetTextMessages(db_contact.contact)
                db_last_message = session.query(SQLMessage).filter_by(user=client.login).order_by('-gid').first()
                if db_last_message:
                    get_messages.data['time'] = db_last_message.time
                else:
                    get_messages.data['time'] = 0

                client.send_message(get_messages)

            session.close()
            get_contacts = GetContactsMessage()
            client.send_message(get_contacts)
        else:
            client.signals['login_error'].emit()
