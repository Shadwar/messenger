from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView

from kivy_client.front.widgets.message import Message


class CommunicationList(ScrollView):
    """ Список контактов """
    container = ObjectProperty(None)

    def add_item(self, message, is_user=False):
        sender = message['u_from']
        text = message['message']

        contact = Message(text=sender + ':\n' + text, is_user=is_user)
        contact.bind(texture_size=contact.setter('size'))
        self.ids.container.add_widget(contact)

    def clear(self):
        self.ids.container.clear_widgets()
