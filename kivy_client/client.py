import socket
import json
import logging
import select
import queue

from sqlalchemy import create_engine
from collections import defaultdict

from kivy_client.back import UserInfo, CommunicationList, ContactList
from shared.lib import Singleton

logger = logging.getLogger('client')


class Client(object, metaclass=Singleton):
    """ Клиент мессенджера
    """
    def __init__(self, addr=None, port=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((addr, port))
        self.socket.setblocking(False)
        self.db_engine = create_engine('sqlite:///client.db')
        self.chats = {}

        self.contacts = []
        self.messages = defaultdict(list)
        self.current_contact = ''

        self.login = None
        self.handlers = dict()
        self.ui_handlers = dict()
        self.init_handlers()
        self.recv_messages = queue.Queue()
        self.send_messages = queue.Queue()
        self.sended_messages = dict()
        self.message_id = 0
        self.public_key = None
        self.private_key = None

    def update(self, dt):
        read_s, write_s, _ = select.select([self.socket], [self.socket], [], 0)

        if read_s:
            fragments = []
            while True:
                try:
                    chunk = self.socket.recv(2048)
                except:
                    break
                fragments.append(chunk)

            raw_data = b"".join(fragments)

            if not raw_data:
                self.socket.close()
                exit(0)
            else:
                for command in self.parse_raw_received(raw_data.decode()):
                    self.send_event(command)

        if write_s:
            while not self.send_messages.empty():
                try:
                    message = self.send_messages.get_nowait()
                except queue.Empty:
                    pass
                else:
                    self.socket.send(bytes(message))

        try:
            message = self.recv_messages.get_nowait()
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            pass
        else:
            response = None
            if 'origin' in message:
                response = message

                message = json.loads(bytes(self.sended_messages[response['origin']]).decode())
                del self.sended_messages[response['origin']]

            action = message['action']
            if action in self.handlers:
                self.handlers[action](message, response)
            if action in self.ui_handlers:
                self.ui_handlers[action](message, response)

    def send_message(self, message):
        self.message_id += 1
        message.data['id'] = self.message_id
        self.sended_messages[self.message_id] = message
        self.send_messages.put(message)

    def init_handlers(self):
        ContactList(self)
        UserInfo(self)
        CommunicationList(self)

    def send_event(self, event):
        self.recv_messages.put(event)

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

        # print(commands)
        return commands

    def authenticate(self, login, password):
        """ Создание нового аккаунта и ключей шифрования """
        self.send_event({'action': 'authenticate_user', 'login': login, 'password': password, 'client': self})

    def send_text_message(self, contact, message):
        """ Отправка и шифрование текстового сообщения """
        self.send_event({'action': 'send_message_to_server', 'contact': contact, 'message': message})

    def save_avatar(self, filename):
        """ Сохранение аватара пользователя в базу данных """
        self.send_event({'action': 'save_avatar', 'filename': filename})

    def load_user_avatar(self, container):
        """ Установка аватара пользователя, если он есть в базе данных """
        self.send_event({'action': 'load_avatar', 'container': container})
