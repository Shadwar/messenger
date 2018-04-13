from .packet import Packet


class GetContactsPacket(Packet):
    """ Пакет запроса списка контактов у сервера """
    def __init__(self):
        super().__init__()
        self.data.update({
            'action': 'get_contacts'
        })
