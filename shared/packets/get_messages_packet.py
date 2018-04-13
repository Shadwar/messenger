from .packet import Packet


class GetMessagesPacket(Packet):
    """ Пакет запроса сообщений от определенного контакта пользователя """
    def __init__(self, contact):
        super().__init__()
        self.data.update({
            'action': 'get_messages',
            'contact': contact
        })
