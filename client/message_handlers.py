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


class WelcomeHandler(MessageHandler):
    """ Приглашение от сервера, сделать аутентификацию """
    def run(self, client, command, response):
        if not response or response['response'] != 202:
            user_name = input('username: ')
            password = input('password: ')
            auth_command = AuthenticateMessage(user_name, password)
            client.send_message(auth_command)


class ProbeHandler(MessageHandler):
    def run(self, client, command, response):
        presence = PresenceMessage(client.login, 'online')
        client.send_message(presence)
