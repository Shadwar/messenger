from .packet import Packet


class DelContactPacket(Packet):
    """ Пакет удаления контакта из списка контактов пользователя """
    def __init__(self, login):
        super().__init__()
        self.data.update({
            'action': 'del_contact',
            'contact': login
        })
