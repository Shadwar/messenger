import unittest
from unittest.mock import Mock
import socket
import json
import server
import commands


class TestServer(unittest.TestCase):
    pass


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.users = []
        self.handler = server.ServerCommandHandler(self.users)
        self.user_sock = Mock()
        self.user_sock.send.return_value = None
        self.user = server.User(self.user_sock, None)

    def test_authenticate_returns_202(self):
        """ Обработчик аутентификации возвращает респонс с 202 кодом  """
        command = commands.AuthenticateCommand('ivan', 'vlado12')
        expected = json.dumps({"response": "202"}).encode()
        self.handler.handle(json.loads(str(command)), self.user)
        self.assertTrue(self.user_sock.send.call_args == ((expected,),))

    def test_quit_return_200(self):
        """ Обработчик выхода возвращает респонс с 200 кодом - выход успешен """
        command = commands.QuitCommand()
        expected = json.dumps({"response": "200"}).encode()
        self.users.append(self.user)
        self.handler.handle(json.loads(str(command)), self.user)
        self.assertTrue(self.user_sock.send.call_args == ((expected,),))

    def test_presence_return_200(self):
        """ Сообщение от пользователя о его нахождении на сервере - должен вернуться код 200 - успешно """
        command = commands.PresenceCommand('ivan', "I'm here")
        expected = json.dumps({"response": "200"}).encode()
        self.handler.handle(json.loads(str(command)), self.user)
        self.assertTrue(self.user_sock.send.call_args == ((expected,),))
