from client.message_handlers.message_handler import MessageHandler
from shared.messages import PresenceMessage


class ProbeHandler(MessageHandler):
    def run(self, client, command, response):
        presence = PresenceMessage(client.login, 'online')
        client.send_message(presence)
