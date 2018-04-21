import os
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from .contact import Contact
from kivy_client.client import Client


class ContactList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)
    user_info = ObjectProperty(None)

    def add_item(self, login, avatar='no_user_avatar.png'):
        contact = Contact(avatar=avatar, text=login)
        contact.on_press = self.on_press_contact(contact)
        self.ids.container.add_widget(contact)

    def on_press_contact(self, contact):
        client = Client()

        def inner():
            client.send_event({'action': 'ui_contact_clicked', 'contact': contact.text.strip()})
        return inner
