from .packet import Packet


class ContactPacket(Packet):
    """ Пакет с контактом пользователя, передаваемый сервером """
    def __init__(self, login, public_key):
        super().__init__()
        self.data.update({
            'action': 'contact',
            'contact': login,
            'public_key': public_key
        })
