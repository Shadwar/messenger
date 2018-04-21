from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    login_button = ObjectProperty(None)
    register_button = ObjectProperty(None)
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)

    def login_button_clicked(self, *args):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        if username and password:
            self.manager.client.authenticate(username, password)
