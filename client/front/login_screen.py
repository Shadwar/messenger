from kivy.properties import ObjectProperty

from .base_screen import BaseScreen
from client.client import Client


class LoginScreen(BaseScreen):
    login_button = ObjectProperty(None)
    register_button = ObjectProperty(None)
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def login_button_clicked(self, *args):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        if username and password:
            self.manager.client.send_event({
                'action': 'authenticate_user',
                'login': username,
                'password': password,
                'client': self.manager.client
            })

    def register_handlers(self, client):
        client.ui_handlers['ui_login_error'] = self.login_error_handler
        client.ui_handlers['ui_login_ok'] = self.login_ok_handler

    def login_error_handler(self, command, response):
        pass

    def login_ok_handler(self, command, response):
        self.manager.current = 'chat'
