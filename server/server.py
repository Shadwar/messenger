import socket
import sys
import select
import queue
import json
import logging
import threading
from time import sleep

from server.file_storage import FileStorage
from server.chat import Chat
from server.user import User
from shared.messages import *
from shared.responses import *
from server.message_handlers import *


logger = logging.getLogger('server')
server_users_lock = threading.Lock()
server_socket_lock = threading.Lock()


def accept_users(ssock, users):
    """ Отдельным потоком добавляем пользователей на сервер """
    global server_socket_lock
    global server_users_lock

    while True:
        server_socket_lock.acquire(blocking=True)
        try:
            sock, _ = ssock.accept()
            sock.setblocking(False)
            user = User(sock)

            server_users_lock.acquire(blocking=True)
            users[sock] = user
            server_users_lock.release()

            user.send_message(WelcomeMessage())
        except BlockingIOError:
            pass
        server_socket_lock.release()
        sleep(0.05)


def send_to_user(user):
    """ Обработка сокетов на запись """
    while True:
        try:
            message = user.send_messages.get()
        except queue.Empty:
            break
        else:
            user.sock.send(bytes(message))


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

        accept_thread = threading.Thread(target=accept_users, args=(self.socket, self.users))
        accept_thread.start()

        while True:
            user_sockets = [sock for sock in self.users.keys()]
            read_sockets, write_sockets, _ = select.select(user_sockets, user_sockets, [], 0)

            for sock in read_sockets:
                self.recv_from_user(self.users[sock])

            for sock in write_sockets:
                if sock in self.users:
                    threading.Thread(target=send_to_user, args=(self.users[sock],)).start()

            self.handle()
            sleep(0.05)

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
            for command in self.parse_raw_received(raw_data.decode()):
                user.recv_message(command)

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
            'get_messages': GetTextMessagesHandler
        })

    def get_online_user_by_login(self, login):
        """
        Получение пользователя по логину, если он онлайн
        :param login: str
        :return: User
        """
        for sock, user in self.users.items():
            if user.login == login:
                return user
        return None

    def parse_raw_received(self, raw):
        """ Парсит входящий массив на отдельные команды"""
        commands = []
        index = 0
        curl = 0
        command = ""
        while index < len(raw):
            command += raw[index]
            if raw[index] == '{':
                curl += 1
            elif raw[index] == '}':
                curl -= 1
                if curl == 0:
                    commands.append(json.loads(command))
                    command = ""
            index += 1

        print(commands)
        return commands
