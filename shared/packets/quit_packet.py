from .packet import Packet


class QuitPacket(Packet):
    """ Пакет отключения клиента от сервера """
    def __init__(self):
        super().__init__()
        self.data.update({
            'action': 'quit'
        })
