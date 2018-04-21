from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from kivy_client.contact import Contact


class ContactList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)

    def add_item(self, login, avatar):
        contact = Contact(avatar=avatar, text=login)
        self.ids.container.add_widget(contact)
