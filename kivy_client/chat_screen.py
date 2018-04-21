from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from .contact import Contact
from .contact_list import ContactList
from .user_info import UserInfo


class ChatScreen(Screen):
    user_info = ObjectProperty(None)
    contact_list = ObjectProperty(None)
    # contact_chat = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.ids.user_info.text = 'shadwar'.ljust(16)
        print(self.ids)
        super().on_pre_enter(*args)




