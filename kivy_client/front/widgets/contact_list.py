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
        Clock.schedule_once(self.init_create_chat_button, 0)
        Clock.schedule_once(self.init_find_user_button, 0)

    def add_item(self, login, avatar=None):
        contact = Contact(avatar=avatar, text=login)
        contact.on_press = self.on_press_contact(contact)
        self.ids.container.add_widget(contact)

    def on_press_contact(self, contact):
        def inner():
            self.client.send_event({'action': 'ui_contact_clicked', 'contact': contact.text.strip()})
        return inner

    def init_create_chat_button(self, dt):
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

    def init_find_user_button(self, dt):
        find_user_popup = Factory.FindUser()

        def find_user():
            name = find_user_popup.ids.contact_name.text
            if name:
                find_user_popup.ids.container.clear_widgets()
                self.client.send_event({'action': 'find_contacts', 'name': name})

        def contact_pressed(name):
            def inner():
                if name.startswith('#'):
                    self.client.send_event({'action': 'chat_join', 'room': name})
                else:
                    self.client.send_event({'action': 'add_contact', 'contact': name})
            return inner

        def found_contact(command, response):
            contact = Contact(avatar=None, text=command['name'])
            contact.on_release = contact_pressed(command['name'])
            find_user_popup.ids.container.add_widget(contact)

        find_user_popup.ids.find_contact.on_release = find_user
        find_user_popup.ids.submit_button.on_release = find_user_popup.dismiss

        self.ids.find_user.on_release = find_user_popup.open
        self.client.ui_handlers['ui_found_contact'] = found_contact
