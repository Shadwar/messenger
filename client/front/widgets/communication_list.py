from kivy.properties import ObjectProperty, Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

from client.front.widgets.message import Message


class CommunicationList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)

    def add_item(self, message, is_user=False):
        sender = message['u_from']
        text = message['message']

        message = Message(text=sender + ':\n' + text, is_user=is_user)
        message.bind(texture_size=message.setter('size'))
        self.ids.container.add_widget(message)

    def clear(self):
        self.ids.container.clear_widgets()
