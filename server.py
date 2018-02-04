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
        self.name = None

    def send_message(self, message):
        self.send_messages.put(message)

    def recv_message(self, message):
        self.recv_messages.put(message)


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

    def execute(self):
        """ Производит обработку входящих команд от всех пользователей"""
        for user in list(self.users.values()):
            while not user.recv_messages.empty():
                command = user.recv_messages.get_nowait()
                self.handle(user, command)

    def handle(self, user, command):
        """ Обработка поступившей команды. """
        if command['action'] == 'authenticate':
            self.authenticate(user, command)
        elif command['action'] == 'quit':
            self.quit(user)
        elif command['action'] == 'presence':
            self.presence(user, command)
        elif command['action'] == 'create':
            self.create_chat(user, command)
        elif command['action'] == 'join':
            self.join_chat(user, command)
        elif command['action'] == 'leave':
            self.leave_chat(user, command)

    def authenticate(self, user, command):
        """ Аутентификация пользователя """
        user.name = command['user']['account_name']
        user.send_message(bytes(commands.Response(202)))

    def quit(self, user):
        """ Выход пользователя с сервера """
        del self.users[user.sock]
        for chat in self.chats:
            if user in chat.users:
                chat.users.remove(user)
        user.send_message(bytes(commands.Response(200)))

    def presence(self, user, command):
        """ Подтверждение нахождения пользователя на сервере """
        user.send_message(bytes(commands.Response(200)))

    def create_chat(self, user, command):
        """ Создание нового чата """
        title = command['room']
        if title in [chat.title for chat in self.chats]:
            user.send_message(bytes(commands.ErrorResponse(400, 'Чат с таким названием уже существует')))
        else:
            chat = Chat(title)
            chat.users.append(user)
            self.chats.append(chat)
            user.send_message(bytes(commands.Response(200)))

    def join_chat(self, user, command):
        """ Присоединение к существующему чату """
        title = command['room']
        for chat in self.chats:
            if title == chat.title:
                if user not in chat.users:
                    chat.users.append(user)
                user.send_message(bytes(commands.Response(200)))
        user.send_message(bytes(commands.ErrorResponse(404, 'Чат с таким названием не найден')))

    def leave_chat(self, user, command):
        """ Покинуть чат """
        title = command['room']
        for chat in self.chats:
            if title == chat.title and user in chat.users:
                chat.users.remove(user)
                user.send_message(bytes(commands.Response(200)))
        user.send_message(bytes(commands.ErrorResponse(400, 'Пользователь не находится в указанном чате')))



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

            for sock in read_sockets:
                self.recv_from_user(self.users[sock])

            for sock in write_sockets:
                if sock in self.users:
                    self.send_to_user(self.users[sock])

            self.handler.execute()

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
            user.recv_message(command)

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
