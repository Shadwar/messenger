import unittest
from unittest.mock import Mock, patch
import json
import server
import commands


class TestServer(unittest.TestCase):
    def test_accept_new_user(self):
        """ Сервер добавляет нового клиента """
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.bind.return_value = None
            mock_socket.return_value.listen.return_value = None
            mock_socket.return_value.settimeout.return_value = None
            mock_socket.return_value.setblocking.return_value = None
            mock_socket.return_value.accept.return_value = (mock_socket, None)

            serv = server.Server('127.0.0.1', 7777)
            self.assertEqual(len(serv.users), 0)
            serv.accept_users()
            self.assertEqual(len(serv.users), 1)

    def test_create_socket(self):
        """ Сервер создает новый сокет """
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.bind.return_value = None
            mock_socket.return_value.listen.return_value = None
            mock_socket.return_value.settimeout.return_value = None
            sock = server.Server.create_socket('127.0.0.1', 7777)
            self.assertTrue(mock_socket.called)
            self.assertTrue(sock.bind.called)
            self.assertTrue(sock.bind.listen)
            self.assertTrue(sock.bind.settimeout)


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.users = {}
        self.chats = []
        self.handler = server.ServerCommandHandler(self.users, self.chats)
        self.user_sock = Mock()
        self.user_sock.send.return_value = None
        self.user = server.User(self.user_sock)
        self.users[self.user_sock] = self.user

    def test_authenticate_returns_202(self):
        """ Обработчик аутентификации возвращает респонс с 202 кодом  """
        command = commands.AuthenticateCommand('ivan', 'vlado12')
        expected = json.dumps({"response": "202"}).encode()
        response = self.handler.handle(self.user, json.loads(str(command)))
        self.assertTrue(response == expected)

    def test_quit_return_200(self):
        """ Обработчик выхода возвращает респонс с 200 кодом - выход успешен """
        command = commands.QuitCommand()
        expected = json.dumps({"response": "200"}).encode()
        response = self.handler.handle(self.user, json.loads(str(command)))
        self.assertTrue(response == expected)

    def test_presence_return_200(self):
        """ Сообщение от пользователя о его нахождении на сервере - должен вернуться код 200 - успешно """
        command = commands.PresenceCommand('ivan', "I'm here")
        expected = json.dumps({"response": "200"}).encode()
        response = self.handler.handle(self.user, json.loads(str(command)))
        self.assertTrue(response == expected)
