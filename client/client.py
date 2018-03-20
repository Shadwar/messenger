import socket
import json
import sys
import logging
import select
import queue
import threading
from time import sleep

from PyQt5.QtGui import QStandardItemModel

from client.message_handlers import *
from shared.responses import *
from shared.messages import *

logger = logging.getLogger('client')

client_sended_messages_lock = threading.Lock()


def handle_commands(client, recv_messages, sended_messages):
    """ Обработка входящих команд """
    global client_sended_messages_lock

    while True:
        try:
            message = recv_messages.get()
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break
        else:
            response = None
            if 'origin' in message:
                response = message

                client_sended_messages_lock.acquire(blocking=True)
                message = json.loads(bytes(sended_messages[response['origin']]).decode())
                del sended_messages[response['origin']]
                client_sended_messages_lock.release()

            action = message['action']
            if action in client.handlers:
                client.handlers[action]().run(client, message, response)
        sleep(0.1)


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

        threading.Thread(target=handle_commands, args=(self, self.recv_messages, self.sended_messages)).start()

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

            sleep(0.1)

    def handle(self):
        """ Обработка входящих сообщений """

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
