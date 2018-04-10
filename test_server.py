import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import json
import server
from server.user import User
from server.server import Server
from shared.responses import *
from shared.messages import *
from server.message_handlers import *

# class TestServer(TestCase):
#     def setUp(self):
#         # Создание мока сервера
#         serv = Mock()
#         serv.users = {}
#         serv.chats = []
#         # Создание мока пользователя
#         self.serv = serv
#         user_sock = Mock()
#         user = User(user_sock)
#         self.user = user
#
#     def test_accept_new_user(self):
#         """ Сервер добавляет нового клиента """
#         with patch('socket.socket') as mock_socket:
#             mock_socket.return_value.bind.return_value = None
#             mock_socket.return_value.listen.return_value = None
#             mock_socket.return_value.settimeout.return_value = None
#             mock_socket.return_value.setblocking.return_value = None
#             mock_socket.return_value.accept.return_value = (mock_socket, None)
#
#             serv = Server('127.0.0.1', 7777)
#             self.assertEqual(len(serv.users), 0)
#             serv.accept_users()
#             self.assertEqual(len(serv.users), 1)
#
#     def test_create_socket(self):
#         """ Сервер создает новый сокет """
#         with patch('socket.socket') as mock_socket:
#             mock_socket.return_value.bind.return_value = None
#             mock_socket.return_value.listen.return_value = None
#             mock_socket.return_value.settimeout.return_value = None
#             sock = Server.create_socket('127.0.0.1', 7777)
#             self.assertTrue(mock_socket.called)
#             self.assertTrue(sock.bind.called)
#             self.assertTrue(sock.bind.listen)
#             self.assertTrue(sock.bind.settimeout)
#
#     def test_send_to_user(self):
#         """ Сервер должен отправлять сообщение пользователю из его очереди сообщений на отправку """
#         with patch('socket.socket') as mock_socket:
#             mock_socket.return_value.bind.return_value = None
#             mock_socket.return_value.listen.return_value = None
#             mock_socket.return_value.setblocking.return_value = None
#             mock_socket.return_value.accept.return_value = (mock_socket, None)
#             serv = Server('127.0.0.1', 7777)
#             user = User(Mock())
#             serv.users[user.sock] = user
#             user.send_messages.put(bytes('message'.encode()))
#             serv.send_to_user(user)
#             self.assertTrue(user.sock.send.callsed)
#             self.assertEqual(user.sock.send.call_args[0][0], b'message')
#
#     def test_recv_from_user(self):
#         """ Сервер получает сообщение от пользователя и добавляет его в очередь сообщений пользователя."""
#         self.serv.recv_from_user = Server.recv_from_user
#         self.user.sock.recv.return_value = b'{"message":"1"}'
#
#         self.serv.users[self.user.sock] = self.user
#         self.serv.recv_from_user(self.serv, self.user)
#
#         self.assertEqual({'message': '1'}, self.user.recv_messages.get_nowait())
#
#
# class TestHandlers(TestCase):
#     def setUp(self):
#         self.users = {}
#         self.chats = []
#         self.user_sock = Mock()
#         self.user_sock.send.return_value = None
#         self.user = User(self.user_sock)
#         self.users[self.user_sock] = self.user
#         self.server =
#
#     def test_authenticate_returns_202(self):
#         """ Обработчик аутентификации возвращает респонс с 402 кодом - такого пользователя нет """
#         command = json.loads(bytes(AuthenticateMessage('ivan', 'vlado12')).decode())
#         AuthenticateMessageHandler().run(self.server, self.user, command)
#         result = self.user.send_messages.get_nowait()
#         self.assertTrue(result.data['response'] == 402)
#
#     def test_quit_return_200(self):
#         """ Обработчик выхода возвращает респонс с 200 кодом - выход успешен """
#         command = json.loads(bytes(QuitMessage()).decode())
#         QuitMessageHandler().run(self.server, self.user, command)
#         result = self.user.send_messages.get_nowait()
#         self.assertTrue(result.data['response'] == 200)
#
#     def test_presence_return_200(self):
#         """ Сообщение от пользователя о его нахождении на сервере - должен вернуться код 200 - успешно """
#         command = json.loads(bytes(PresenceMessage('ivan', "I'm here")).decode())
#         PresenceMessageHandler().run(self.server, self.user, command)
#         result = self.user.send_messages.get_nowait()
#         self.assertTrue(result.data['response'] == 200)
#
#     def test_create_chat_return_200_if_not_exists(self):
#         """ При создании нового чата должен вернуться 200 ответ """
#         command = json.loads(bytes(ChatCreateMessage('#test_room')).decode())
#         ChatCreateMessageHandler().run(self.server, self.user, command)
#         result = self.user.send_messages.get_nowait()
#         self.assertTrue(result.data['response'] == 200)

    # def test_create_chat_return_400_if_already_exists(self):
    #     """ Если такой чат уже существует - вернуть 400 ошибку """
    #     command = ChatCreateMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = self.user.send_messages.get_nowait()
    #     self.handler.handle(self.user, command.data)
    #     second_message = json.loads(self.user.send_messages.get_nowait().decode())
    #     self.assertTrue(second_message['response'] == 400)
    #
    # def test_join_not_exists_chat_return_404(self):
    #     """ При попытке подключения к несуществующему чату, выдать ошибку 404 """
    #     command = ChatJoinMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = json.loads(self.user.send_messages.get_nowait().decode())
    #     self.assertTrue(message['response'] == 404)
    #
    # def test_join_to_exists_chat_return_200(self):
    #     """ При подключении к существующему чату выдает ответ 200 """
    #     command = ChatCreateMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = self.user.send_messages.get_nowait()
    #     command = ChatJoinMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = json.loads(self.user.send_messages.get_nowait().decode())
    #     self.assertTrue(message['response'] == 200)
    #
    # def test_leave_chat_return_200(self):
    #     """ При выходе из существующего чата возвращается ответ 200"""
    #     command = ChatCreateMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = self.user.send_messages.get_nowait()
    #     command = ChatLeaveMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = json.loads(self.user.send_messages.get_nowait().decode())
    #     self.assertTrue(message['response'] == 200)
    #
    # def test_leave_not_exists_chat_return_400(self):
    #     """ Если при выходе такого чата не существует - возвращается ответ 400 """
    #     command = ChatLeaveMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = json.loads(self.user.send_messages.get_nowait().decode())
    #     self.assertTrue(message['response'] == 400)
    #
    # def test_send_message_to_user(self):
    #     """ Отправка сообщения пользователю передает его указанному получателю """
    #     self.user.name = 'name1'
    #     user2_sock = Mock()
    #     user2_sock.send.return_value = None
    #     user2 = User(user2_sock)
    #     user2.name = 'name2'
    #     self.users[user2_sock] = user2
    #
    #     command = TextMessage(self.user.name, user2.name, 'Message')
    #     self.handler.handle(self.user, command.data)
    #     message = json.loads(user2.send_messages.get_nowait().decode())
    #     self.assertTrue(message['message'] == 'Message')
    #
    # def test_send_message_to_chat(self):
    #     self.user.name = 'name1'
    #     user2_sock = Mock()
    #     user2_sock.send.return_value = None
    #     user2 = User(user2_sock)
    #     user2.name = 'name2'
    #     self.users[user2_sock] = user2
    #
    #     command = ChatCreateMessage('#test_room')
    #     self.handler.handle(self.user, command.data)
    #     message = self.user.send_messages.get_nowait()
    #
    #     command = ChatJoinMessage('#test_room')
    #     self.handler.handle(user2, command.data)
    #     message = user2.send_messages.get_nowait().decode()
    #
    #     command = TextMessage(self.user.name, '#test_room', 'Message')
    #     self.handler.handle(self.user, command.data)
    #
    #     message1 = json.loads(self.user.send_messages.get_nowait().decode())
    #     message2 = json.loads(user2.send_messages.get_nowait().decode())
    #
    #     self.assertTrue(message1['message'] == 'Message')
    #     self.assertTrue(message2['message'] == 'Message')
