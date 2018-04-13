from .packet import Packet


class WelcomePacket(Packet):
    """ Пакет приветствия, которое отсылает сервер клиенту при подключении """
    def __init__(self):
        super().__init__()
        self.data.update({
            'action': 'welcome'
        })
