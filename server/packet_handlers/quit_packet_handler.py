from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class QuitPacketHandler(PacketHandler):
    """ Отключение пользователя от сервера """
    def run(self, server, protocol, command):
        protocol.send_packet(ResponsePacket(200, command['id']))
        server.remove_user(protocol)
