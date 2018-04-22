from .packet import Packet


class FoundContactPacket(Packet):
    """ Пакет с найденным контактом """
    def __init__(self, name):
        super().__init__()
        self.data.update({
            'action': 'found_contact',
            'name': name
        })
