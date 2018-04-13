from .packet import Packet


class AlertPacket(Packet):
    """ Пакет предупреждения от сервера на определенный запрос """
    def __init__(self, code, origin, message):
        super().__init__()
        self.data.update({
            'response': code,
            'origin': origin,
            'alert': message
        })
