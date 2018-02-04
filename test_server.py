import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import json
import server
import commands


class TestServer(TestCase):
    def setUp(self):
        # Создание мока сервера
        serv = Mock()
        serv.users = {}
        serv.chats = []
        # Создание мока пользователя
        self.serv = serv
        user_sock = Mock()
        user = server.User(user_sock)
        self.user = user

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

    def test_send_to_user(self):
        """ Сервер должен отправлять сообщение пользователю из его очереди сообщений на отправку """
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.bind.return_value = None
            mock_socket.return_value.listen.return_value = None
            mock_socket.return_value.setblocking.return_value = None
            mock_socket.return_value.accept.return_value = (mock_socket, None)
            serv = server.Server('127.0.0.1', 7777)
            user = server.User(Mock())
            serv.users[user.sock] = user
            user.send_messages.put(bytes('message'.encode()))
            serv.send_to_user(user)
            self.assertTrue(user.sock.send.callsed)
            self.assertEqual(user.sock.send.call_args[0][0], b'message')

    def test_recv_from_user(self):
        """ Сервер получает сообщение от пользователя и добавляет его в очередь сообщений пользователя."""
        self.serv.recv_from_user = server.Server.recv_from_user
        self.user.sock.recv.return_value = b'{"message":"1"}'

        self.serv.users[self.user.sock] = self.user
        self.serv.recv_from_user(self.serv, self.user)

        self.assertEqual({'message': '1'}, self.user.recv_messages.get_nowait())


class TestHandlers(TestCase):
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
