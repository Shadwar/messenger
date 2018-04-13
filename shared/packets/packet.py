import time
import json


class Packet(object):
    """ Класс пакета информации для передачи между сервером и клиентом"""
    def __init__(self):
        self.data = dict()
        self.data.update({ 'time': int(time.time())})

    def __bytes__(self):
        return json.dumps(self.data).encode()
