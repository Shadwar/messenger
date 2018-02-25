from shared.jim import JIM


class Response(JIM):
    """ Ответ сервера """
    def __init__(self, code, origin):
        super().__init__()
        self.data['response'] = code
        self.data['origin'] = origin

    def __eq__(self, other):
        return self.data == other.data


class AlertResponse(Response):
    """ Ответ сервера о сообщении/уведомлении """
    def __init__(self, code, origin, message):
        super().__init__(code, origin)
        self.data['alert'] = message


class ErrorResponse(Response):
    """ Ответ сервера об ошибке """
    def __init__(self, code, origin, message):
        super().__init__(code, origin)
        self.data['error'] = message
