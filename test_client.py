import unittest
import json
import commands
import client


class TestClient(unittest.TestCase):
    pass


class TestHandlers(unittest.TestCase):

    def test_probe_return_presence(self):
        """ На probe запрос от сервера должен возвращаться presence ответ """
        command = commands.ProbeCommand()
        result = client.ProbeHandler.handle(command)

        self.assertTrue('presence' in result.decode())
