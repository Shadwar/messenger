from .packet import Packet


class FindContactsPacket(Packet):
    """ Пакет поиска контактов на сервере """
    def __init__(self, name):
        super().__init__()
        self.data.update({
            'action': 'find_contacts',
            'name': name
        })
