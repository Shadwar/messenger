import unittest
from unittest.mock import Mock
import json
import shared.commands as commands
import client.client as client


class TestClient(unittest.TestCase):
    pass


class TestHandlers(unittest.TestCase):

    def setUp(self):
        self.server_sock = Mock()
        self.server_sock.send.return_value = None
        self.handler = client.ClientCommandHandler('ivan', self.server_sock)

    def test_probe_return_presence(self):
        """ На probe запрос от сервера должен возвращаться presence ответ """
        command = commands.ProbeCommand()
        self.handler.handle(json.loads(str(command)))
        self.assertTrue('presence'.encode() in self.server_sock.send.call_args[0][0])
