import socket
import sys
import select
import queue
import json
import commands
import log_config
from lib import log


class User(object):
    """ Пользователь """
    def __init__(self, sock):
        self.sock = sock
        self.recv_messages = queue.Queue()
        self.send_messages = queue.Queue()

    def send_message(self, message):
        self.send_messages.put(message)


class Chat(object):
    """ Чат """
    def __init__(self, title):
        self.title = title
        self.users = []

    def connect(self, user):
        """ Добавление нового пользователя в чат """
        self.users.append(user)

    def remove(self, user):
        """ Убирает пользователя из чата """
        self.users.remove(user)

    def send_message(self, message):
        """ Отправка сообщения в чат всем пользователям """
        for u in self.users:
            u.send_message(message)


class ServerCommandHandler(object):
    """ Серверный обработчик команд, поступающих от клиента """
    def __init__(self, users, chats):
        self.users = users
        self.chats = chats

    def handle(self, command):
        """ Обработка поступившей команды. """
        if command['action'] == 'authenticate':
            return self.authenticate(command)
        elif command['action'] == 'quit':
            return self.quit()
        elif command['action'] == 'presence':
            return self.presence(command)

    def authenticate(self, command):
        """ Аутентификация пользователя """
        return bytes(commands.Response(202))

    def quit(self):
        """ Выход пользователя с сервера """
        return bytes(commands.Response(200))

    def presence(self, command):
        """ Подтверждение нахождения пользователя на сервере """
        return bytes(commands.Response(200))


class Server(object):
    """ Сервер мессенджера
    """
    def __init__(self, ip, port):
        self.socket = Server.create_socket(ip, port)
        self.users = {}
        self.chats = []
        self.handler = ServerCommandHandler(self.users, self.chats)

    def run(self):
        """ Запуск сервера
        """
        while True:
            self.accept_users()

            user_sockets = [sock for sock in self.users.keys()]

            read_sockets, write_sockets, _ = select.select(user_sockets, user_sockets, [], 0)
            print(self.users)

            for sock in read_sockets:
                self.recv_from_user(self.users[sock])

            for sock in write_sockets:
                if sock in self.users:
                    self.send_to_user(self.users[sock])

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
            for chat in self.chats:
                chat.remove(user)
        else:
            command = json.loads(raw_data.decode())
            response = self.handler.handle(command)
            user.send_message(response)

    def send_to_user(self, user):
        """ Обработка сокетов на запись """
        try:
            message = user.send_messages.get_nowait()
        except queue.Empty:
            pass
        else:
            user.sock.send(message)

    @classmethod
    def create_socket(cls, ip, port):
        """ Создание сокета сервера
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(5)
        sock.setblocking(False)
        return sock


if __name__ == '__main__':
    args = sys.argv
    # Получаем ip и port из коммандной строки,
    # показывать ошибку, если ip не указан
    if len(args) not in (3, 5):
        print("Ошибка запуска сервера:")
        print("server.py -a addr [-p port]")
        sys.exit()

    port = 7777
    for i, s in enumerate(args):
        if s == '-a':
            addr = args[i+1]
        elif s == '-p':
            port = int(args[i+1])

    server = Server(addr, port)
    server.run()
