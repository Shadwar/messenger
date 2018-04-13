from .packet import Packet


class ChatLeavePacket(Packet):
    """ Пакет отключения пользователя от чат-комнаты """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'leave',
            'room': room
        })
