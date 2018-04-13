from .packet import Packet


class ResponsePacket(Packet):
    """ Пакет ответа сервера на определенный запрос """
    def __init__(self, code, origin):
        super().__init__()
        self.data.update({
            'response': code,
            'origin': origin,
        })
