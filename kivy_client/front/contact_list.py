import os
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from .contact import Contact


class ContactList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)
    user_info = ObjectProperty(None)

    def add_item(self, login, avatar='no_user_avatar.png'):
        contact = Contact(avatar=avatar, text=login)
        self.ids.container.add_widget(contact)
