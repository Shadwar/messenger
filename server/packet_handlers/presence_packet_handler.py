from shared.packets import ResponsePacket
from .packet_handler import PacketHandler


class PresencePacketHandler(PacketHandler):
    """ Изменение статуса пользователя на сервере """
    def run(self, server, protocol, command):
        protocol.send_packet(ResponsePacket(200, command['id']))
