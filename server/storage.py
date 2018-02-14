import abc


class Storage(object):
    """ Хранилище данных """

    @abc.abstractmethod
    def add(self, table, key, data):
        """ Добавить данные в таблицу """
        pass

    def get(self, table, key):
        """ TODO: Вернуть данные из таблицы """
        return None

    def remove(self, table, key):
        """ TODO: Удалить данные из таблицы """
        pass
