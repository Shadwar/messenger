from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from .widgets import ContactList, UserInfo, CommunicationList, CommunicationInput


class ChatScreen(Screen):
    user_info = ObjectProperty(None)
    contact_list = ObjectProperty(None)
    communication_list = ObjectProperty(None)
    communication_input = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.ids.user_info.text = 'shadwar'.ljust(16)

        for i in range(30):
            self.ids.contact_list.add_item('button-{}'.format(i))

        for i in range(50):
            self.ids.communication_list.add_item('message-{}'.format(i), i % 3 == 0)

        print(self.ids)
        super().on_pre_enter(*args)




