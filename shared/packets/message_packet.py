from .packet import Packet


class MessagePacket(Packet):
    """ Пакет текстового сообщения """
    def __init__(self, sender, receiver, message):
        super().__init__()
        self.data.update({
            'action': 'message',
            'from': sender,
            'to': receiver,
            'message': message
        })
