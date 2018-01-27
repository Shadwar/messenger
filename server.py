import socket
import json
import sys


class Server(object):
    """ Сервер мессенджера
    """

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

        while True:
            sock, addr = self.socket.accept()


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
