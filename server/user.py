import queue


class User(object):
    """ Пользователь """
    def __init__(self, sock):
        self.sock = sock
        self.recv_messages = queue.Queue()
        self.send_messages = queue.Queue()
        self.name = None

    def send_message(self, message):
        """ Добавить пользователю сообщение на отправку """
        self.send_messages.put(message)

    def recv_message(self, message):
        """ Добавить пользователю полученное сообщение"""
        self.recv_messages.put(message)