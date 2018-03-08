import socket
import json
import sys
import logging
import select
import queue
from time import sleep

from PyQt5.QtGui import QStandardItemModel

from client.message_handlers import *
from shared.responses import *
from shared.messages import *

logger = logging.getLogger('client')

class ClientCommandHandler(object):
    """ Обработчик команд, поступивших от сервера """
    def __init__(self, name, sock):
        self.name = name
        self.socket = sock

    def handle(self, command):
        """ Обработка команд """
        if command['action'] == 'probe':
            self.socket.send(bytes(PresenceMessage('ivan', "I'm here")))


class Client(object):
    """ Клиент мессенджера
    """
    def __init__(self, addr, port):
        self.signals = dict()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((addr, port))
        self.chats = {}
        self.contacts = None
        self.messages = dict()
        self.login = None
        self.handlers = {}
        self.init_handlers()
        self.recv_messages = queue.Queue()
        self.send_messages = queue.Queue()
        self.sended_messages = dict()
        self.message_id = 0

    def run(self):
        """ Запуск клиента, подключение к серверу, запуск цикла обработки сообщений
        """
        logger.info('Запуск клиента')
        while True:
            read_s, write_s, _ = select.select([self.socket], [self.socket], [], 0)

            if read_s:
                raw_data = self.socket.recv(1024)

                if not raw_data:
                    self.socket.close()
                    exit(0)
                else:
                    for command in self.parse_raw_received(raw_data.decode()):
                        self.recv_messages.put(command)

            if write_s:
                try:
                    message = self.send_messages.get_nowait()
                except queue.Empty:
                    pass
                else:
                    self.socket.send(bytes(message))

            self.handle()
            sleep(0.1)

    def handle(self):
        """ Обработка входящих сообщений """
        try:
            message = self.recv_messages.get_nowait()
        except queue.Empty:
            pass
        else:
            response = None
            if 'origin' in message:
                response = message
                message = json.loads(bytes(self.sended_messages[response['origin']]).decode())
                del self.sended_messages[response['origin']]
            action = message['action']
            if action in self.handlers:
                self.handlers[action]().run(self, message, response)

    def send_message(self, message):
        self.message_id += 1
        message.data['id'] = self.message_id
        self.sended_messages[self.message_id] = message
        self.send_messages.put(message)

    def init_handlers(self):
        self.handlers = dict({
            'authenticate': AuthenticateHandler,
            'add_contact': AddContactHandler,
            'contact_list': ContactHandler,
            'msg': TextMessageHandler,
        })
        pass

    def parse_raw_received(self, raw):
        """ Парсит входящий массив на отдельные команды"""
        commands = []
        index = 0
        curl = 0
        command = ""
        while index < len(raw):
            command += raw[index]
            if raw[index] == '{':
                curl += 1
            elif raw[index] == '}':
                curl -= 1
                if curl == 0:
                    commands.append(json.loads(command))
                    command = ""
            index += 1

        print(commands)
        return commands


    #     if self.authenticate():
    #         print('Command list:')
    #         print('c - create chat. (c chat_name)')
    #         print('j - join chat. (j chat_name)')
    #         print('l - leave chat. (l chat_name)')
    #         print('s - send message. (s receiver message)')
    #         print('q - quit from server. (q)')
    #         while True:
    #             user_command = input('next command (enter to pass): ').split()
    #             user_command.append(None)
    #
    #             if user_command[0] == 'q':
    #                 send_command = QuitMessage()
    #             elif user_command[0] == 'c':
    #                 if user_command[1][0] != '#':
    #                     user_command[1] = '#' + user_command[1]
    #                 send_command = ChatCreateMessage(user_command[1])
    #             elif user_command[0] == 'j':
    #                 send_command = ChatJoinMessage(user_command[1])
    #             elif user_command[0] == 'l':
    #                 send_command = ChatLeaveMessage(user_command[1])
    #             elif user_command[0] == 's':
    #                 send_command = TextMessage(self.user_name, user_command[1], user_command[2])
    #             else:
    #                 send_command = PresenceMessage(self.user_name, 'Online')
    #
    #             self.socket.send(bytes(send_command))
    #
    #             if user_command[0] == 'q':
    #                 sys.exit()
    #
    #             raw_data = self.socket.recv(1024)
    #             print(raw_data)
    #             command = json.loads(raw_data.decode())
    #             if 'action' in command:
    #                 self.handler.handle(command)
    #
    #
    # def authenticate(self):
    #     """ Аутентификация пользователя
    #         :return: True|False - в зависимости от успеха
    #     """
    #     while True:
    #         user_name = input('username: ')
    #         password = input('password: ')
    #         auth_command = AuthenticateMessage(user_name, password)
    #         self.socket.send(bytes(auth_command))
    #         response = json.loads(self.socket.recv(1024).decode())
    #         success = response.get('response', 402) == 202
    #         print(response)
    #         if success:
    #             self.user_name = user_name
    #             self.password = password
    #             break
    #     return success
