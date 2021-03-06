class Chat(object):
    """ Чат """
    def __init__(self, title):
        self.title = title
        self.gid = None
        self.users = []

    def connect(self, user):
        """ Добавление нового пользователя в чат """
        self.users.append(user)

    def remove(self, user):
        """ Убирает пользователя из чата """
        self.users.remove(user)

    def send_message(self, message):
        """ Отправка сообщения в чат всем пользователям """
        for user in self.users:
            user.send_packet(message)
