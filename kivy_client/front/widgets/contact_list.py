import os

from kivy.factory import Factory
from kivy.properties import ObjectProperty, Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from .contact import Contact
from kivy_client.client import Client


class ContactList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)
    create_chat = ObjectProperty(None)
    find_user = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Client()
        Clock.schedule_once(self.init_buttons, 0)

    def add_item(self, login, avatar=None):
        contact = Contact(avatar=avatar, text=login)
        contact.on_press = self.on_press_contact(contact)
        self.ids.container.add_widget(contact)

    def on_press_contact(self, contact):
        client = Client()

        def inner():
            client.send_event({'action': 'ui_contact_clicked', 'contact': contact.text.strip()})
        return inner

    def init_buttons(self, dt):
        create_chat_popup = Factory.CreateChat()

        def create_chat():
            name = create_chat_popup.ids.chat_name_input.text
            if name:
                if not name.startswith('#'):
                    name = '#' + name
                self.client.send_event({'action': 'chat_create', 'room': name})
                create_chat_popup.dismiss()
            pass
        create_chat_popup.ids.submit_button.on_release = create_chat

        self.ids.create_chat.on_press = create_chat_popup.open
