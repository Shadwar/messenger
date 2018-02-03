import socket
import sys
import select
import queue

import commands


class ServerCommandHandler(object):
    """ Серверный обработчик команд, поступающих от клиента """
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
        user.send(result)

    def quit(self, user):
        """ Выход пользователя с сервера """
        self.users.remove(user)
        user.send(bytes(commands.Response(200)))
        user.close()

    def presence(self, command, user):
        """ Подтверждение нахождения пользователя на сервере """
        user.send(bytes(commands.Response(200)))


class Server(object):
    """ Сервер мессенджера
    """
    def __init__(self, ip, port):
        self.socket = Server.create_socket(ip, port)
        self.users = []
        self.message_queue = {}
        self.handler = ServerCommandHandler(self.users)

    def run(self):
        """ Запуск сервера
        """

        while True:
            self.accept_users()

            read_sockets, write_sockets, exc_sockets = select.select(self.users, self.users, self.users, 0)

            for sock in read_sockets:
                self.handle_read_socket(sock)

            for sock in write_sockets:
                self.handle_write_socket(sock)

            for sock in exc_sockets:
                self.handle_exception_socket(sock)

    def accept_users(self):
        """ Подключение нового пользователя к серверу
        """
        try:
            user, _ = self.socket.accept()
            user.setblocking(False)
            self.message_queue[user] = queue.Queue()
            self.users.append(user)
        except socket.timeout:
            pass

    def handle_read_socket(self, sock):
        """ Обработка сокетов на чтение """
        raw_data = sock.recv(1024)

        # Если возвращено 0 байт, значит пользователь отключился
        if not raw_data:
            sock.close()
            self.users.remove(sock)
            del self.message_queue[sock]
        else:
            # Обработать сообщение и добавить ответ
            self.message_queue[sock].put(raw_data)

    def handle_write_socket(self, sock):
        """ Обработка сокетов на запись """
        try:
            message = self.message_queue[sock].get_nowait()
            sock.send(message)
        except queue.Empty:
            pass

    def handle_exception_socket(self, sock):
        """ Обработка сокетов вызывавших исключение """
        pass

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
