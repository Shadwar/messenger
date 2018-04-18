from .packet import Packet


class ChatContactPacket(Packet):
    """ Пакет с контактом чата, передаваемый сервером """
    def __init__(self, name):
        super().__init__()
        self.data.update({
            'action': 'chat_contact',
            'room': name
        })
