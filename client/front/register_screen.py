from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from .base_screen import BaseScreen


class RegisterScreen(BaseScreen):
    button_submit = ObjectProperty(None)

    def register_handlers(self, client):
        pass
