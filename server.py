import socket
import json
import sys
from collections import namedtuple

import commands


User = namedtuple('User', 'sock addr')


class Handler(object):
    """
        TODO: подумать над тем, чтобы в хэндлеры передавать объект со списком пользователей и чатов
    """
    pass


class AuthenticateHandler(Handler):
    """ Обработчик аутентификации пользователя
        TODO: добавить проверку пользователя в базе данных
    """
    @staticmethod
    def handle(command):
        return bytes(commands.Response(202))


class QuitHandler(Handler):
    """ Обработчик выхода пользователя.
    """
    @staticmethod
    def handle(command):
        return bytes(commands.Response(200))


class PresenceHandler(Handler):
    """ Обработчик присутствия пользователя на сервере.
    """
    @staticmethod
    def handle(command):
        return bytes(commands.Response(200))


class Server(object):
    """ Сервер мессенджера
    """
    client_sockets = []

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """ Запуск сервера
        """
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.socket.settimeout(5)

        # TODO: Сделать обработку отдельных клиентов по тредам
        user = User(*self.socket.accept())
        Server.client_sockets.append(user)

        while True:
            raw_data = user.sock.recv(1024)
            command = json.loads(raw_data.decode())
            self.processing(user, command)

    def processing(self, user, command):
        """ Обработка поступившей команды. """
        if command['action'] == 'authenticate':
            result = AuthenticateHandler.handle(command)
            user.sock.send(result)
        elif command['action'] == 'quit':
            Server.client_sockets.remove(user)
        elif command['action'] == 'presence':
            result = PresenceHandler.handle(command)
            user.sock.send(result)


if __name__ == '__main__':
    args = sys.argv
    # Получаем ip и port из коммандной строки,
    # показывать ошибку, если ip не указан
    if len(args) not in (3, 5):
        print("Ошибка запуска сервера:")
        print("server.py -a addr [port]")
        sys.exit()

    port = 7777
    for i, s in enumerate(args[1:]):
        if s == '-a':
            addr = args[i+1]
        elif s == '-p':
            port = int(args[2])

    server = Server(addr, port)
    server.run()
