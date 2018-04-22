from kivy.properties import ObjectProperty

from .base_screen import BaseScreen
from .widgets import ContactList, UserInfo, CommunicationList, CommunicationInput


class ChatScreen(BaseScreen):
    user_info = ObjectProperty(None)
    contact_list = ObjectProperty(None)
    communication_list = ObjectProperty(None)
    communication_input = ObjectProperty(None)

    def register_handlers(self, client):
        client.ui_handlers['ui_add_contact'] = self.add_contact_handler
        client.ui_handlers['ui_add_message'] = self.add_message_handler
        client.ui_handlers['ui_user_clicked'] = self.user_clicked_handler
        client.ui_handlers['ui_contact_clicked'] = self.contact_clicked_handler
        client.ui_handlers['ui_send_message_clicked'] = self.send_message_clicked

    def on_pre_enter(self, *args):
        self.ids.user_info.text = 'shadwar'.ljust(16)

        for contact in self.manager.client.contacts:
            self.ids.contact_list.add_item(contact)

        super().on_pre_enter(*args)

    def add_contact_handler(self, command, response):
        """ При добавлении нового контакта, он добавляется в список контактов"""
        self.ids.contact_list.add_item(command['contact'])

    def add_message_handler(self, command, response):
        """ При добавлении нового сообщения, оно добавляется в список сообщений """
        self.ids.communication_list.add_item(command, command['u_from'] == self.manager.client.login)

    def user_clicked_handler(self, command, response):
        """ TODO: Показать новое окно, смены пароля и аватара """
        print(command)
        pass

    def contact_clicked_handler(self, command, response):
        """ При выборе контакта очищается список сообщений и добавляются сообщения данного котакта """
        contact = command['contact']
        self.ids.communication_list.clear()

        self.manager.client.current_contact = contact

        for message in self.manager.client.messages[contact]:
            self.ids.communication_list.add_item(message, message['u_from'] == self.manager.client.login)

    def send_message_clicked(self, command, response):
        """ При нажатии на кнопку отправки сообщения, проверить текущий контакт и отправить событие бэкэнду """
        if self.manager.client.current_contact:
            self.manager.client.send_event({
                'action': 'send_message',
                'contact': self.manager.client.current_contact,
                'message': command['message']
            })
