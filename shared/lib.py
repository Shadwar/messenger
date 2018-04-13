from shared.packets import ErrorPacket


def login_required(func):
    """
    Декоратор для обработчиков команд пользователя на сервере
    :param func:
    :return:
    """
    def wrapper(*args):
        server = args[1]
        user = args[2]
        command = args[3]

        if user.gid is None:
            user.send_message(ErrorPacket(401, command['id'], 'Login required'))
            return None
        return func(*args)

    return wrapper
