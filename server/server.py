import asyncio
import json

from sqlalchemy import create_engine

from server.packet_handlers import *
from shared.packets import WelcomePacket


class Server(object):
    """ Сервер мессенджера """
    clients = []
    logged_users = dict()
    handlers = None
    db_engine = None

    class ServerProtocol(asyncio.Protocol):
        """ Класс протокола взаимодействия с клиентом """
        class User(object):
            def __init__(self):
                self.gid = None
                self.login = None
                self.public_key = None
                self.protocol = None

        def connection_made(self, transport):
            self.transport = transport
            self.peername = transport.get_extra_info("peername")
            self.user = None
            print("Соединение создано: {}".format(self.peername))
            Server.clients.append(self)
            self.send_packet(WelcomePacket())

        def data_received(self, data):
            decoded = Server.parse_raw_received(data.decode())
            print("data_received: {}".format(decoded))
            for command in decoded:
                Server.handle_command(self, command)

        def connection_lost(self, exc):
            print("Соединение разорвано: {}".format(self.peername))
            self.transport = None
            Server.remove_user(self)

        def send_packet(self, packet):
            """ Отправка пакета пользователю """
            self.transport.write(bytes(packet))

    def __init__(self, ip, port):
        Server.init_handlers()
        Server.db_engine = create_engine('sqlite:///server.db')

        self.loop = asyncio.get_event_loop()
        server_coro = self.loop.create_server(self.ServerProtocol, host=ip , port=port)
        server = self.loop.run_until_complete(server_coro)

        for sock in server.sockets:
            print("serving on {}".format(sock.getsockname()))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print('Сервер остановлен')
        server.close()
        self.loop.run_until_complete(server.wait_closed())
        self.loop.close()

    @staticmethod
    def parse_raw_received(raw):
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
        return commands

    @staticmethod
    def init_handlers():
        Server.handlers = dict({
            'authenticate': AuthenticatePacketHandler,
            'add_contact': AddContactPacketHandler,
            'chat_create': ChatCreatePacketHandler,
            'chat_join': ChatJoinPacketHandler,
            'chat_leave': ChatLeavePacketHandler,
            'del_contact': DelContactPacketHandler,
            'get_contacts': GetContactsPacketHandler,
            'get_messages': GetMessagesPacketHandler,
            'message': MessagePacketHandler,
            'presence': PresencePacketHandler,
            'quit': QuitPacketHandler
        })

    @staticmethod
    def handle_command(protocol, command):
        action = command['action']
        Server.handlers[action](Server.db_engine).run(Server, protocol, command)

    @staticmethod
    def remove_user(protocol):
        Server.clients.remove(protocol)
        Server.logged_users.pop(protocol.user.login)
