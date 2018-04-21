from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from kivy_client.message import Message


class CommunicationList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)

    def add_item(self, text, is_user=False):
        contact = Message(text=text, is_user=is_user)
        contact.bind(texture_size=contact.setter('size'))
        self.ids.container.add_widget(contact)
