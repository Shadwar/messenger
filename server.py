import socket
import json
import sys
from collections import namedtuple

import commands


User = namedtuple('User', 'sock addr')


class ServerCommandHandler(object):
    """ Серверный обработчик команд, поступаемых от клиента """
    def __init__(self, users):
        self.users = users

    def handle(self, command, user):
        """ Обработка поступившей команды. """
        if command['action'] == 'authenticate':
            self.authenticate(command, user)
        elif command['action'] == 'quit':
            self.quit(user)
        elif command['action'] == 'presence':
            self.presence(command, user)

    def authenticate(self, command, user):
        """ Аутентификация пользователя """
        result = bytes(commands.Response(202))
        user.sock.send(result)

    def quit(self, user):
        """ Выход пользователя с сервера """
        self.users.remove(user)
        user.sock.send(bytes(commands.Response(200)))
        user.sock.close()

    def presence(self, command, user):
        """ Подтверждение нахождения пользователя на сервере """
        user.sock.send(bytes(commands.Response(200)))


class Server(object):
    """ Сервер мессенджера
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.users = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = ServerCommandHandler(self.users)

    def run(self):
        """ Запуск сервера
        """
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.socket.settimeout(5)

        # TODO: Сделать обработку отдельных клиентов по тредам
        user = User(*self.socket.accept())
        self.users.append(user)

        while True:
            raw_data = user.sock.recv(1024)
            command = json.loads(raw_data.decode())
            print(command)
            if 'action' in command:
                self.handler.handle(command, user)


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
