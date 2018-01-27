import socket
import json
import sys
from collections import namedtuple

import commands


User = namedtuple('User', 'sock addr')


class Handler(object):
    pass


class AuthenticateHandler(Handler):
    """ Обработчик аутентификации пользователя
        TODO: добавить проверку пользователя в базе данных
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
        if command['action'] == 'quit':
            Server.client_sockets.remove(user)


if __name__ == '__main__':
    args = sys.argv
    # Получаем ip и port из коммандной строки,
    # показывать ошибку, если ip не указан
    if len(args) not in (2, 3):
        print("Ошибка запуска сервера:")
        print("server.py ip [port]")
        sys.exit()

    ip = args[1]
    try:
        port = int(args[2])
    except Exception:
        port = 5555

    server = Server(ip, port)
    server.run()
