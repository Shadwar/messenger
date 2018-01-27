import socket
import json
import sys
import commands


class Client(object):
    """ Клиент мессенджера
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        """ Запуск клиента, подключение к серверу, запуск цикла обработки сообщений
        """
        self.socket.connect((self.ip, self.port))

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
        print("client.py ip [port]")
        sys.exit()

    ip = args[1]

    try:
        port = int(args[2])
    except Exception:
        port = 5555

    client = Client(ip, port)
    client.run()
