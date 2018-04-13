from .packet import Packet


class AddContactPacket(Packet):
    """ Пакет добавления нового контакта пользователем """
    def __init__(self, login):
        super().__init__()
        self.data.update({
            'action': 'add_contact',
            'contact': login
        })
