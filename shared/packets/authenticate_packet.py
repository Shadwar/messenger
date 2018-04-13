from .packet import Packet


class AuthenticatePacket(Packet):
    """ Пакет аутентификации, отправляемый клиентом серверу """
    def __init__(self, login, password, public_key):
        super().__init__()
        self.data.update({
            'action': 'authenticate',
            'account_name': login,
            'password': password,
            'public_key': public_key
        })
