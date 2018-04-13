import abc


class MessageHandler(object):
    """ Обработчик команд """
    def __init__(self, engine):
        self.db_engine = engine

    @abc.abstractmethod
    def run(self, client, command, response):
        """ Обработка команды и возврат значения """
        pass
