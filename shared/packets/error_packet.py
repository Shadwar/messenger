from .packet import Packet


class ErrorPacket(Packet):
    """ Пакет ошибки от сервера на определенный запрос """
    def __init__(self, code, origin, message):
        super().__init__()
        self.data.update({
            'response': code,
            'origin': origin,
            'error': message
        })
