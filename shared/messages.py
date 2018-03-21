import time
from shared.jim import JIM


class Message(JIM):
    def __init__(self):
        super().__init__()
        self.data['time'] = int(time.time())


class ProbeMessage(Message):
    """ Запрос сервера о доступности клиента """
    def __init__(self):
        super().__init__()
        self.data['action'] = 'probe'


class WelcomeMessage(Message):
    def __init__(self):
        super().__init__()
        self.data['action'] = 'welcome'


class AuthenticateMessage(Message):
    """ Запрос пользователя об аутентификации """
    def __init__(self, login, password, public_key):
        super().__init__()
        self.data.update({
            'action': 'authenticate',
            'user': {
                'account_name': login,
                'password': password,
                'public_key': public_key
            }
        })


class QuitMessage(Message):
    """ Отключение клиента от сервера """
    def __init__(self):
        super().__init__()
        self.data['action'] = 'quit'


class PresenceMessage(Message):
    """ Ответ клиента о присутствии на сервере """
    def __init__(self, login, status):
        super().__init__()
        self.data.update({
            'action': 'presence',
            'user': {
                'account_name': login,
                'status': status
            }
        })


class TextMessage(Message):
    """ Сообщение отдельному пользователю или в указанный чат """
    def __init__(self, sender, receiver, message):
        super().__init__()
        self.data.update({
            'action': 'msg',
            'to': receiver,
            'from': sender,
            'message': message
        })


class ChatJoinMessage(Message):
    """ Команда присоединения к чату """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'join',
            'room': room
        })


class ChatLeaveMessage(Message):
    """  Команда покинуть чат """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'leave',
            'room': room
        })


class ChatCreateMessage(Message):
    """  Команда покинуть чат """
    def __init__(self, room):
        super().__init__()
        self.data.update({
            'action': 'create',
            'room': room
        })


class GetContactsMessage(Message):
    """ Запрос на контакты от сервера """
    def __init__(self):
        super().__init__()
        self.data['action'] = 'get_contacts'


class ContactMessage(Message):
    """ Контакт пользователя """
    def __init__(self, login, public_key):
        super().__init__()
        self.data.update({
            'action': 'contact_list',
            'contact': login,
            'public_key': public_key
        })


class AddContactMessage(Message):
    """ Добавление контакта в список контактов пользователя """
    def __init__(self, login, public_key):
        super().__init__()
        self.data.update({
            'action': 'add_contact',
            'contact': login,
            'public_key': public_key
        })


class DelContactMessage(Message):
    """ Удаление контакта в список контактов пользователя """
    def __init__(self, login):
        super().__init__()
        self.data.update({
            'action': 'del_contact',
            'contact': login
        })


class GetTextMessages(Message):
    """ Получение сообщений определенного пользователя """
    def __init__(self, contact):
        super().__init__()
        self.data.update({
            'action': 'get_messages',
            'contact': contact
        })
