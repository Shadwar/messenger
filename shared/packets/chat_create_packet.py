from .packet import Packet


class ChatCreatePacket(Packet):
    """ Пакет создания новой чат-комнаты пользователем """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'chat_create',
            'room': room
        })
