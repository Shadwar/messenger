import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from kivy_client.chat_screen import ChatScreen
from kivy_client.login_screen import LoginScreen
from kivy_client.register_screen import RegisterScreen


for file in os.listdir('kivy_client/ui'):
    if file.endswith('.kv'):
        Builder.load_file(os.path.join('kivy_client/ui', file))


class ClientApp(App):
    """ Класс, отвечающий за создание клиентского окна """
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ChatScreen(name='chat'))

        sm.current = 'chat'
        scr = sm.get_screen('chat')
        for i in range(3):
            scr.ids.contact_list.add_item('button-{}'.format(i))


        return sm
