from client.message_handlers.message_handler import MessageHandler
from shared.packets import PresencePacket


class ProbeHandler(MessageHandler):
    def run(self, client, command, response):
        presence = PresencePacket(client.login, 'online')
        client.send_message(presence)
