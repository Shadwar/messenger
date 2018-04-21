import abc

from kivy.uix.screenmanager import Screen


class BaseScreen(Screen):
    """ Базовый класс экрана """

    @abc.abstractmethod
    def register_handlers(self, client):
        """
        Регистрация обработчиков событий

        :param client: Client
        :return:
        """
        pass
