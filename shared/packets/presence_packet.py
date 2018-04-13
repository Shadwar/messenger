from .packet import Packet


class PresencePacket(Packet):
    """ Пакет со статусом пользователя, передаваемый серверу """
    def __init__(self, login, status):
        super().__init__()
        self.data.update({
            'action': 'presence',
            'account_name': login,
            'status': status
        })
