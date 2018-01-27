import unittest

import json
import server
import commands

class TestServer(unittest.TestCase):
    pass


class TestHandlers(unittest.TestCase):

    def test_authenticate_returns_202(self):
        """ Обработчик аутентификации возвращает респонс с 202 кодом  """
        command = commands.AuthenticateCommand('ivan', 'vlado12')
        expected = json.dumps({"response": "202"}).encode()

        result = server.AuthenticateHandler.handle(command)
        self.assertEqual(result, expected)

    def test_quit_return_200(self):
        """ Обработчик выхода возвращает респонс с 200 кодом - выход успешен """
        command = commands.QuitCommand()
        expected = json.dumps({"response": "200"}).encode()

        result = server.QuitHandler.handle(command)
        self.assertEqual(result, expected)

    def test_presence_return_200(self):
        """ Сообщение от пользователя о его нахождении на сервере - должен вернуться код 200 - успешно """
        command = commands.PresenceCommand('ivan', "I'm here")
        expected = json.dumps({"response": "200"}).encode()

        result = server.PresenceHandler.handle(command)
        self.assertEqual(result, expected)
