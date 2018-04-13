from .packet import Packet


class ChatJoinPacket(Packet):
    """ Пакет присоединения пользователя к чат-комнате """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'join',
            'room': room
        })
