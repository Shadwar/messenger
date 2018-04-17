from .packet import Packet


class AlertPacket(Packet):
    """ Пакет предупреждения от сервера на определенный запрос """
    def __init__(self, code, origin, message):
        super().__init__()
        if isinstance(message, list):
            self.data.update({
                'response': code,
                'origin': origin
            })
            for i, val in enumerate(message):
                self.data.update({
                    'alert_{}'.format(i): val
                })
        else:
            self.data.update({
                'response': code,
                'origin': origin,
                'alert': message
            })
