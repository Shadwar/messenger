from shared.jim import JIM


class Response(JIM):
    """ Ответ сервера """
    def __init__(self, code):
        super().__init__()
        self.data['response'] = code


class AlertResponse(Response):
    """ Ответ сервера о сообщении/уведомлении """
    def __init__(self, code, message):
        super().__init__(code)
        self.data['alert'] = message


class ErrorResponse(Response):
    """ Ответ сервера об ошибке """
    def __init__(self, code, message):
        super().__init__(code)
        self.data['error'] = message
