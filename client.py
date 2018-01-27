import socket
import json
import sys
import commands


class Handler(object):
    pass


class ProbeHandler(Handler):
    @staticmethod
    def handle(command):
        return bytes(commands.PresenceCommand('ivan', "I'm here"))


class Client(object):
    """ Клиент мессенджера
    """
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """ Запуск клиента, подключение к серверу, запуск цикла обработки сообщений
        """
        self.socket.connect((self.addr, self.port))

        if self.authenticate():
            while True:
                debug_pause = input('next packet:')
                presence_command = commands.PresenceCommand('ivan', "I'm here")
                self.socket.send(bytes(presence_command))
                received = self.socket.recv(1024)
                print(received)

    def authenticate(self):
        """ Аутентификация пользователя
            :return: True|False - в зависимости от успеха
        """
        auth_command = commands.AuthenticateCommand('ivan', 'vlado12')
        self.socket.send(bytes(auth_command))
        response = json.loads(self.socket.recv(1024).decode())
        return response.get('response', 404) == '202'


if __name__ == '__main__':
    args = sys.argv

    if len(args) not in (2, 3):
        print("Ошибка запуска клиента:")
        print("client.py addr [port]")
        sys.exit()

    addr = args[1]

    try:
        port = int(args[2])
    except Exception:
        port = 7777

    client = Client(addr, port)
    client.run()
