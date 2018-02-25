import abc

from shared.responses import *
from shared.messages import *
from client.alchemy import *


class MessageHandler(object):
    """ Обработчик команд """
    def __init__(self):
        self.db_engine = create_engine('sqlite:///client.db')

    @abc.abstractmethod
    def run(self, client, command, response):
        """ Обработка команды и возврат значения """
        pass


class AuthenticateHandler(MessageHandler):
    """ Аутентификация на сервере """
    def run(self, client, command, response):
        if response and response['response'] == 202:
            client.signals['login_ok'].emit()
        else:
            client.signals['login_error'].emit()


class ProbeHandler(MessageHandler):
    def run(self, client, command, response):
        presence = PresenceMessage(client.login, 'online')
        client.send_message(presence)
