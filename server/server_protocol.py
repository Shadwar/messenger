import asyncio

from shared.packets import WelcomePacket


class ServerProtocol(asyncio.Protocol):
    """ Класс протокола взаимодействия с клиентом """

    def connection_made(self, transport):
        from server.server import Server
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        self.user = None
        print("Соединение создано: {}".format(self.peername))
        Server.clients.append(self)
        self.send_packet(WelcomePacket())

    def data_received(self, data):
        from server.server import Server
        decoded = Server.parse_raw_received(data.decode())
        print("Получены данные: {}".format(decoded))
        for command in decoded:
            Server.handle_command(self, command)

    def connection_lost(self, exc):
        from server.server import Server
        print("Соединение разорвано: {}".format(self.peername))
        self.transport = None
        Server.remove_user(self)

    def send_packet(self, packet):
        """ Отправка пакета пользователю """
        self.transport.write(bytes(packet))
