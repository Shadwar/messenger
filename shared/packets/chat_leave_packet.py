from .packet import Packet


class ChatLeavePacket(Packet):
    """ Пакет отключения пользователя от чат-комнаты """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'chat_leave',
            'room': room
        })
