import socket
import json
import sys
import commands


class ClientCommandHandler(object):
    """ Обработчик команд, поступивших от сервера """
    def __init__(self, name, sock):
        self.name = name
        self.socket = sock

    def handle(self, command):
        """ Обработка команд """
        if command['action'] == 'probe':
            self.socket.send(bytes(commands.PresenceCommand('ivan', "I'm here")))


class Client(object):
    """ Клиент мессенджера
    """
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = ClientCommandHandler('ivan', self.socket)
        self.user_name = ''
        self.password = ''

    def run(self):
        """ Запуск клиента, подключение к серверу, запуск цикла обработки сообщений
        """
        self.socket.connect((self.addr, self.port))

        if self.authenticate():
            print('Command list:')
            print('c - create chat. (c chat_name)')
            print('j - join chat. (j chat_name)')
            print('l - leave chat. (l chat_name)')
            print('s - send message. (s receiver message)')
            print('q - quit from server. (q)')
            while True:
                user_command = input('next command (enter to pass): ').split()
                user_command.append(None)

                if user_command[0] == 'q':
                    send_command = commands.QuitCommand()
                elif user_command[0] == 'c':
                    if user_command[1][0] != '#':
                        user_command[1] = '#' + user_command[1]
                    send_command = commands.ChatCreateCommand(user_command[1])
                elif user_command[0] == 'j':
                    send_command = commands.ChatJoinCommand(user_command[1])
                elif user_command[0] == 'l':
                    send_command = commands.ChatLeaveCommand(user_command[1])
                elif user_command[0] == 's':
                    send_command = commands.MessageCommand(self.user_name, user_command[1], user_command[2])
                else:
                    send_command = commands.PresenceCommand(self.user_name, 'Online')

                self.socket.send(bytes(send_command))

                if user_command[0] == 'q':
                    sys.exit()

                raw_data = self.socket.recv(1024)
                print(raw_data)
                command = json.loads(raw_data.decode())
                if 'action' in command:
                    self.handler.handle(command)

    def authenticate(self):
        """ Аутентификация пользователя
            :return: True|False - в зависимости от успеха
        """
        while True:
            user_name = input('username: ')
            password = input('password: ')
            auth_command = commands.AuthenticateCommand(user_name, password)
            self.socket.send(bytes(auth_command))
            response = json.loads(self.socket.recv(1024).decode())
            success = response.get('response', 404) == '202'
            if success:
                self.user_name = user_name
                self.password = password
                break
        return success


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
