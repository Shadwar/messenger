import socket
import sys
import select
import queue
import json
import logging
from server.file_storage import FileStorage
from server.chat import Chat
from server.user import User
from shared.messages import *
from shared.responses import *
from server.message_handlers import *


logger = logging.getLogger('server')


class Server(object):
    """ Сервер мессенджера
    """
    def __init__(self, ip, port):
        self.socket = Server.create_socket(ip, port)
        self.users = {}
        self.chats = {}
        self.handlers = None
        self.init_handlers()

    def run(self):
        """ Запуск сервера
        """
        logger.info('Запуск сервера')
        while True:
            self.accept_users()

            user_sockets = [sock for sock in self.users.keys()]
            read_sockets, write_sockets, _ = select.select(user_sockets, user_sockets, [], 0)

            for sock in read_sockets:
                self.recv_from_user(self.users[sock])

            for sock in write_sockets:
                if sock in self.users:
                    self.send_to_user(self.users[sock])

            self.handle()

    def accept_users(self):
        """ Подключение нового пользователя к серверу
        """
        try:
            sock, _ = self.socket.accept()
            sock.setblocking(False)
            user = User(sock)
            self.users[sock] = user
        except BlockingIOError:
            pass

    def recv_from_user(self, user):
        """ Обработка сокетов на чтение """
        raw_data = user.sock.recv(1024)

        # Если возвращено 0 байт, значит пользователь отключился
        if not raw_data:
            del self.users[user.sock]
            user.sock.close()
            for chat in user.chats:
                chat.remove(user)
        else:
            command = json.loads(raw_data.decode())
            user.recv_message(command)

    def send_to_user(self, user):
        """ Обработка сокетов на запись """
        try:
            message = user.send_messages.get_nowait()
        except queue.Empty:
            pass
        else:
            user.sock.send(bytes(message))

    @classmethod
    def create_socket(cls, ip, port):
        """ Создание сокета сервера
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(5)
        sock.setblocking(False)
        return sock

    def handle(self):
        """ Обработка входящих команд пользователя """
        for user in self.users.values():
            try:
                message = user.recv_messages.get_nowait()
            except queue.Empty:
                pass
            else:
                action = message['action']
                if action in self.handlers:
                    self.handlers[action]().run(self, user, message)

    def init_handlers(self):
        """ Дорбавление обработчиков входящих сообщений """
        self.handlers = dict({
            'authenticate': AuthenticateMessageHandler,
            'quit': QuitMessageHandler,
            'msg': TextMessageHandler,
            'join': ChatJoinMessageHandler,
            'leave': ChatLeaveMessageHandler,
            'create': ChatCreateMessageHandler,
            'get_contacts': GetContactsMessageHandler,
            'add_contact': AddContactMessageHandler,
            'del_contact': DelContactMessageHandler,
        })
