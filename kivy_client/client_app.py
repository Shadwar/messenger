import os
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivy_client.front import ChatScreen, LoginScreen, RegisterScreen
from kivy_client.client import Client


for file in os.listdir('kivy_client/front/ui'):
    if file.endswith('.kv'):
        Builder.load_file(os.path.join('kivy_client/front/ui', file))


class ClientApp(App):
    """ Класс, отвечающий за создание клиентского окна """
    def build(self):
        sm = ScreenManager()
        sm.client = Client(None, None)

        login_screen = LoginScreen(name='login')
        login_screen.register_handlers(sm.client)

        register_screen = RegisterScreen(name='register')
        register_screen.register_handlers(sm.client)

        chat_screen = ChatScreen(name='chat')
        chat_screen.register_handlers(sm.client)

        sm.add_widget(login_screen)
        sm.add_widget(register_screen)
        sm.add_widget(chat_screen)

        Clock.schedule_interval(sm.client.update, 1.0 / 10.0)

        return sm
