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
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ChatScreen(name='chat'))

        sm.client = Client(None, None)
        Clock.schedule_interval(sm.client.update, 1.0 / 10.0)
        self.sm = sm

        return sm
