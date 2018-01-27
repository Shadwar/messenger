import json
import time

# Коды ошибок:
# 1xx​- информационные сообщения:
#   100​- базовое уведомление;
#   101​- важное уведомление.
# 2xx​- успешное завершение:
#   200​- OK;
#   201​(created) - объект создан;
#   202​(accepted)- подтверждение.
# 4xx​- ошибка на стороне клиента:
#   400​- неправильный запрос/JSON-объект;
#   401​- не авторизован;
#   402​- неправильный логин/пароль;
#   403​(forbidden) - пользователь заблокирован;
#   404​(not found) - пользователь/чат отсутствует на сервере;
#   409​(conflict) - уже имеется подключение с указанным логином;
#   410​(gone) - адресат существует, но недоступен (offline).
# 5xx​- ошибка на стороне сервера:
#   500​- ошибка сервера.


class Command(object):
    pass

    def __bytes__(self):
        return self.__str__().encode()


class Response(Command):
    pass


class AlertResponse(Response):
    """ Ответ сервера о сообщении/уведомлении
    {
      "response": 1xx / 2xx,
      "time": <unix timestamp>,
      "alert": "message (optional for 2xx codes)"
    }
    """
    def __init__(self, code, message=''):
        self.code = code
        self.message = message

    def __str__(self):
        command = {
            'response': self.code,
            'time': int(time.time()),
            'alert': self.message
        }
        return json.dumps(command)


class ErrorResponse(Response):
    """ Ответ сервера об ошибке
    {
       "response": 4xx / 5xx,
       "time": <unix timestamp>,
       "error": "error message (optional)"
    }
    """
    def __init__(self, code, message=''):
        self.code = code
        self.message = message

    def __str__(self):
        command = {
            'response': self.code,
            'time': int(time.time()),
            'error': self.message
        }
        return json.dumps(command)


class ProbeCommand(Command):
    """ Запрос сервероа о доступности клиента
    {
        "action": "probe",
        "time": <unix timestamp>,
    }
    """
    action = 'probe'

    def __str__(self):
        command = {
            'action': ProbeCommand.action,
            'time': int(time.time())
        }
        return json.dumps(command)


class AuthenticateCommand(Command):
    """ Запрос пользователя об аутентификации
    {
       "action": "authenticate",
       "time": <unix timestamp>,
       "user": {
           "account_name": "C0deMaver1ck",
           "password": "CorrectHorseBatterStaple"
       }
    }
    """
    action = 'authenticate'

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def __str__(self):
        command = {
            'action': AuthenticateCommand.action,
            'time': int(time.time()),
            'user': {
                'account_name': self.account,
                'password': self.password
            }
        }
        return json.dumps(command)


class QuitCommand(Command):
    """ Отключение клиента от сервера
    {
       "action": "quit"
    }
    """
    action = "quit"

    def __str__(self):
        command = {
            'action': QuitCommand.action
        }
        return json.dumps(command)


class PresenceCommand(Command):
    """ Ответ пользователя о присутствии на сервере
    {
       "action": "presence",
       "time": <unix timestamp>,
       "type": "status",
       "user": {
           "account_name": "C0deMaver1ck",
           "status": "Yep, I am here!"
       }
    }
    """
    action = "presence"
    type = "status"

    def __init__(self, account, status):
        self.account = account
        self.status = status

    def __str__(self):
        command = {
            'action': PresenceCommand.action,
            'time': int(time.time()),
            'type': PresenceCommand.type,
            'user': {
                'account_name': self.account,
                'status': self.status
            }
        }

        return json.dumps(command)


class MessageCommand(Command):
    """ Сообщение отдельному пользователю или в указанный чат
    {
       "action": "msg",
       "time": <unix timestamp>,
       "to": "account_name",
       "from": "account_name",
       "encoding": "ascii",
       "message": "message"
    }
    """
    action = 'msg'

    def __init__(self, sender, receiver, message, encoding='ascii'):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.encoding = encoding

    def __str__(self):
        command = {
            'action': self.__class__.action,
            'time': int(time.time()),
            'to': self.receiver,
            'from': self.sender,
            'encoding': self.encoding,
            'message': self.message
        }
        return json.dumps(command)


class ChatJoinCommand(Command):
    """ Команда присоединения к чату
    {
        "action": "join",
        "time": <unix timestamp>,
        "room": "#room_name"
    }
    """
    action = 'join'

    def __init__(self, room):
        self.room = room

    def __str__(self):
        command = {
            'action': self.__class__.action,
            'time': int(time.time()),
            'room': self.room
        }
        return json.dumps(command)


class ChatLeaveCommand(Command):
    """ Команда покинуть чат
    {
        "action": "leave",
        "time": <unix timestamp>,
        "room": "#room_name"
    }
    """
    action = 'leave'

    def __init__(self, room):
        self.room = room

    def __str__(self):
        command = {
            'action': self.__class__.action,
            'time': int(time.time()),
            'room': self.room
        }
        return json.dumps(command)