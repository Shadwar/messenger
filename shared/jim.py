import json


class JIM(object):
    """ JIM Сообщение между сервером и клиентом """
    def __init__(self):
        self.data = dict()

    def __bytes__(self):
        print(self.data)
        return json.dumps(self.data).encode()
