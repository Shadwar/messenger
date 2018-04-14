import abc


class PacketHandler(object):
    """ Обработчик входящих пакетов """
    def __init__(self, db_engine):
        self.db_engine = db_engine

    @abc.abstractmethod
    def run(self, client, command, response):
        """ Обработка входящего пакета и возврат значения """
        pass
